@echo off
REM Copy all EML sample files to Downloads folder

echo.
echo Copying PhishGuard Sample EML Files...
echo.

set source=E:\projectpcr\samples
set destination=%USERPROFILE%\Downloads\PhishGuard_Samples

REM Create destination folder
if not exist "%destination%" mkdir "%destination%"

REM Copy all EML files
copy "%source%\*.eml" "%destination%" /Y

echo.
echo Done! Files copied to:
echo %destination%
echo.
echo Sample files:
dir "%destination%\*.eml" /B
echo.
pause
