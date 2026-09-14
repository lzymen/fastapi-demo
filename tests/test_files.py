import pytest
from fastapi import status


def get_auth_headers(client, test_user):
    """获取认证 headers"""
    client.post("/auth/register", json=test_user)
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_upload_file(client, test_user):
    """测试文件上传"""
    headers = get_auth_headers(client, test_user)

    # 创建测试文件
    file_content = b"Hello, World!"
    files = {"file": ("test.txt", file_content, "text/plain")}

    response = client.post("/files/upload", headers=headers, files=files)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["original_filename"] == "test.txt"
    assert data["file_size"] == len(file_content)
    assert data["content_type"] == "text/plain"


def test_upload_file_no_auth(client):
    """测试未认证上传文件"""
    files = {"file": ("test.txt", b"Hello", "text/plain")}
    response = client.post("/files/upload", files=files)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_files(client, test_user):
    """测试获取文件列表"""
    headers = get_auth_headers(client, test_user)

    # 上传两个文件
    files1 = {"file": ("test1.txt", b"Content 1", "text/plain")}
    files2 = {"file": ("test2.txt", b"Content 2", "text/plain")}
    client.post("/files/upload", headers=headers, files=files1)
    client.post("/files/upload", headers=headers, files=files2)

    # 获取文件列表
    response = client.get("/files/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2
    assert len(data["files"]) == 2


def test_download_file(client, test_user):
    """测试文件下载"""
    headers = get_auth_headers(client, test_user)

    # 上传文件
    file_content = b"Hello, World!"
    files = {"file": ("test.txt", file_content, "text/plain")}
    upload_response = client.post("/files/upload", headers=headers, files=files)
    file_id = upload_response.json()["id"]

    # 下载文件
    response = client.get(f"/files/{file_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content == file_content


def test_delete_file(client, test_user):
    """测试删除文件"""
    headers = get_auth_headers(client, test_user)

    # 上传文件
    files = {"file": ("test.txt", b"Hello", "text/plain")}
    upload_response = client.post("/files/upload", headers=headers, files=files)
    file_id = upload_response.json()["id"]

    # 删除文件
    response = client.delete(f"/files/{file_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "File deleted successfully"

    # 验证文件已删除
    list_response = client.get("/files/", headers=headers)
    assert list_response.json()["total"] == 0


def test_download_nonexistent_file(client, test_user):
    """测试下载不存在的文件"""
    headers = get_auth_headers(client, test_user)

    response = client.get("/files/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
