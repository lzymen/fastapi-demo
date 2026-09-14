import uuid
from pathlib import Path
from datetime import datetime

import aiofiles
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from config import settings, UPLOAD_PATH
from models.user import File, User
from schemas.file import FileResponse, FileListResponse


class FileService:
    """文件服务"""

    @staticmethod
    async def upload_file(
        db: Session,
        file: UploadFile,
        current_user: User
    ) -> FileResponse:
        """上传文件"""
        # 检查文件大小
        file_size = 0
        content = await file.read()
        file_size = len(content)

        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # 生成唯一文件名
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # 保存文件
        file_path = UPLOAD_PATH / unique_filename
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # 保存文件信息到数据库
        db_file = File(
            filename=unique_filename,
            original_filename=file.filename,
            file_size=file_size,
            content_type=file.content_type,
            user_id=current_user.id
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return FileResponse.model_validate(db_file)

    @staticmethod
    def get_user_files(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> FileListResponse:
        """获取用户的文件列表"""
        files = db.query(File).filter(
            File.user_id == current_user.id
        ).offset(skip).limit(limit).all()

        total = db.query(File).filter(
            File.user_id == current_user.id
        ).count()

        return FileListResponse(
            files=[FileResponse.model_validate(f) for f in files],
            total=total
        )

    @staticmethod
    def get_file_by_id(db: Session, file_id: int, current_user: User) -> File:
        """根据ID获取文件"""
        file = db.query(File).filter(
            File.id == file_id,
            File.user_id == current_user.id
        ).first()

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        return file

    @staticmethod
    def delete_file(db: Session, file_id: int, current_user: User) -> dict:
        """删除文件"""
        file = FileService.get_file_by_id(db, file_id, current_user)

        # 删除物理文件
        file_path = UPLOAD_PATH / file.filename
        if file_path.exists():
            file_path.unlink()

        # 删除数据库记录
        db.delete(file)
        db.commit()

        return {"message": "File deleted successfully"}


# 创建全局服务实例
file_service = FileService()
