#!/bin/bash
# Setup script for EDITH Drone Environment verification tests

set -e  # Exit on error

echo "=========================================="
echo "EDITH Drone Environment - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -eq 10 ]; then
    echo "✓ Python $PYTHON_VERSION (correct version)"
else
    echo "⚠ WARNING: Python $PYTHON_VERSION detected"
    echo "  Recommended: Python 3.10"
    echo "  Newer versions may have pybullet build issues"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if conda is available
echo ""
echo "[2/5] Checking for conda..."
if command -v conda &> /dev/null; then
    echo "✓ Conda found"
    echo ""
    echo "Recommended: Create isolated environment"
    echo "  conda create -n drones python=3.10"
    echo "  conda activate drones"
    echo ""
    read -p "Have you activated the conda environment? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please activate conda environment first, then re-run this script"
        exit 1
    fi
else
    echo "⚠ Conda not found (optional but recommended)"
fi

# Upgrade pip
echo ""
echo "[3/5] Upgrading pip..."
python3 -m pip install --upgrade pip
echo "✓ Pip upgraded"

# Install requirements
echo ""
echo "[4/5] Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Clone and install gym-pybullet-drones
echo ""
echo "[5/5] Installing gym-pybullet-drones..."

if [ -d "gym-pybullet-drones" ]; then
    echo "⚠ gym-pybullet-drones directory already exists"
    read -p "Reinstall? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf gym-pybullet-drones
    else
        echo "Skipping gym-pybullet-drones installation"
        echo ""
        echo "=========================================="
        echo "Setup complete!"
        echo "=========================================="
        exit 0
    fi
fi

echo "Cloning gym-pybullet-drones..."
git clone https://github.com/utiasDSL/gym-pybullet-drones.git

echo "Checking out main branch..."
cd gym-pybullet-drones
git checkout main

echo "Installing in editable mode..."
pip install -e .

cd ..

echo "✓ gym-pybullet-drones installed"

# Summary
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run verification tests:"
echo "     python3 run_all_tests.py"
echo ""
echo "  2. Or run tests individually:"
echo "     python3 test_01_imports.py"
echo "     python3 test_02_headless_basic.py"
echo "     python3 test_03_headless_env.py"
echo "     python3 test_04_camera_headless.py  # CRITICAL"
echo ""
echo "  3. Check test_camera_output.png after test 04"
echo "     to verify image quality"
echo ""
echo "=========================================="
