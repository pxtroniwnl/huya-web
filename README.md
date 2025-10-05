<p align="center">
  <img src="images/logo-huya.png" alt="Huya Weather logo" width="180" />
</p>

<div align="center">

# Huya Weather

Una plataforma web para exploración y descarga de datos meteorológicos con mapa interactivo y visualizaciones de series de tiempo. UI moderna en tema oscuro, responsiva y lista para integrarse con un backend productivo.

</div>

---

## 1) Visión general

Huya Weather ofrece un flujo completo para que un usuario seleccione ubicación y rango temporal, visualice métricas meteorológicas clave como series de tiempo y descargue los datos en formatos abiertos. El proyecto se ha diseñado con foco en experiencia de usuario, claridad visual y extensibilidad técnica.

> Nota: En esta versión de demostración, los datos se generan de forma simulada en el frontend para permitir una navegación fluida sin dependencias externas. La arquitectura está preparada para conectarse a APIs/servicios reales.

## 2) Características principales

- Mapa interactivo (Leaflet) para seleccionar coordenadas de interés.
- Visualizaciones con Chart.js (líneas suavizadas, leyenda, tooltips, escalas legibles).
- Variables soportadas: Precipitation (%), Humidity (%), Pressure (hPa), Wind (km/h), Temperature (°C).
- Descarga de datos en CSV, JSON o Excel desde la página dedicada.
- Tema oscuro consistente, animaciones sutiles y estados de carga/errores.
- Interfaz en inglés para audiencias internacionales (i18n baseline).

## 3) Estructura del proyecto

```
huya-web/
├── pages/
│   ├── index.html       # Dashboard (mapa + series de tiempo)
│   ├── download.html    # Descarga de datos (variables, formato, mapa)
│   └── about.html       # Nuestro equipo
├── js/
│   ├── script.js        # Lógica del dashboard y gráficos
│   ├── download.js      # Lógica de descargas y selección de ubicación
│   └── about.js         # Interacciones de la sección About
├── styles/
│   ├── styles.css       # Estilos globales (tema oscuro, componentes)
│   ├── download-styles.css
│   └── about-styles.css
├── images/              # Recursos estáticos (logo, fotos, etc.)
└── backend/             # Prototipos/ejemplos para integración futura
```

## 4) Stack técnico

- HTML5, CSS3 (variables, gradientes, animaciones), JavaScript (ES6+)
- Leaflet (mapa interactivo)
- Chart.js (visualizaciones de series de tiempo)
- Font Awesome (iconografía)

## 5) Guía de inicio rápido

1. Clona el repositorio y abre `pages/index.html` en tu navegador.
2. Haz clic en el mapa para fijar una ubicación y define el rango de fechas.
3. Selecciona la variable y pulsa “Generate Chart”.
4. Ve a `pages/download.html` para descargar los datos en el formato deseado.

## 6) Flujo funcional

- Selección de ubicación: Leaflet captura lat/lon a partir de un clic y los expone a los módulos de gráficos/descargas.
- Generación de series: el frontend sintetiza datos con patrones estacionales y ruido controlado para la demo.
- Renderizado: Chart.js configura ejes, leyendas, colores y relleno con un estilo unificado.
- Descarga: se construye un dataset según variables/fechas/ubicación y se exporta a CSV/JSON/Excel.

## 7) Convenciones de código y estilo

- Nombrado claro y explícito (variables y funciones descriptivas).
- Separación de responsabilidades por archivo (`script.js` vs `download.js`).
- Estilos consistentes: tema oscuro, hover/active unificados, escalas legibles.
- Comentarios solo cuando aportan contexto no obvio (mantenibilidad).

## 8) Integración con backend (roadmap)

- Reemplazar generadores locales con un endpoint (e.g., `/api/timeseries`) que reciba: lat, lon, `start_date`, `end_date`, `variables`, `aggregation`.
- Implementar caché por coordenada y ventana temporal para mejorar latencia y costos.
- Añadir pronósticos probabilísticos (cuantiles/intervalos) y métricas de evaluación.
- Seguridad: credenciales/secretos solo en servidor (variables de entorno o gestor de secretos), nunca en el cliente.

## 9) Accesibilidad y UX

- Alto contraste en textos y controles.
- Estados de carga y error claros.
- Layout responsivo (grid/flex) y controles táctiles adecuados.

## 10) Contribución

1. Crea un fork y una rama por feature.
2. Escribe commits descriptivos y enfocados.
3. Abre un Pull Request con contexto (antes/después, capturas si aplica).

## 11) Licencia

Este proyecto está bajo la Licencia MIT. Consulta `LICENSE` para más detalles.

---

Hecho con dedicación por el equipo de Huya Weather.

