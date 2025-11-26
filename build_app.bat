@echo off
echo ====================================
echo     بناء برنامج نظام عمولة المشرفين
echo ====================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] تثبيت PyInstaller...
    pip install pyinstaller
) else (
    echo [1/3] PyInstaller مثبت مسبقاً ✓
)

echo.
echo [2/3] بناء الملف التنفيذي...
pyinstaller main.spec --clean

if %errorlevel% equ 0 (
    echo.
    echo [3/3] تم البناء بنجاح! ✓
    echo.
    echo الملف التنفيذي موجود في: dist\نظام_عمولة_المشرفين.exe
    echo.
    echo ملاحظة: تأكد من نسخ ملف credentials.json إلى مجلد dist
    echo.
    pause
) else (
    echo.
    echo ❌ فشل البناء! يرجى التحقق من الأخطاء أعلاه
    echo.
    pause
)
