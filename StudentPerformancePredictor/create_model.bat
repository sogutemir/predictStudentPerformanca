@echo off
title Model Olusturucu
echo ========================================
echo    Ogrenci Performans Modeli Olusturucu
echo ========================================
echo.
echo Model olusturuluyor...
python create_model.py
echo.
if %ERRORLEVEL% EQU 0 (
    echo [BASARILI] Model basariyla olusturuldu!
) else (
    echo [HATA] Model olusturulurken bir hata olustu.
)
echo.
echo Devam etmek icin herhangi bir tusa basin...
pause > nul 