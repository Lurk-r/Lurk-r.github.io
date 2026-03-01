@echo off
title PixelGun Ban Checker Proxy Server
echo.
echo ========================================
echo   PixelGun Ban Checker - Proxy Server
echo ========================================
echo.
echo Starting proxy server on port 9999...
echo.
echo This proxy bypasses CORS restrictions for the browser-based
echo ban checker. Keep this window open while using the tool.
echo.
echo Press Ctrl+C to stop the server.
echo.
python proxy.py
pause