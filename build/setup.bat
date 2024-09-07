:: Windows installer
:: Usage: setup.bat

@echo off

set name=Stone Story RPG Save editor
set src=%CD%\..\src

@RD /S /Q build
@RD /S /Q dist

echo "Building"
python -m PyInstaller ^
--noconfirm ^
--onedir ^
--windowed ^
--icon "%src%\images\icon.ico" ^
--name "%name%" ^
--contents-directory "Contents" ^
--add-data "%src%\translations;translations/" ^
--add-data "%src%\fonts;fonts/" ^
--add-data "%src%\images;images/" ^
--add-data "%src%\settings.toml;." ^
"%src%\editor.py"

del "%name%.spec"

echo "Running build"
start /wait "" "%CD%\dist\%name%\%name%.exe"
