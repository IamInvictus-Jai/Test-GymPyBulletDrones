@echo off
REM Setup script for EDITH Drone Environment verification tests (Windows)

echo ==========================================
echo EDITH Drone Environment - Setup (Windows)
echo ==========================================
echo.

REM Check Python version
echo [1/6] Checking Python version...
python --version 2>nul
if errorlevel 1 (
    echo X Python not found in PATH
    echo   Please install Python 3.10 and add to PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo + Python %PYTHON_VERSION% found
echo   Recommended: Python 3.10
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo ! venv directory already exists
    set /p RECREATE="Recreate virtual environment? (y/n): "
    if /i "%RECREATE%"=="y" (
        echo Removing old venv...
        rmdir /s /q venv
    ) else (
        echo Using existing venv
        goto :activate_venv
    )
)

echo Creating venv...
python -m venv venv
if errorlevel 1 (
    echo X Failed to create virtual environment
    echo   Make sure Python 3.10 is installed correctly
    pause
    exit /b 1
)
echo + Virtual environment created

:activate_venv
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo X Failed to activate virtual environment
    pause
    exit /b 1
)
echo + Virtual environment activated

REM Upgrade pip
echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip
echo + Pip upgraded

REM Install requirements
echo.
echo [5/6] Installing Python dependencies...
pip install -r requirements.txt
echo + Dependencies installed

REM Clone and install gym-pybullet-drones
echo.
echo [6/6] Installing gym-pybullet-drones...

if exist gym-pybullet-drones (
    echo ! gym-pybullet-drones directory already exists
    set /p REINSTALL="Reinstall? (y/n): "
    if /i not "%REINSTALL%"=="y" (
        echo Skipping gym-pybullet-drones installation
        goto :done
    )
    rmdir /s /q gym-pybullet-drones
)

echo Cloning gym-pybullet-drones...
git clone https://github.com/utiasDSL/gym-pybullet-drones.git

echo Checking out main branch...
cd gym-pybullet-drones
git checkout main

echo Installing in editable mode...
pip install -e .

cd ..

echo + gym-pybullet-drones installed

:done
REM Summary
echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo Next steps:
echo   1. Activate virtual environment (if not already active):
echo      venv\Scripts\activate.bat
echo.
echo   2. Run verification tests:
echo      python run_all_tests.py
echo.
echo   3. Or run tests individually:
echo      python test_01_imports.py
echo      python test_02_headless_basic.py
echo      python test_03_headless_env.py
echo      python test_04_camera_headless.py  # CRITICAL
echo.
echo   4. Check test_camera_output.png after test 04
echo      to verify image quality
echo.
echo ==========================================
echo.
echo Virtual environment is active. You can now run tests.
pause
