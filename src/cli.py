import typer
from pathlib import Path
import asyncio
from src.core.repository import clone_repository, process_files
from src.core.vectorstore import VectorStore

app = typer.Typer()

@app.command()
def analyze_repo(repo_url: str, clone_path: Path = Path("./cloned_repo")):
    """Clone and analyze a Git repository."""
    async def async_analyze():
        # Pinecone
        vector_store = VectorStore(api_key="your_openai_api_key")

        # duplicate
        repo_path = await clone_repository(repo_url, clone_path)

        # process files
        files = await process_files(repo_path)
        for file_content in files:
            if isinstance(file_content, str):
                await vector_store.store_embedding(file_content, {"repo": repo_url})

    asyncio.run(async_analyze())

@app.command()
def search(query: str, top_k: int = 5):
    """Search for similar items in the vector store."""
    async def async_search():
        vector_store = VectorStore(api_key="your_openai_api_key")
        results = await vector_store.search_similar(query, top_k=top_k)
        for match in results:
            print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")

    asyncio.run(async_search())

@app.command()
def start_telemetry_server(port: int = 8001):
    """Start the telemetry server."""
    from src.utils.telemetry import start_telemetry_server
    start_telemetry_server(port)

if __name__ == "__main__":
    app()
