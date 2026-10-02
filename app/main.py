from fastapi import FastAPI
from app.auth.github import router as github_router
from app.config import SESSION_SECRET
from starlette.middleware.sessions import SessionMiddleware
from app.repos.github import router as repositories_router


app = FastAPI(title="Noetik")

app.add_middleware(SessionMiddleware, secret_key = SESSION_SECRET, same_site="lax", https_only=False) #make this true for prod

app.include_router(github_router)
app.include_router(repositories_router)

@app.get("/")
def root():
    return {
        "message": "bappa ftw"
    }