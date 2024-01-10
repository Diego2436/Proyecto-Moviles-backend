# Foodtruck-Zacatengo-Movil-Backend
Backend foodtruck movil zacatenco para app movil
- Desarrollado en Django


# Como Correr el backend en modo local

## Requisitos Previos
- Instalar Python >= 3.12.1 
    - Descarga Python: https://www.python.org/downloads/
  <br>
- Instalar virtualenv >= 20.25.0 [Para usar entornos virtuales en python]
    - Ejecuta el siguiente comando en una terminal para instalarlo: **pip install virtualenv**
  <br>
- Instalar MySQL Workbench >= 8.0
    - Descarga MySQL Workbench: https://dev.mysql.com/downloads/workbench/


## Correr en Local Host
- Clonar este repositorio en tu PC
    - Usando Git: **git clone https://github.com/osvid98/Foodtruck-Zacatenco-Movil-Backend.git**
    - Puedes usar Github Desktop si lo tuyo no son los comandos: https://desktop.github.com
  <br>
- Crea una nueva base de datos en MySQL con el nombre "db_foodtruck" y usarla
   - Para mayor facilidad correr el script "db_foodtruck.sql" en Workbench que se encuentra en la carpeta "BD"
  <br>
- En el directorio backend-django/Proyecto_API/Proyecto_API/settings.py configurar tu localhost y password de tu SQL
    - En la linea 77 "DATABASES" configurar tu localhost  y password de tu SQL segun tus necesidades.
  <br>
- Posicionate en la carpeta "backend-django" en una terminal
    - Usar: **cd .\backend-django**
  <br>
- Ejecutar "activate" de la carpeta env/Scripts para activar el entorno virtual de python
   - Ejecuta: **.\env\Scripts\activate**
  <br>
- Posicionate en la carpeta en la carpeta "Proyecto_API"
   - Usar: **cd .\Proyecto_API** 
  <br>
- Ejecutar las migraciones de los modelos de Django a la Base de Datos
   - Usar: **python manage.py migrate**   
  <br>
- Ejecutar el servidor local
   - Usar: **python manage.py runserver**
   - Entra en modo local en tu navegador (comunmente es http://127.0.0.1:8000/)

