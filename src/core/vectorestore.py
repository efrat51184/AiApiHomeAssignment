import openai
import pinecone
import asyncio
from typing import List, Dict

class VectorStore:
    def __init__(self, pinecone_config: Dict, openai_api_key: str):
        openai.api_key = openai_api_key
        pinecone.init(api_key=pinecone_config['api_key'], environment=pinecone_config['environment'])
        self.index = pinecone.Index(pinecone_config['index_name'])
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        response = await asyncio.to_thread(
            openai.Embedding.create,
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    
    async def store_embedding(self, text: str, metadata: dict) -> None:
        """Store embedding with metadata."""
        embedding = await self.generate_embedding(text)
        await asyncio.to_thread(
            self.index.upsert,
            vectors=[(metadata.get('file'), embedding, metadata)]
        )
        print(f"Stored embedding for file: {metadata.get('file')}")
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar embeddings."""
        query_embedding = await self.generate_embedding(query)
        results = await asyncio.to_thread(
            self.index.query,
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results['matches']
