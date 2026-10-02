Virtual env: python -m venv venv, venv\Scripts\activate
Installed fastapi, uvicorn, httpx, gitpython, python-dotenv

run: uvicorn app.main:app --reload

GitHub App Setup:
github -> settings -> developer settings -> GitHub App
Repo permissins -> actions? admin? commit statuses? contents is done. metadata is compulsory. deployments? issues? pull requests?
Webhook currently inactive -> to be active later to get updates from repo


put app id, client id and client secret in env.


completed the user OAuth and callback part/mechanism
Adding middleware using Starlette now.

Endpoints:
/: base
/api/auth/github/login: Github Oauth 
/api/auth/github/callback: exchange code for access token and stores auth user in session
/api/auth/github/me: identify current auth user
/api/auth/github/repos: fetch repos accessible to user
/api/repos/import: POST: verify and clone selected repo into local