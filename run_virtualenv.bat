@echo off
python -m virtualenv venv
echo Creando Entorno Virtual: OK
call .\venv\Scripts\activate
echo Cargado Entorno Virtual: OK
echo Cargado Dependencias, espera un momento.
pip install -r "requirements.txt"
cd .\Proyecto_API
cmd /k
