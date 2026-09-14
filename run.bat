@echo off
REM FastAPI Demo 启动脚本

echo 启动 FastAPI Demo...

REM 检查是否安装了 uv
where uv >nul 2>nul
if %errorlevel% equ 0 (
    echo 使用 uv 启动...
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
) else (
    echo 使用 python 启动...
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
)
