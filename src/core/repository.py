import asyncio
from pathlib import Path
from git import Repo, GitCommandError
import aiofiles

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

async def process_files(repo_path: Path) -> list[str]:
    """Process files in the repository asynchronously."""
    tasks = []
    for file_path in repo_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.js', '.java', '.txt']:  # ניתן להוסיף סוגי קבצים נוספים
            tasks.append(process_file(file_path))
    return await asyncio.gather(*tasks, return_exceptions=True)

async def process_file(file_path: Path) -> str:
    """Process a single file asynchronously."""
    try:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()
            print(f"Processed file: {file_path}")
            return content
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return ""
