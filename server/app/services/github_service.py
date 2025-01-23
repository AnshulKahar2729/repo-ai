from github import Github
from app.core.config import settings
from app.utils.url_parser import parse_github_url
from typing import List, Dict

class GitHubService:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
    
    def get_repo_contents(self, repo_url: str) -> List[Dict[str, str]]:
        owner, repo_name = parse_github_url(repo_url)
        print(f"Owner: {owner}, Repo: {repo_name}")
        repo = self.client.get_repo(f"{owner}/{repo_name}")
        print(f"Repo: {repo}")
        return self._traverse_contents(repo, "")
    
    def _traverse_contents(self, repo, path: str) -> List[Dict[str, str]]:
        contents = []
        
        try:
            for content in repo.get_contents(path):
                if content.type == "file":
                    contents.append({
                        "path": content.path,
                        "content": content.decoded_content.decode('utf-8')
                    })
                elif content.type == "dir":
                    dir_contents = self._traverse_contents(repo, content.path)
                    contents.extend(dir_contents)
        except Exception as e:
            print(f"Error accessing {path}: {str(e)}")
        print(f"Contents: {contents}")
        return contents