import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.auth import get_current_user
from app.models.user import User
from app.config import UPLOAD_DIR

router = APIRouter()

SYNTHESIS_FILENAME = "tableau_synthese.pdf"


def synthesis_path() -> str:
    return os.path.join(UPLOAD_DIR, SYNTHESIS_FILENAME)


@router.post("/upload")
async def upload_synthesis(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    content = await file.read()
    with open(synthesis_path(), "wb") as f:
        f.write(content)
    return {"message": "Tableau de synthèse mis à jour"}


@router.get("")
async def download_synthesis():
    path = synthesis_path()
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Tableau de synthèse introuvable")
    return FileResponse(
        path,
        media_type="application/pdf",
        filename="Tableau_Synthese_Tommy_Etendard.pdf",
        headers={"Content-Disposition": "attachment; filename=Tableau_Synthese_Tommy_Etendard.pdf"},
    )
