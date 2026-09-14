from datetime import datetime
from pydantic import BaseModel


class FileResponse(BaseModel):
    """文件响应"""
    id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    upload_time: datetime
    user_id: int

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    """文件列表响应"""
    files: list[FileResponse]
    total: int
