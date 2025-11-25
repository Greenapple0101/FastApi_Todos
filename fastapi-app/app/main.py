from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from prometheus_fastapi_instrumentator import Instrumentator

from .api.routes import router as todo_router

BASE_DIR = Path(__file__).resolve().parent  # /app/fastapi-app/app
APP_ROOT = BASE_DIR.parent                  # /app/fastapi-app
STATIC_DIR = APP_ROOT / "static"
TEMPLATES_DIR = APP_ROOT / "templates"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        csp = ("default-src 'self'; img-src 'self' data: http: https:;"
               "style-src 'self' 'unsafe-inline'; "
               "script-src 'self' 'unsafe-inline'")
        response.headers.setdefault("Content-Security-Policy", csp)
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Todos", version="2.0.0")

    # Static mount
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
        print(f"✅ Static files mounted from: {STATIC_DIR}")
    else:
        print(f"❌ Static not found at: {STATIC_DIR}")

    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    Instrumentator().instrument(app).expose(app)

    app.include_router(todo_router)

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/health")
    async def health():
        return JSONResponse({"status": "ok"})

    return app


app = create_app()
