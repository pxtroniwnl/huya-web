# 🌤️ Huya Weather - Dashboard Meteorológico

Un dashboard moderno y elegante para **simulación de predicción meteorológica** desarrollado para el NASA SPACE APPS Challenge, en colaboración con la Universidad Tecnológica de Bolivia.

> ⚠️ **IMPORTANTE**: Este proyecto es una **simulación educativa** y de demostración. Los datos meteorológicos mostrados son generados algorítmicamente y no representan información meteorológica real.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [API y Backend](#-api-y-backend)
- [Personalización](#-personalización)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)
- [Equipo](#-equipo)

## ✨ Características

### 🎨 **Interfaz de Usuario**
- **Diseño Moderno**: Interfaz oscura con colores vibrantes de la marca Huya
- **Responsive Design**: Adaptable a dispositivos móviles y tablets
- **Animaciones Suaves**: Efectos CSS y transiciones fluidas
- **Mapa Interactivo**: Selección de ubicación mediante clic en el mapa de Sudamérica
- **Navegación Intuitiva**: Sidebar con navegación entre secciones

### 📊 **Funcionalidades de Simulación Meteorológica**
- **Simulación de Datos**: Generación algorítmica de datos meteorológicos realistas
- **Múltiples Variables**: Temperatura, humedad, velocidad del viento, presión, radiación UV, calidad del aire
- **Selección de Fechas**: Rango personalizable para simulaciones
- **Conversión de Unidades**: Cambio dinámico de unidades de medida
- **Descarga de Datos Simulados**: Exportación en formatos CSV, JSON y Excel
- **Gráficos de Serie Temporal**: Visualización de tendencias simuladas

### 🔧 **Características Técnicas**
- **Simulación Completa**: Sistema de generación de datos meteorológicos simulados
- **Algoritmos Realistas**: Factores estacionales, diarios y geográficos
- **Backend Híbrido**: PHP + Python para procesamiento de simulaciones
- **Fallback Automático**: Funciona completamente offline con datos simulados
- **Validación de Datos**: Verificación de coordenadas y fechas
- **Manejo de Errores**: Notificaciones informativas y recuperación automática

## 🛠️ Tecnologías Utilizadas

### **Frontend**
- **HTML5**: Estructura semántica y accesible
- **CSS3**: Estilos modernos con gradientes, animaciones y variables CSS
- **JavaScript (ES6+)**: Funcionalidad interactiva y asíncrona
- **Leaflet**: Biblioteca de mapas interactivos
- **Font Awesome**: Iconografía moderna

### **Backend**
- **PHP 7.4+**: API REST para comunicación con el frontend
- **Python 3.6+**: Procesamiento de datos meteorológicos
- **Apache**: Servidor web con mod_rewrite

### **APIs y Servicios**
- **OpenStreetMap**: Datos de mapas base
- **Nominatim**: Geocodificación inversa para nombres de ubicaciones

## 🚀 Instalación

### **Requisitos del Sistema**

#### **Servidor Web**
- Apache 2.4+ con mod_rewrite habilitado
- PHP 7.4+ con extensiones: json, curl (opcional)
- Python 3.6+ con módulos estándar

#### **Navegador**
- Chrome 60+, Firefox 55+, Safari 12+, Edge 79+

### **Instalación Paso a Paso**

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/tu-usuario/huya-weather.git
   cd huya-weather
   ```

2. **Configurar Apache**
   ```bash
   sudo a2enmod rewrite
   sudo systemctl restart apache2
   ```

3. **Configurar Permisos**
   ```bash
   chmod +x weather_data_generator.py
   chmod 644 *.php *.html *.css *.js
   chmod 644 .htaccess
   ```

4. **Verificar Instalación**
   ```bash
   php -v
   python3 --version
   ```

5. **Acceder a la Aplicación**
   - Abrir `http://localhost/huya-weather/` en tu navegador
   - O abrir directamente `index.html` para modo sin servidor
   - ⚠️ **Nota**: Los datos mostrados son simulados, no reales

## 📁 Estructura del Proyecto

```
huya-web/
├── 📄 index.html              # Página de redirección principal
├── 📁 pages/                  # Páginas HTML
│   ├── 📄 index.html          # Dashboard principal
│   ├── 📄 download.html       # Página de descarga de datos
│   └── 📄 about.html          # Página "Sobre Nosotros"
├── 📁 styles/                 # Archivos CSS
│   ├── 🎨 styles.css          # Estilos principales
│   ├── 🎨 download-styles.css # Estilos de descarga
│   └── 🎨 about-styles.css    # Estilos "Sobre Nosotros"
├── 📁 js/                     # Archivos JavaScript
│   ├── ⚡ script.js           # JavaScript principal
│   ├── ⚡ download.js         # JavaScript de descarga
│   └── ⚡ about.js            # JavaScript "Sobre Nosotros"
├── 📁 backend/                # Archivos de backend
│   ├── 🐘 calculate_weather.php      # API PHP
│   ├── 🐍 weather_processor.py      # Procesador Python original
│   └── 🐍 weather_data_generator.py # Generador Python mejorado
├── 📁 docs/                   # Documentación
│   ├── 📖 README.md           # Documentación principal
│   └── 📖 SETUP.md            # Guía de configuración
├── ⚙️ .htaccess               # Configuración Apache
└── 📁 images/                 # Recursos multimedia
    ├── 🖼️ logo-huya.png
    ├── 🖼️ katlyn.jpeg
    ├── 🖼️ patron.jpeg
    ├── 🖼️ utb.png
    └── 🖼️ nasa.webp
```

## 🎯 Uso

### **⚠️ Simulación de Datos**

Este proyecto utiliza **datos simulados** generados algorítmicamente para demostrar funcionalidades meteorológicas. Los datos mostrados **NO son reales** y se generan usando:

- **Factores Estacionales**: Variaciones basadas en el día del año
- **Factores Diarios**: Patrones de temperatura y humedad por hora
- **Factores Geográficos**: Influencia de la latitud y longitud
- **Variación Aleatoria**: Para simular la variabilidad natural
- **Rangos Realistas**: Valores dentro de parámetros meteorológicos típicos

### **Dashboard Principal**

1. **Seleccionar Fechas**
   - Elegir fecha de inicio y fin en los selectores
   - El sistema valida automáticamente el rango

2. **Seleccionar Ubicación**
   - Hacer clic en el mapa para colocar un marcador
   - Las coordenadas se actualizan automáticamente

3. **Calcular Predicciones**
   - Presionar el botón "Calculate"
   - Los datos se generan usando algoritmos meteorológicos

4. **Ver Resultados**
   - Temperatura actual y condición del clima
   - Métricas detalladas con iconos coloridos
   - Conversión de unidades en tiempo real

### **Descarga de Datos**

1. **Acceder a la Página**
   - Hacer clic en el icono de descarga del sidebar
   - O navegar directamente a `download.html`

2. **Configurar Parámetros**
   - Seleccionar fechas de inicio y fin
   - Elegir variables meteorológicas deseadas
   - Seleccionar formato de descarga (CSV, JSON, Excel)

3. **Seleccionar Ubicación**
   - Hacer clic en el mapa para elegir ubicación
   - Verificar coordenadas en la información de ubicación

4. **Descargar Datos**
   - Presionar "Descargar Datos"
   - El archivo se genera y descarga automáticamente

### **Página del Equipo**

1. **Navegar a "Sobre Nosotros"**
   - Hacer clic en el icono de usuarios del sidebar
   - O navegar directamente a `about.html`

2. **Explorar el Equipo**
   - Ver información detallada de cada miembro
   - Conocer roles y habilidades especializadas
   - Ver fotos de los miembros del equipo

3. **Conocer Aliados**
   - Universidad Tecnológica de Bolivia
   - NASA SPACE APPS Challenge

## 🔌 API y Backend (Simulación)

### **⚠️ Sistema de Simulación**

El backend está diseñado para **simular** el procesamiento de datos meteorológicos. No se conecta a APIs meteorológicas reales.

### **API PHP (`calculate_weather.php`)**

```php
POST /calculate_weather.php
Content-Type: application/json

{
    "start_date": "2025-01-01",
    "end_date": "2025-01-04",
    "latitude": -17.7833,
    "longitude": -63.1833
}
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "current_weather": {
            "temperature": 28.5,
            "condition": "Sunny",
            "humidity": 65.2,
            "pressure": 1015,
            "wind_speed": 8.3,
            "uv_index": 7.2,
            "air_quality": 45
        },
        "forecast": [...],
        "location": {
            "latitude": -17.7833,
            "longitude": -63.1833
        }
    },
    "message": "Cálculo completado exitosamente"
}
```

### **Script Python (`weather_data_generator.py`) - SIMULACIÓN**

```bash
python3 weather_data_generator.py -17.7833 -63.1833 2025-01-01 2025-01-04 --variables temperature,humidity,wind-speed
```

**⚠️ Características de Simulación:**
- **Algoritmos simulados** meteorológicos realistas
- **Factores geográficos** y estacionales simulados
- **Validación de coordenadas** para entrada
- **Múltiples formatos** de salida simulados
- **Manejo de errores** robusto
- **Datos NO reales** - Solo para demostración

### **🔬 Algoritmos de Simulación**

Los datos meteorológicos se generan usando algoritmos que simulan patrones realistas:

#### **Temperatura**
```javascript
// Factor estacional basado en el día del año
seasonalFactor = 1 + 0.3 * sin((dayOfYear / 365) * 2 * π)

// Factor diario basado en la hora
dailyFactor = 1 + 0.2 * sin((hour / 24) * 2 * π)

// Temperatura final simulada
temperature = baseTemp * seasonalFactor * dailyFactor * randomFactor
```

#### **Humedad**
- Rango: 0-100%
- Patrones diarios inversos a la temperatura
- Variación estacional suave

#### **Velocidad del Viento**
- Rango: 0-50 km/h
- Variación aleatoria controlada
- Patrones geográficos simulados

#### **Presión Atmosférica**
- Rango: 950-1050 hPa
- Variación mínima diaria
- Factores geográficos simulados

### **⚠️ Advertencias y Limitaciones**

#### **Datos Simulados**
- ❌ **NO usar para decisiones meteorológicas reales**
- ❌ **NO representa condiciones meteorológicas actuales**
- ❌ **NO se conecta a servicios meteorológicos reales**
- ✅ **Solo para demostración y aprendizaje**
- ✅ **Algoritmos educativos y realistas**

#### **Propósito del Proyecto**
- 🎓 **Educativo**: Demostrar conceptos de desarrollo web
- 🏆 **Competencia**: NASA SPACE APPS Challenge
- 🎨 **Portfolio**: Mostrar habilidades técnicas
- 🔬 **Investigación**: Algoritmos de simulación meteorológica

## 🎨 Personalización

### **Colores y Tema**

Editar variables CSS en `styles.css`:

```css
:root {
    --huya-blue: #0066CC;           /* Azul principal */
    --huya-light-blue: #00A8FF;     /* Azul claro */
    --huya-dark-blue: #004499;      /* Azul oscuro */
    --huya-accent: #FFD700;         /* Dorado para UV */
    --huya-bg: #0F1419;             /* Fondo principal */
    --huya-card: #1A2332;           /* Fondo de tarjetas */
    --huya-border: #2A3441;         /* Bordes */
}
```

### **Agregar Nuevas Variables**

1. **Actualizar HTML** (`index.html` y `download.html`)
2. **Agregar estilos** en `styles.css`
3. **Implementar lógica** en `script.js` y `download.js`
4. **Actualizar Python** en `weather_data_generator.py`

### **Modificar Algoritmos**

Editar `weather_data_generator.py`:

```python
def calculate_weather_metric(lat, lon, date, base_value):
    # Tu algoritmo personalizado aquí
    return calculated_value
```

## 🤝 Contribuciones

### **Cómo Contribuir**

1. **Fork** el repositorio
2. **Crear** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** un Pull Request

### **Estándares de Código**

- **JavaScript**: ES6+ con comentarios JSDoc
- **CSS**: BEM methodology con variables CSS
- **PHP**: PSR-12 con documentación PHPDoc
- **Python**: PEP 8 con docstrings

### **Reportar Bugs**

Usar el sistema de Issues de GitHub con:
- Descripción detallada del problema
- Pasos para reproducir
- Capturas de pantalla si aplica
- Información del navegador y sistema

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 Huya Weather Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👥 Equipo

### **Liderazgo**
- **👑 Jasen Yukopila** - Lead del Proyecto

### **Backend**
- **🖥️ Leonardo Muñoz** - Desarrollo Backend
- **🗄️ Carlos Toro** - Bases de Datos y Algoritmos

### **UX/UI**
- **🎨 Katlyn Gutierrez** - Diseño UX/UI
- **🖌️ Isabel Buelvas** - Frontend UX/UI

### **Frontend**
- **💻 Alejandro Patron** - Desarrollo Frontend

### **Instituciones Aliadas**
- **🏛️ Universidad Tecnológica de Bolivia**
- **🚀 NASA SPACE APPS Challenge**

## 📞 Contacto

- **Email**: huya.weather@utb.edu.bo
- **GitHub**: [github.com/huya-weather](https://github.com/huya-weather)
- **Website**: [huya-weather.utb.edu.bo](https://huya-weather.utb.edu.bo)

## 🙏 Agradecimientos

- **NASA SPACE APPS** por la oportunidad de participar
- **Universidad Tecnológica de Bolivia** por el apoyo institucional
- **OpenStreetMap** por los datos de mapas
- **Leaflet** por la biblioteca de mapas
- **Font Awesome** por los iconos

---

**Huya Weather** - Dashboard Meteorológico de Predicción  
*Desarrollado con ❤️ para el NASA SPACE APPS Challenge 2025*