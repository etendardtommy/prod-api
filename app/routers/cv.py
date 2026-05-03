import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.auth import get_current_user
from app.models.user import User
from app.config import UPLOAD_DIR

router = APIRouter()

CV_FILENAME = "cv.pdf"
MAX_PDF_SIZE = 10 * 1024 * 1024  # 10 Mo


def cv_path() -> str:
    return os.path.join(UPLOAD_DIR, CV_FILENAME)


@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Seuls les fichiers PDF sont acceptés")

    content = await file.read(MAX_PDF_SIZE + 1)
    if len(content) > MAX_PDF_SIZE:
        raise HTTPException(413, "Fichier trop volumineux. Taille maximum : 10 Mo")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(cv_path(), "wb") as f:
        f.write(content)
    return {"message": "CV mis à jour"}


@router.get("")
async def download_cv():
    path = cv_path()
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="CV introuvable")
    return FileResponse(
        path,
        media_type="application/pdf",
        filename="CV_Tommy_Etendard.pdf",
        headers={"Content-Disposition": "attachment; filename=CV_Tommy_Etendard.pdf"},
    )
