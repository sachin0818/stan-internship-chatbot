# app/chatbot.py

import google.generativeai as genai # type: ignore
from .memory import Memory

class Chatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.memory = Memory()

    def generate_response(self, user_id, user_message):
        """Generates a response from the chatbot."""
        self.memory.add_message(user_id, user_message, "user")
        context = self.memory.get_context(user_id)

        prompt = f"""
        You are a human-like conversational AI. Your goal is to be empathetic, engaging, and personal.
        Remember the user's past conversations and adapt your tone and responses accordingly.
        
        Previous conversation:
        {context}

        Current message from user {user_id}:
        {user_message}

        Your response:
        """

        response = self.model.generate_content(prompt)
        bot_response = response.text

        self.memory.add_message(user_id, bot_response, "assistant")
        return bot_response