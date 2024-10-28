@echo off
setlocal enabledelayedexpansion

:init
echo Initializing project...

:: Create virtual environment
python -m venv env
if !errorlevel! neq 0 goto :error

:: Activate virtual environment and install requirements
call env\Scripts\activate.bat
if !errorlevel! neq 0 goto :error

pip install -r requirements.txt
if !errorlevel! neq 0 goto :error

:: Copy .start.env to .env
copy .start.env .env
if !errorlevel! neq 0 goto :error

:: Install npm packages
cmd /c npm install
if !errorlevel! neq 0 goto :error

:: Initialize git repository
git init
if !errorlevel! neq 0 goto :error

:: Run Django commands
python manage.py migrate
if !errorlevel! neq 0 goto :error

python manage.py makesuperuser
if !errorlevel! neq 0 goto :error

python manage.py generate_tailwind_directories
if !errorlevel! neq 0 goto :error

:: Build tailwind
cmd /c npm run tailwind:build
if !errorlevel! neq 0 goto :error

:: Initial git commit
git add .
if !errorlevel! neq 0 goto :error

git commit -m "Initial commit"
if !errorlevel! neq 0 goto :error

:: Display instructions
echo Run 'start_server.bat' to start the server
echo Run 'start_tailwind_watch.bat' to start tailwind watch
echo Run 'make_migrations.bat' to make migrations
echo Run 'migrate.bat' to migrate

:: Create additional batch files for other commands
echo python manage.py runserver > start_server.bat
echo npm run tailwind:watch > start_tailwind_watch.bat
echo python manage.py makemigrations > make_migrations.bat
echo python manage.py migrate > migrate.bat

echo Initialization completed successfully.
goto :end

:error
echo An error occurred. Exiting...
exit /b 1

:end
pause