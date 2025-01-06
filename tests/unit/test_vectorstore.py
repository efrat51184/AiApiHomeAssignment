import pytest
from unittest.mock import AsyncMock, patch
from AiApiHomeAssignment.src.core.vectorestore import VectorStore

@pytest.mark.asyncio
async def test_generate_embedding():
    vector_store = VectorStore(pinecone_config={}, openai_api_key="test_key")
    with patch("openai.Embedding.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {'data': [{'embedding': [0.1, 0.2, 0.3]}]}
        embedding = await vector_store.generate_embedding("Test text")
        assert embedding == [0.1, 0.2, 0.3]
