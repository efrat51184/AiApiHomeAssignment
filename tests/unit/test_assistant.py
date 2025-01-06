import pytest
from unittest.mock import AsyncMock, patch
from src.core.assistant import Assistant

@pytest.mark.asyncio
async def test_analyze_code():
    assistant = Assistant(openai_api_key="test_key")
    with patch("openai.ChatCompletion.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {
            'choices': [{'message': {'content': 'This code defines a function.'}}]
        }
        analysis = await assistant.analyze_code("What does this code do?", "def foo(): pass")
        assert analysis == "This code defines a function."
