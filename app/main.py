from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.config import ALLOWED_ORIGINS, UPLOAD_DIR
from app.database import engine, Base
from app.models import *  # noqa: F401, F403
from app.routers import auth, roster, gallery, projects, articles, experiences, messages, analytics, upload
from app.routers import skills
from app.routers import about
from app.routers import cv
from app.routers import synthesis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée les tables manquantes sans toucher aux existantes
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Eclyps Multi-Site API",
    description="API centralisée pour Portfolio, Eclyps et Admin.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers uploadés
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Auth
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# Public + Admin routes — préfixes alignés sur les appels des fronts
app.include_router(roster.router, prefix="/api/roster", tags=["Roster"])
app.include_router(gallery.router, prefix="/api/gallery", tags=["Galerie"])
app.include_router(projects.router, prefix="/api/portfolio/projects", tags=["Projets"])
app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(experiences.router, prefix="/api/experience", tags=["Expériences"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(skills.router, prefix="/api/skills", tags=["Compétences"])
app.include_router(about.router, prefix="/api/about", tags=["À propos"])
app.include_router(cv.router, prefix="/api/cv", tags=["CV"])
app.include_router(synthesis.router, prefix="/api/synthesis", tags=["Synthèse"])


@app.get("/")
async def root():
    return {"message": "API Multi-Site v2"}


# Admin SPA — fallback SPA : sert le fichier s'il existe, sinon index.html
ADMIN_DIST = os.path.join(os.path.dirname(__file__), "..", "admin_dist")

if os.path.isdir(ADMIN_DIST):
    @app.get("/admin")
    async def serve_admin_root():
        return FileResponse(os.path.join(ADMIN_DIST, "index.html"))

    @app.get("/admin/{full_path:path}")
    async def serve_admin(full_path: str):
        file_path = os.path.join(ADMIN_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(ADMIN_DIST, "index.html"))
