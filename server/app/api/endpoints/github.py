from fastapi import APIRouter, HTTPException
from app.models.github import RepoQuery, RepoResponse
from app.services.github_service import GitHubService
from app.services.vector_store import VectorStore

router = APIRouter()
github_service = GitHubService()
vector_store = VectorStore()



@router.post("/chat", response_model=RepoResponse)
async def process_repo(req: RepoQuery):
    print("Processing repo", req.repo_url)
    print("Query", req.query)
    try:
        repo_contents = await github_service.get_repo_contents(req.repo_url)
        print(f"Processing {len(repo_contents)} files")
        # print repo_contents
        print("repo_contents", repo_contents)
        vector_store.add_texts(repo_contents)
        response = vector_store.query(req.query)
        return RepoResponse(response=response)
    except Exception as e:
        raise HTTPException(500, str(e))
    
@router.post("/analyze-repo")
async def analyze_repo(repo_url: str):
    qa_system = GitHubRepoQA()
    repo_id = hash(repo_url)  # Generate unique ID
    await qa_system.process_repo(repo_url)
    return {"repo_id": repo_id}
