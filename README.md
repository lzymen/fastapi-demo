# FastAPI Demo

一个完整的 FastAPI demo 项目，包含用户认证、文件上传下载等功能。

## 功能特性

- ✅ 用户注册和登录（JWT 认证）
- ✅ 密码加密存储（bcrypt）
- ✅ 文件上传（支持多文件）
- ✅ 文件下载（流式传输）
- ✅ 文件列表和删除
- ✅ SQLite 数据库（轻量级）
- ✅ 自动生成 API 文档
- ✅ 完整的测试用例

## 技术栈

- **FastAPI** - 现代、高性能的 Web 框架
- **SQLAlchemy** - Python SQL 工具包和 ORM
- **Python-Jose** - JWT 令牌处理
- **Passlib** - 密码哈希
- **Pydantic** - 数据验证
- **Uvicorn** - ASGI 服务器

## 项目结构

```
fastapi_demo/
├── main.py              # 应用入口
├── config.py            # 配置管理
├── database.py          # 数据库连接
├── models/              # 数据模型
│   ├── __init__.py
│   └── user.py
├── schemas/             # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   └── file.py
├── routers/             # API 路由
│   ├── __init__.py
│   ├── auth.py
│   └── files.py
├── services/            # 业务逻辑
│   ├── __init__.py
│   ├── auth_service.py
│   └── file_service.py
├── utils/               # 工具函数
│   ├── __init__.py
│   ├── security.py
│   └── deps.py
├── uploads/             # 上传文件存储目录
└── tests/               # 测试文件
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    └── test_files.py
```

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync
```

### 2. 运行项目

```bash
# 开发模式（热重载）
uvicorn main:app --reload

# 或使用 poe
poe dev
```

### 3. 访问 API 文档

打开浏览器访问：http://localhost:8000/docs

## API 端点

### 认证相关

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /auth/me` - 获取当前用户信息（需要认证）

### 文件管理

- `POST /files/upload` - 上传文件（需要认证）
- `GET /files/` - 获取文件列表（需要认证）
- `GET /files/{file_id}` - 下载文件（需要认证）
- `DELETE /files/{file_id}` - 删除文件（需要认证）

### 其他

- `GET /` - 根路由
- `GET /health` - 健康检查

## 使用示例

### 1. 用户注册

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. 用户登录

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 上传文件

```bash
curl -X POST "http://localhost:8000/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/your/file.txt"
```

### 4. 下载文件

```bash
curl -X GET "http://localhost:8000/files/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output downloaded_file.txt
```

## 运行测试

```bash
# 使用 pytest
pytest

# 或使用 poe
poe test
```

## 配置说明

配置项在 `config.py` 中定义，可以通过环境变量或 `.env` 文件覆盖：

- `DATABASE_URL` - 数据库连接字符串
- `SECRET_KEY` - JWT 密钥（生产环境请修改）
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token 过期时间
- `MAX_FILE_SIZE` - 最大文件大小（字节）

## 部署到服务器

### 方式一：使用 uv（推荐）

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 同步依赖
uv sync

# 3. 运行服务
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 方式二：使用 pip

```bash
# 1. 从 pyproject.toml 安装
pip install .

# 2. 运行服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 许可证

MIT License
