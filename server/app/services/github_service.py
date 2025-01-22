from github import Github
from app.core.config import settings
from app.utils.url_parser import parse_github_url
from typing import List, Dict

class GitHubService:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
    
    async def get_repo_contents(self, repo_url: str) -> List[Dict[str, str]]:
        owner, repo_name = parse_github_url(repo_url)
        repo = self.client.get_repo(f"{owner}/{repo_name}")
        contents = []
        
        for content in repo.get_contents(""):
            if content.type == "file":
                contents.append({
                    "path": content.path,
                    "content": content.decoded_content.decode()
                })
        
        return contents

