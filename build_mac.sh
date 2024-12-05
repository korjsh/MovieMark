#!/bin/bash

echo "Building executable for macOS..."

pyinstaller --onefile --hidden-import=passlib.handlers.bcrypt \
    --add-data ".env:." \
    --name my_fastapi_server main.py

if [ $? -ne 0 ]; then
    echo "Error occurred during the build process."
    exit 1
fi

echo "Build complete. The executable is in the 'dist' folder."
