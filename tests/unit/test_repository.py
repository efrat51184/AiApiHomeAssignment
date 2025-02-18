import pytest
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.core.repository import process_file

@pytest.mark.asyncio
async def test_process_file():
    test_file = Path("tests/test_data/sample.py")
    content = await process_file(test_file)
    assert isinstance(content, str)
    assert "def" in content  # Assuming sample.py contains a function
