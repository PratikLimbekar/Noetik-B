import os
from pathlib import Path

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from git import Repo

router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"]
)

REPOSITORIES_DIR = Path("repositories")
REPOSITORIES_DIR.mkdir(exist_ok=True)


@router.post("/import")
async def import_repository(
    request: Request,
    owner: str,
    repo: str
):
    access_token = request.session.get("github_access_token")

    if not access_token:
        return JSONResponse(
            status_code=401,
            content={
                "error": "GitHub authentication required"
            }
        )

    # Verify that the repository exists and is accessible
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2026-03-10",
            }
        )

    if response.status_code != 200:
        return JSONResponse(
            status_code=response.status_code,
            content={
                "error": "Repository is not accessible",
                "details": response.json()
            }
        )

    repository = response.json()

    # Local directory for this repository
    repo_path = REPOSITORIES_DIR / f"{owner}_{repo}"

    # Already imported
    if repo_path.exists():
        return {
            "message": "Repository already imported",
            "repository": {
                "owner": owner,
                "name": repo,
                "path": str(repo_path)
            }
        }

    # Clone using the GitHub access token
    clone_url = repository["clone_url"]

    authenticated_url = clone_url.replace(
        "https://github.com/",
        f"https://x-access-token:{access_token}@github.com/"
    )

    try:
        Repo.clone_from(
            authenticated_url,
            repo_path
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to clone repository",
                "details": str(e)
            }
        )

    return {
        "message": "Repository imported successfully",
        "repository": {
            "owner": owner,
            "name": repo,
            "full_name": repository["full_name"],
            "path": str(repo_path),
            "default_branch": repository["default_branch"]
        }
    }