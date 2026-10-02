from fastapi import FastAPI
from app.auth.github import router as github_router

app = FastAPI(title="Noetik")

app.include_router(github_router)

@app.get("/")
def root():
    return {
        "message": "bappa ftw"
    }