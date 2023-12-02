@echo off

:: Define variables
set "project_path=%~dp0"
set "env_path=%project_path%zenml_test_env_1"

:: Step 1: Open and run code 1 in a new cmd window
start cmd /k "cd %project_path% && conda activate %env_path% && python app.py"
timeout /t 20 /nobreak

:: Step 2: Open and run code 2 in a new cmd window
start cmd /k "cd %project_path% && conda activate %env_path% && zenml up --blocking"
timeout /t 20 /nobreak

:: Step 3: Open a browser at http://127.0.0.1:8237
start http://127.0.0.1:8237
