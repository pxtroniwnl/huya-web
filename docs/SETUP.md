# Configuración del Servidor - Huya Weather

## Requisitos del Sistema

### Servidor Web
- **Apache** con mod_rewrite habilitado
- **PHP 7.4+** con extensiones:
  - json
  - curl (opcional, para futuras mejoras)
- **Python 3.6+** con módulos:
  - json (incluido por defecto)
  - math (incluido por defecto)
  - random (incluido por defecto)
  - datetime (incluido por defecto)

## Instalación

### 1. Configurar Apache
Asegúrate de que mod_rewrite esté habilitado:
```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

### 2. Configurar PHP
Verifica que PHP esté instalado y funcionando:
```bash
php -v
```

### 3. Configurar Python
Verifica que Python esté instalado:
```bash
python3 --version
```

### 4. Permisos de Archivos
Asegúrate de que los archivos tengan los permisos correctos:
```bash
chmod +x weather_processor.py
chmod 644 *.php *.html *.css *.js
chmod 644 .htaccess
```

### 5. Configurar CORS (si es necesario)
Si tienes problemas con CORS, puedes modificar el archivo `.htaccess` o agregar estas líneas a tu configuración de Apache:
```apache
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
```

## Estructura del Proyecto

```
huya-web/
├── index.html              # Página principal
├── styles.css              # Estilos CSS
├── script.js               # JavaScript del frontend
├── calculate_weather.php   # Backend PHP
├── weather_processor.py    # Script Python para procesamiento
├── .htaccess              # Configuración de Apache
├── images/
│   └── logo-huya.png      # Logo de Huya
├── README.md              # Documentación principal
└── SETUP.md               # Este archivo
```

## Uso

1. **Coloca todos los archivos** en el directorio de tu servidor web (ej: `/var/www/html/huya-web/`)

2. **Abre tu navegador** y ve a `http://localhost/huya-web/` (o tu dominio)

3. **Selecciona fechas** en los campos de fecha

4. **Haz clic en el mapa** para seleccionar una ubicación

5. **Presiona "Calculate"** para obtener datos meteorológicos

## Solución de Problemas

### Error: "Método no permitido"
- Verifica que mod_rewrite esté habilitado en Apache
- Revisa que el archivo `.htaccess` esté presente

### Error: "Error al ejecutar el script de Python"
- Verifica que Python esté instalado y en el PATH
- Asegúrate de que el archivo `weather_processor.py` tenga permisos de ejecución
- Revisa los logs de error de Apache

### Error de CORS
- Verifica la configuración de CORS en `.htaccess`
- Asegúrate de que las cabeceras estén configuradas correctamente

### El mapa no se carga
- Verifica tu conexión a internet (Leaflet requiere conexión)
- Revisa la consola del navegador para errores de JavaScript

## Personalización

### Modificar el Script Python
Puedes editar `weather_processor.py` para:
- Cambiar los algoritmos de cálculo
- Agregar más métricas meteorológicas
- Integrar con APIs reales de clima

### Modificar el Backend PHP
Puedes editar `calculate_weather.php` para:
- Agregar validaciones adicionales
- Implementar autenticación
- Agregar logging

### Modificar el Frontend
Puedes editar `script.js` y `styles.css` para:
- Cambiar la interfaz de usuario
- Agregar más funcionalidades
- Mejorar las animaciones

## Soporte

Para soporte técnico o reportar bugs, contacta al equipo de desarrollo.

---

**Huya Weather** - Dashboard Meteorológico de Predicción


