import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.auth import get_current_user
from app.models.user import User
from app.config import UPLOAD_DIR

router = APIRouter()

CV_FILENAME = "cv.pdf"


def cv_path() -> str:
    return os.path.join(UPLOAD_DIR, CV_FILENAME)


@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    content = await file.read()
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
