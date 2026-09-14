import pytest
from fastapi import status


def test_register_user(client, test_user):
    """测试用户注册"""
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_user(client, test_user):
    """测试重复注册"""
    # 第一次注册
    client.post("/auth/register", json=test_user)

    # 第二次注册应该失败
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user(client, test_user):
    """测试用户登录"""
    # 先注册
    client.post("/auth/register", json=test_user)

    # 登录
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """测试错误密码登录"""
    # 先注册
    client.post("/auth/register", json=test_user)

    # 使用错误密码登录
    login_data = {
        "username": test_user["username"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, test_user):
    """测试获取当前用户信息"""
    # 注册
    client.post("/auth/register", json=test_user)

    # 登录获取 token
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]

    # 获取用户信息
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]


def test_get_current_user_no_token(client):
    """测试无 token 获取用户信息"""
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
