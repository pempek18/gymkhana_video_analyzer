@echo off
echo ========================================
echo Gymkhana Video Analyzer - Local Build
echo ========================================
echo.

echo Using existing icon: img/pacholek.ico
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
python build_exe.py

echo.
echo Build complete! Check the 'dist' folder.
echo.
echo Files created:
echo - GymkhanaVideoAnalyzer.exe
echo - GymkhanaVideoAnalyzer-Windows.zip
echo.
echo Press any key to test the executable...
pause >nul

echo.
echo Testing executable...
if exist "dist\GymkhanaVideoAnalyzer.exe" (
    echo Starting application...
    start "" "dist\GymkhanaVideoAnalyzer.exe"
) else (
    echo Error: Executable not found in dist folder!
)

echo.
echo Build process completed!
pause
