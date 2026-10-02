Virtual env: python -m venv venv, venv\Scripts\activate
Installed fastapi, uvicorn, httpx, gitpython, python-dotenv

run: uvicorn app.main:app --reload

GitHub App Setup:
github -> settings -> developer settings -> GitHub App
Repo permissins -> actions? admin? commit statuses? contents is done. metadata is compulsory. deployments? issues? pull requests?

Webhook currently inactive -> to be active later to get updates from repo

put app id, client id and client secret in env.


installed authlib to avoid implementing backedn protocols