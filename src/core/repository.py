import asyncio
from pathlib import Path
from git import Repo, GitCommandError
import aiofiles
import mimetypes
import magic



async def clone_repository(repo_url: str, clone_path: Path) -> Path:
    """Clone a Git repository to the specified path."""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, Repo.clone_from, repo_url, clone_path)
        print(f"Repository cloned to {clone_path}")
    except GitCommandError as e:
        print(f"Error cloning repository: {e}")
        raise e
    return clone_path


async def process_files(repo_path: Path, max_tokens: int = 1000) -> list[str]:
    """Process files in the repository asynchronously and return chunks."""
    tasks = []
    for file_path in repo_path.rglob('*'):
        if file_path.is_file() and is_supported_file_mine_type(file_path):  # check supported files
            tasks.append(process_file(file_path, max_tokens))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_chunks = []
    for result in results:
        if isinstance(result, list):
            all_chunks.extend(result)
    return all_chunks



async def process_file(file_path: Path, max_tokens: int = 1000) -> list[str]:
    """Process a single file and split it into chunks asynchronously."""
    try:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()  # reading the file contents
            return chunk_text(content, max_tokens)  # dividing text into sections
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []


def chunk_text(text: str, max_tokens: int = 1000) -> list[str]:
    """Split text into smaller chunks to fit within token limits."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def is_supported_file_mine_type(file_path: Path) -> bool:
    """option 1 - Check if a file is of a supported type with mine_type"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        # supported files
        supported_mime_types = [
            "text/plain",       # text files
            "application/json", # JSON
            "application/javascript", # JavaScript
            "text/x-python",    # Python
            "text/x-java-source" # Java
        ]
        return mime_type in supported_mime_types
    return False


def is_supported_file_magic(file_path: Path) -> bool:
    """option 2 - Check if a file is of a supported type using python-magic"""
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(str(file_path))
    supported_mime_types = [
        "text/plain",       # text file
        "application/json", # JSON
        "application/javascript", # JavaScript
        "text/x-python",    # Python
        "text/x-java-source" # Java
    ]
    return mime_type in supported_mime_types
