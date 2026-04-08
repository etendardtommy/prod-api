import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File
from app.auth import get_current_user
from app.models.user import User
from app.config import UPLOAD_DIR, API_PUBLIC_URL

router = APIRouter()


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": filename, "url": f"{API_PUBLIC_URL}/uploads/{filename}"}
