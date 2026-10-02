from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

router = APIRouter(
    prefix="/api/auth/github",
    tags=["GitHub Auth"],
)

CALLBACK_URL = "http://localhost:8000/api/auth/github/callback"


@router.get("/login")
async def github_login():
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
    }

    url = (
        "https://github.com/login/oauth/authorize?"
        + urlencode(params)
    )

    return RedirectResponse(url)


@router.get("/callback")
async def github_callback(code: str, request: Request):
    async with httpx.AsyncClient() as client:

        # Exchange authorization code for access token
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": CALLBACK_URL,
            },
            headers={
                "Accept": "application/json",
            },
        )

        token_data = token_response.json()

        if "access_token" not in token_data:
            return {
                "error": "Failed to obtain GitHub access token",
                "details": token_data,
            }

        access_token = token_data["access_token"]

        # Get authenticated user
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )

        user_data = user_response.json()

    return {
        "message": "GitHub authentication successful",
        "user": {
            "login": user_data.get("login"),
            "name": user_data.get("name"),
            "avatar_url": user_data.get("avatar_url"),
        },
    }