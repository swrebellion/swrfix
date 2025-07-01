@echo off
echo Building Star Wars: Rebellion Community Fix Installer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if errorlevel 1 (
    echo Installing pywin32...
    pip install pywin32
)

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "Star_Wars_Rebellion_Community_Fix_Installer" --icon=icon.ico main.py

if exist "dist\Star_Wars_Rebellion_Community_Fix_Installer.exe" (
    echo.
    echo ✓ Build successful!
    echo ✓ Executable created: dist\Star_Wars_Rebellion_Community_Fix_Installer.exe
    echo.
    echo Creating distribution package...
    python build_distribution.py
    echo.
    echo ✓ Ready for distribution!
    echo Check the created ZIP file for the complete package.
) else (
    echo.
    echo ✗ Build failed!
    echo Check the output above for errors.
)

echo.
pause
