@echo off
title Django Sunucu
echo ========================================
echo    Ogrenci Performans Tahmincisi Server
echo ========================================
echo.
echo Django sunucusu baslatiliyor...
echo URL: http://127.0.0.1:8000/
echo.
echo Sunucuyu durdurmak icin Ctrl+C basin
echo ========================================
echo.
python manage.py runserver 127.0.0.1:8000 