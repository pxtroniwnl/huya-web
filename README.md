<p align="center">
  <img src="images/logo-huya.png" alt="Huya Weather logo" width="180" />
</p>

# Huya Weather

Dashboard meteorológico con mapa interactivo, series de tiempo y descarga de datos (CSV/JSON/Excel). UI moderna en tema oscuro, responsiva y lista para conectar a un backend real.

Páginas clave: `pages/index.html` (dashboard), `pages/download.html` (descargas), `pages/about.html` (equipo).

> ⚠️ Importante: Los datos actuales son simulados para demo educativa.

## Características

- Diseño oscuro moderno, responsive y con animaciones
- Mapa interactivo (Leaflet) y visualización (Chart.js)
- Variables: Precipitation %, Humidity %, Pressure (hPa), Wind (km/h), Temperature (°C)
- Descarga en CSV/JSON/Excel

## Tecnologías

- Frontend: HTML, CSS (variables/animaciones), JavaScript (ES6+)
- Visualización: Chart.js
- Mapas: Leaflet
- Iconos: Font Awesome

## Estructura del Proyecto

```
huya-web/
├── pages/               # index (dashboard), download, about
├── js/                  # script.js (dashboard), download.js
├── styles/              # styles.css base + específicos
├── images/              # assets (incluye logo)
└── backend/             # prototipos y utilidades
```

## Uso Rápido

1) Abrir `pages/index.html` en el navegador
2) Seleccionar ubicaciones/fechas y generar la serie
3) Ir a `pages/download.html` para descargar datos

## Licencia

MIT. Ver `LICENSE`.

---

Huya Weather — desarrollado con ❤️ para demostración y aprendizaje.

