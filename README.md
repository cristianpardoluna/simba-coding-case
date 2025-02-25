# simba-coding-case
La aplicación se compone de dos capas `backend` y `frontend`

## Requerimientos
Debe existir el archivo `backend/.env` con las siguientes variables para que el cliente OpenAI funcione:
```sh
OPENAI_API_KEY="LLAVE API OPEN AI"
OPENAI_API_ORGANIZATION="ORGANIZACIÓN OPEN AI"
OPENAI_API_PROJECT="PROYECTO OPEN AI"
```

## Instalar dependencias
### Backend
Dentro de la carpeta `backend`
```
pip install -r requirements.txt
```
### Frontend
Dentro de la carpeta `frontend`
```
npm install
```

## Correr servidores de desarrollo
### Backend
Dentro de la carpeta `backend`
```sh
# si es primera vez correr también python3 manage.py migrate
python3 manage.py runserver
```
### Frontend
Dentro de la carpeta `frontend`
```
npm run dev
```
la aplicacion correrá por defecto en `http://localhost:5173/`