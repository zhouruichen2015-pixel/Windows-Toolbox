@echo off
chcp 65001 >nul
title 启动 MHY 工具箱

:: 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
:: 去掉末尾的反斜杠
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 尝试多种方式找到 Python
set "PYTHON_CMD="

:: 方法1: 尝试使用 'python' 命令
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    goto :found_python
)

:: 方法2: 尝试使用 'python3' 命令
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python3"
    goto :found_python
)

:: 方法3: 尝试使用 'py' 命令（Python启动器）
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
    goto :found_python
)

:: 方法4: 尝试从常见安装位置查找
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%ProgramFiles%\Python312\python.exe"
    "%ProgramFiles%\Python311\python.exe"
    "%ProgramFiles%\Python310\python.exe"
) do (
    if exist %%p (
        set "PYTHON_CMD=%%p"
        goto :found_python
    )
)

:: 如果都没找到，提示用户
echo 错误: 未找到 Python！
echo 请确保已安装 Python 并添加到系统 PATH 环境变量中。
echo.
echo 你可以访问 https://www.python.org/downloads/ 下载安装。
pause
exit /b 1

:found_python
echo 使用 Python: %PYTHON_CMD%
echo.

:: 运行主程序
"%PYTHON_CMD%" "%SCRIPT_DIR%\main.py"

:: 脚本运行完后暂停窗口（方便看报错，不需要可以删掉这行）
pause
