# app/memory.py

import chromadb
from datetime import datetime

class Memory:
    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="chatbot_memory")

    def add_message(self, user_id, message, role):
        """Adds a message to the user's conversation history."""
        timestamp = datetime.now().isoformat()
        self.collection.add(
            documents=[message],
            metadatas=[{"role": role, "user_id": user_id, "timestamp": timestamp}],
            ids=[f"{user_id}-{timestamp}"]
        )

    def get_context(self, user_id, n_results=10):
        """Retrieves the most recent conversation history for a user."""
        try:
            results = self.collection.query(
                # Using a generic query text as we are filtering by metadata
                query_texts=[""], 
                n_results=n_results,
                where={"user_id": user_id}
            )
            # ChromaDB can return empty lists if no results are found
            if results and results['documents'] and results['documents'][0]:
                # Sort documents by timestamp to get the most recent ones
                # This is a more robust way to handle context
                history = sorted(zip(results['documents'][0], results['metadatas'][0]), key=lambda x: x[1]['timestamp'], reverse=True)
                # Format the history for the prompt
                formatted_history = [f"{item[1]['role']}: {item[0]}" for item in history]
                return "\n".join(formatted_history)
            else:
                return "No previous conversation history found."
        except Exception as e:
            print(f"Error retrieving context from ChromaDB: {e}")
            return "Could not retrieve conversation history."