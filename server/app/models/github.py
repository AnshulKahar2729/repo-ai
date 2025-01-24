from pydantic import BaseModel

class RepoQuery(BaseModel):
    repo_url: str
    query: str

class RepoResponse(BaseModel):
    response: str
    