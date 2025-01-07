import yaml
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path
import os

class Config:
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.load_api_key()
        
    def load_api_key(self):
        # Retrieve the API key from the .env file
        load_dotenv(dotenv_path = Path('../../config/.env'))
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in .env file")
        
    def get_openai_api_key(self):
        return self.api_key

    def get_pinecone_config(self):
        return self.config['pinecone']

    def get_clone_path(self):
        return Path(self.config['repository']['clone_path'])
            
