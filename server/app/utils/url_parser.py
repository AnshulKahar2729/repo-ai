import re
from fastapi import HTTPException

def parse_github_url(url: str) -> tuple[str, str]:
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, url)
    if not match:
        raise HTTPException(400, "Invalid GitHub URL")
    return match.group(1), match.group(2)

