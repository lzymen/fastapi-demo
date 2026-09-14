@echo off
REM FastAPI Demo 启动脚本

echo ================================
echo FastAPI Demo 启动脚本
echo ================================
echo.
echo 选择监听模式:
echo 1) 本地访问 (127.0.0.1) - 仅本机可访问
echo 2) 外部访问 (0.0.0.0)   - 局域网/公网可访问
echo.
set /p choice="请输入选择 (1 或 2): "

if "%choice%"=="1" (
    set HOST=127.0.0.1
) else if "%choice%"=="2" (
    set HOST=0.0.0.0
) else (
    echo 无效选择，默认使用本地访问
    set HOST=127.0.0.1
)

set PORT=8000
echo.
echo 启动 FastAPI Demo...
echo 监听地址: %HOST%:%PORT%
echo API 文档: http://localhost:%PORT%/docs
echo.
echo 按 Ctrl+C 停止服务
echo ================================

REM 检查是否安装了 uv
where uv >nul 2>nul
if %errorlevel% equ 0 (
    uv run uvicorn main:app --host %HOST% --port %PORT% --reload
) else (
    python -m uvicorn main:app --host %HOST% --port %PORT% --reload
)
