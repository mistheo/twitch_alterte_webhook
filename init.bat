@echo off
setlocal

REM Chemin vers Python (assurez-vous que Python est installé et accessible dans le PATH système)
set "PYTHON=python"

REM Nom de l'environnement virtuel
set "VENV_NAME=.venv"

REM Création de l'environnement virtuel
%PYTHON% -m venv %VENV_NAME%

REM Activation de l'environnement virtuel
call %VENV_NAME%\Scripts\activate.bat

REM Installation des modules nécessaires
pip install requests
pip install discord_webhook

REM Désactivation de l'environnement virtuel
deactivate

echo Environnement virtuel configuré avec succès.
