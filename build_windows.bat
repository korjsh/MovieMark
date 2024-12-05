@echo off
echo Building executable for Windows...

pyinstaller --onefile --hidden-import=passlib.handlers.bcrypt --name my_fastapi_server --add-data ".env;." main.py

if %ERRORLEVEL% NEQ 0 (
    echo Error occurred during the build process.
    exit /b %ERRORLEVEL%
)

echo Build complete. The executable is in the "dist" folder.
pause
