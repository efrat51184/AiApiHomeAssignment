import yaml
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path
import os

class Config:
    def __init__(self, config_path: Path):
        with open("\config.yaml", 'r') as file:
            self.config = yaml.safe_load(file)
        self.load_api_key()
        
    def load_api_key(self):
        # Retrieve the API key from the .env file
        load_dotenv(dotenv_path = Path('../../config/.env'))
        self.config['pinecone']['api_key'] = os.getenv("PINECONE_API_KEY")
        if not self.config['pinecone']['api_key']:
            raise ValueError("PINECONE_API_KEY not found in .env file")
        self.config['openai']['api_key'] = os.getenv("OPENAI_API_KEY")
        if not self.config['openai']['api_key']:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
    def get_openai_api_key(self):
        return self.config['openai']['api_key']

    def get_pinecone_config(self):
        return self.config['pinecone']

    def get_clone_path(self):
        return Path(self.config['repository']['clone_path'])
            
