import pytest
from httpx import AsyncClient
from pathlib import Path
import os
from src.main import app

@pytest.mark.asyncio
async def test_analyze_repository():
    """Test the end-to-end flow of analyzing a repository."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Step 1: Analyze a repository
        response = await client.post(
            "/analyze-repo/",
            json={"repo_url": "https://github.com/example/repo.git"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Repository analyzed and embeddings stored."

@pytest.mark.asyncio
async def test_search_repository():
    """Test the search functionality."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Step 2: Perform a search query
        response = await client.get(
            "/search/",
            params={"query": "Explain vector databases"}
        )
        assert response.status_code == 200
        results = response.json()["results"]
        assert len(results) > 0
        assert "text" in results[0]["metadata"]

@pytest.mark.asyncio
async def test_code_analysis():
    """Test the code analysis functionality."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Step 3: Analyze a specific code snippet
        response = await client.post(
            "/analyze-code/",
            json={
                "query": "What does this code do?",
                "file_id": "example_file_id"
            }
        )
        assert response.status_code == 200
        analysis = response.json()["analysis"]
        assert isinstance(analysis, str)
