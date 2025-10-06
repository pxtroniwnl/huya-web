# Configuración para XAMPP

## Pasos para configurar el proyecto en XAMPP:

### 1. Instalar XAMPP
- Descargar desde: https://www.apachefriends.org/
- Instalar en C:\xampp\

### 2. Copiar proyecto
- Copiar toda la carpeta `huya-web` a `C:\xampp\htdocs\huya-web`

### 3. Iniciar servicios
- Abrir XAMPP Control Panel
- Iniciar Apache
- Iniciar MySQL (opcional)

### 4. Instalar dependencias de Python
```bash
pip install scikit-learn pandas numpy xarray earthaccess dask h5py
```

### 5. Acceder al proyecto
- Abrir navegador en: http://localhost/huya-web/pages/index.html

### 6. Verificar permisos
- Asegurar que Apache puede ejecutar Python
- Verificar que la carpeta backend tiene permisos de escritura

## Estructura de archivos en XAMPP:
```
C:\xampp\htdocs\huya-web\
├── pages\
│   └── index.html
├── js\
│   └── script.js
├── styles\
│   └── styles.css
├── backend\
│   ├── calculate_weather.php
│   ├── python.py
│   └── resultados.json
└── .htaccess
```
