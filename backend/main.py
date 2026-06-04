from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routes import auth, agent, webhook
from dotenv import load_dotenv
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")

app = FastAPI(title="Hermes Onboarding")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend/static")),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "frontend/templates")
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(agent.router, prefix="/api/agent")
app.include_router(webhook.router, prefix="/webhook")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"bot_username": BOT_USERNAME}
    )

@app.get("/success/{user_id}", response_class=HTMLResponse)
async def success(request: Request, user_id: str):
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={"user_id": user_id}
    )

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )