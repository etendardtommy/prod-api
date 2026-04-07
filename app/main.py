from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.config import ALLOWED_ORIGINS, UPLOAD_DIR
from app.routers import auth, roster, gallery, projects, articles, experiences, messages, analytics, upload

app = FastAPI(
    title="Eclyps Multi-Site API",
    description="API centralisée pour Portfolio, Eclyps et Admin.",
    version="2.0.0",
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


@app.get("/")
async def root():
    return {"message": "API Multi-Site v2 — /docs pour la documentation"}


# Admin SPA — fallback SPA : sert le fichier s'il existe, sinon index.html
ADMIN_DIST = os.path.join(os.path.dirname(__file__), "..", "admin_dist")

if os.path.isdir(ADMIN_DIST):
    @app.get("/admin")
    @app.get("/admin/{full_path:path}")
    async def serve_admin(full_path: str = ""):
        file_path = os.path.join(ADMIN_DIST, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(ADMIN_DIST, "index.html"))
