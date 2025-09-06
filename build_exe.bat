@echo off
chcp 65001 >nul
echo ========================================
echo     Windows端口转发管理工具打包脚本
echo ========================================
echo.

echo [1/4] 检查PyInstaller安装状态...
py -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyInstaller未安装，正在安装...
    py -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ PyInstaller安装失败！
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装完成！
) else (
    echo ✅ PyInstaller已安装
)
echo.

echo [2/4] 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo ✅ 清理完成！
echo.

echo [3/4] 开始打包应用程序...
echo 这可能需要几分钟时间，请耐心等待...
py -m PyInstaller build_exe.spec --clean
if %errorlevel% neq 0 (
    echo ❌ 打包失败！请检查错误信息。
    pause
    exit /b 1
)
echo ✅ 打包完成！
echo.

echo [4/4] 检查生成的文件...
if exist "dist\WinPortForwarder.exe" (
    echo ✅ 可执行文件生成成功！
    echo 📁 文件位置: %cd%\dist\WinPortForwarder.exe
    echo 📊 文件大小:
    dir "dist\WinPortForwarder.exe" | find "WinPortForwarder.exe"
    echo.
    echo ========================================
    echo 🎉 打包完成！
    echo ========================================
    echo 您可以在 dist 文件夹中找到可执行文件：
    echo WinPortForwarder.exe
    echo.
    echo 该文件可以在没有安装Python的Windows系统上运行。
    echo.
    set /p choice=是否现在运行测试程序？(Y/N): 
    if /i "%choice%"=="Y" (
        echo 正在启动程序...
        start "" "dist\WinPortForwarder.exe"
    )
) else (
    echo ❌ 可执行文件生成失败！
    echo 请检查上面的错误信息。
)

echo.
echo 按任意键退出...
pause >nul