#redirects to github
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.config import GITHUB_CLIENT_ID

router = APIRouter(prefix="/api/auth/github", tags=["GitHub Auth"])

@router.get("/login")
async def github_login():
    redirect_url = "http://localhost:8000/api/auth/github/callback"
    github_url = (
        "https://github.com/login/authorize"f"?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_url}&scope=read:user"
    )

    return RedirectResponse(github_url)