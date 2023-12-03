@echo off

:: Define variables
set "project_path=%CD%\"
set "env_path=%project_path%zenml_test_env_1"
echo %env_path%
echo "-----------------"

:: Step 1: Run training and testing pipelines in iterations
echo %DATE% %TIME% - Running training and testing pipelines...
start cmd /k "zenml clean -y && cd %project_path% && conda activate %env_path% && python first_pipeline.py"
timeout /t 30 /nobreak

:: Step 2: Run zenml server
echo %DATE% %TIME% - Running ZenML server...
start cmd /k "cd %project_path% && conda activate %env_path% && zenml up --blocking"
timeout /t 20 /nobreak

:: Step 3: Open a browser at http://127.0.0.1:8237
echo %DATE% %TIME% - Opening browser at http://127.0.0.1:8237...
start http://127.0.0.1:8237

goto :eof
