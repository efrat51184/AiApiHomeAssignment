from fastapi import APIRouter, HTTPException
from pathlib import Path
import asyncio

from AiApiHomeAssignment.src.core.vectorestore import VectorStore
from src.core.repository import clone_repository, process_files
from src.core.assistant import Assistant
from src.utils.config import Config

router = APIRouter()

config = Config(Path('../config/config.yaml'))
vector_store = VectorStore(
    pinecone_config=config.get_pinecone_config(),
    openai_api_key=config.get_openai_api_key()
)
assistant = Assistant(openai_api_key=config.get_openai_api_key())

@router.post("/analyze-repo/")
async def analyze_repo(repo_url: str):
    clone_path = config.get_clone_path() / Path(repo_url).stem
    try:
        await clone_repository(repo_url, clone_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    files_content = await process_files(clone_path)
    store_tasks = []
    for file_content, file_path in zip(files_content, clone_path.rglob('*')):
        if file_path.is_file() and file_content:
            metadata = {"file": str(file_path)}
            store_tasks.append(vector_store.store_embedding(file_content, metadata))
    await asyncio.gather(*store_tasks)
    
    return {"message": "Repository analyzed and embeddings stored."}

@router.get("/search/")
async def search(query: str):
    results = await vector_store.search_similar(query)
    return {"results": results}

@router.post("/analyze-code/")
async def analyze_code(query: str, file_id: str):
    # Retrieve context from Pinecone
    results = await vector_store.search_similar(query, top_k=1)
    if not results:
        raise HTTPException(status_code=404, detail="No relevant code found.")
    context = results[0]['metadata']['text']
    analysis = await assistant.analyze_code(query, context)
    return {"analysis": analysis}
