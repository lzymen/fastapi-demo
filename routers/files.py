from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.file import FileResponse as FileSchema, FileListResponse
from services.file_service import file_service
from utils.deps import get_current_active_user
from config import UPLOAD_PATH

router = APIRouter(
    prefix="/files",
    tags=["文件管理"]
)


@router.post("/upload", response_model=FileSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """上传文件"""
    return await file_service.upload_file(db, file, current_user)


@router.get("/", response_model=FileListResponse)
async def list_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取文件列表"""
    return file_service.get_user_files(db, current_user, skip, limit)


@router.get("/{file_id}")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """下载文件"""
    file = file_service.get_file_by_id(db, file_id, current_user)
    file_path = UPLOAD_PATH / file.filename

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )

    return FileResponse(
        path=file_path,
        filename=file.original_filename,
        media_type=file.content_type
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除文件"""
    return file_service.delete_file(db, file_id, current_user)
