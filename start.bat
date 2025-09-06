@echo off
echo Windows Port Forward Manager
echo ========================
echo.
echo Starting application...
echo.

REM Try different Python commands
if exist "%LOCALAPPDATA%\Programs\Python" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" (
            "%%i\python.exe" main.py
            goto :end
        )
    )
)

REM Try python in system PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    python main.py
    goto :end
)

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    py main.py
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    python3 main.py
    goto :end
)

echo Error: Python interpreter not found!
echo Please install Python 3.7 or higher.
echo Download: https://www.python.org/downloads/
echo.
pause
goto :end

:end
echo.
echo Application exited.
pause