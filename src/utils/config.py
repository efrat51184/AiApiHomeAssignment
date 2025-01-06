import yaml
from pathlib import Path

class Config:
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_openai_api_key(self):
        return self.config['openai']['api_key']

    def get_pinecone_config(self):
        return self.config['pinecone']

    def get_clone_path(self):
        return Path(self.config['repository']['clone_path'])
