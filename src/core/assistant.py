import openai
import asyncio

class Assistant:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key

    async def analyze_code(self, query: str, context: str) -> str:
        """Use OpenAI's assistant to analyze code."""
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for analyzing code."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuery:\n{query}"}
            ]
        )
        return response['choices'][0]['message']['content']
