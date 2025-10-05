// Inicializar la página de descarga
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
    setDefaultDates();
});

// Inicializar el mapa
function initializeMap() {
    const map = L.map('map').setView([-35.0, -65.0], 4);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Leaflet | © OpenStreetMap contributors | CARTO',
        maxZoom: 18,
        className: 'custom-tile'
    }).addTo(map);
    
    // Aplicar filtro de escala de grises
    const style = document.createElement('style');
    style.textContent = `
        .custom-tile {
            filter: grayscale(100%) contrast(1.2);
        }
    `;
    document.head.appendChild(style);
    
    let currentMarker = null;
    
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Almacenar coordenadas
        window.selectedLocation = { lat: lat, lng: lng };
        
        // Remover marcador anterior
        if (currentMarker) {
            map.removeLayer(currentMarker);
        }
        
        // Crear nuevo marcador
        currentMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'custom-marker',
                html: '<div class="marker-pin"></div>',
                iconSize: [20, 20],
                iconAnchor: [10, 20]
            })
        }).addTo(map);
        
        // Actualizar información de ubicación
        updateLocationInfo(lat, lng);
    });
    
    // Estilo del marcador
    const markerStyle = document.createElement('style');
    markerStyle.textContent = `
        .custom-marker {
            background: transparent;
            border: none;
        }
        .marker-pin {
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, #FF6CAB, #FF4A8A);
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            border: 3px solid white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
    `;
    document.head.appendChild(markerStyle);
    
    window.mapInstance = map;
}

// Configurar event listeners
function setupEventListeners() {
    // Botón de descarga
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.addEventListener('click', downloadData);
    
    // Botón de regreso al dashboard
    const backBtn = document.querySelector('.back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'index.html';
        });
    }
    
    // Navegación del sidebar
    const dashboardIcon = document.querySelector('.sidebar-icon:nth-child(1)');
    const aboutIcon = document.querySelector('.sidebar-icon:nth-child(3)');
    
    if (dashboardIcon) {
        dashboardIcon.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
    
    if (aboutIcon) {
        aboutIcon.addEventListener('click', function() {
            window.location.href = 'about.html';
        });
    }
    
    // Validación de fechas
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    startDate.addEventListener('change', validateDates);
    endDate.addEventListener('change', validateDates);
    
    // Eliminar funcionalidad de "Select All" (no se agrega botón)
}

// Establecer fechas por defecto
function setDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    startDate.value = today.toISOString().split('T')[0];
    endDate.value = tomorrow.toISOString().split('T')[0];
}

// Validar fechas
function validateDates() {
    const startDate = new Date(document.getElementById('start-date').value);
    const endDate = new Date(document.getElementById('end-date').value);
    
    if (startDate > endDate) {
        showNotification('Start date cannot be later than end date', 'error');
        document.getElementById('end-date').value = document.getElementById('start-date').value;
    }
}

// Actualizar información de ubicación
function updateLocationInfo(lat, lng) {
    const locationInfo = document.getElementById('locationInfo');
    locationInfo.innerHTML = `
        <i class="fas fa-map-marker-alt"></i>
        <span>Selected location: ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
    `;
}

// (Función de alternar todas eliminada por requerimiento)

// Descargar datos
async function downloadData() {
    // Validar ubicación
    if (!window.selectedLocation) {
        showNotification('Please select a location on the map', 'error');
        return;
    }
    
    // Validar fechas
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (!startDate || !endDate) {
        showNotification('Please select both dates', 'error');
        return;
    }
    
    // Obtener variables seleccionadas
    const selectedVariables = getSelectedVariables();
    if (selectedVariables.length === 0) {
        showNotification('Please select at least one variable', 'error');
        return;
    }
    
    // Obtener formato seleccionado
    const format = document.querySelector('input[name="format"]:checked').value;
    
    const downloadBtn = document.getElementById('downloadBtn');
    const originalText = downloadBtn.innerHTML;
    
    // Mostrar estado de carga
    downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating data...';
    downloadBtn.disabled = true;
    downloadBtn.classList.add('loading');
    
    try {
        // Generar datos meteorológicos
        const weatherData = await generateWeatherData(
            window.selectedLocation.lat,
            window.selectedLocation.lng,
            startDate,
            endDate,
            selectedVariables
        );
        
        // Descargar archivo
        downloadFile(weatherData, format, startDate, endDate);
        
        showNotification('Data downloaded successfully', 'success');
        
    } catch (error) {
        console.error('Error generating data:', error);
        showNotification('Error generating data: ' + error.message, 'error');
    } finally {
        downloadBtn.innerHTML = originalText;
        downloadBtn.disabled = false;
        downloadBtn.classList.remove('loading');
    }
}

// Obtener variables seleccionadas
function getSelectedVariables() {
    const checkboxes = document.querySelectorAll('.variable-item input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => ({
        id: cb.id,
        name: cb.nextElementSibling.textContent.trim(),
        icon: cb.nextElementSibling.querySelector('i').className
    }));
}

// Simular llamada al archivo Python para generar datos
async function generateWeatherData(lat, lng, startDate, endDate, variables) {
    try {
        // Simular llamada al script Python
        const pythonScript = 'python ../backend/weather_data_generator.py';
        const params = {
            latitude: lat,
            longitude: lng,
            start_date: startDate,
            end_date: endDate,
            variables: variables.map(v => v.id).join(',')
        };
        
        // Simular delay de procesamiento Python
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Generar datos simulados como si vinieran del Python
        const data = await simulatePythonDataGeneration(lat, lng, startDate, endDate, variables);
        
        return data;
        
    } catch (error) {
        console.log('Using local simulated data:', error.message);
        // Fallback a datos locales si falla la simulación Python
        return generateLocalWeatherData(lat, lng, startDate, endDate, variables);
    }
}

// Simular generación de datos desde Python
async function simulatePythonDataGeneration(lat, lng, startDate, endDate, variables) {
    // Simular respuesta del script Python
    const pythonResponse = {
        status: 'success',
        data: {
            location: {
                latitude: lat,
                longitude: lng,
                name: await getLocationName(lat, lng)
            },
            date_range: {
                start: startDate,
                end: endDate
            },
            variables: variables.map(v => v.id),
            weather_data: []
        },
        metadata: {
            generated_at: new Date().toISOString(),
            processing_time: '1.2s',
            data_points: 0
        }
    };
    
    // Calcular días de diferencia
    const start = new Date(startDate);
    const end = new Date(endDate);
    const daysDiff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    
    // Factores basados en coordenadas (simulando algoritmo Python)
    const latFactor = Math.abs(lat) / 90.0;
    const lonFactor = (lng + 180) / 360.0;
    
    // Generar datos base usando algoritmos meteorológicos simulados
    const baseTemp = 25 + (latFactor * 15) - (latFactor * 20);
    const baseHumidity = 50 + (latFactor * 30);
    const basePressure = 1013 + (latFactor * 50);
    const baseWind = 5 + (latFactor * 10);
    const baseUV = 3 + (latFactor * 8);
    
    for (let i = 0; i < daysDiff; i++) {
        const currentDate = new Date(start);
        currentDate.setDate(start.getDate() + i);
        
        // Simular patrones meteorológicos reales
        const dayFactor = Math.sin((i * 2 * Math.PI) / 7);
        const seasonalFactor = Math.sin((i * 2 * Math.PI) / 365);
        const randomFactor = Math.random();
        
        const dayData = {
            fecha: currentDate.toISOString().split('T')[0],
            latitud: lat,
            longitud: lng,
            timestamp: currentDate.getTime()
        };
        
        // Agregar variables seleccionadas con algoritmos meteorológicos
        variables.forEach(variable => {
            switch (variable.id) {
                case 'temperature':
                    dayData.temperatura = Math.round((baseTemp + (dayFactor * 5) + (seasonalFactor * 3) + (randomFactor - 0.5) * 10) * 10) / 10;
                    break;
                case 'humidity':
                    dayData.humedad = Math.round((baseHumidity + (dayFactor * 10) + (seasonalFactor * 5) + (randomFactor - 0.5) * 20) * 10) / 10;
                    break;
                case 'wind-speed':
                    dayData.velocidad_viento = Math.round((baseWind + (dayFactor * 3) + (seasonalFactor * 2) + (randomFactor - 0.5) * 5) * 10) / 10;
                    break;
                case 'pressure':
                    dayData.presion = Math.round(basePressure + (dayFactor * 20) + (seasonalFactor * 10) + (randomFactor - 0.5) * 30);
                    break;
                case 'uv-index':
                    dayData.radiacion_uv = Math.round((baseUV + (dayFactor * 2) + (seasonalFactor * 1) + (randomFactor - 0.5) * 3) * 10) / 10;
                    break;
                case 'air-quality':
                    dayData.calidad_aire = Math.round(20 + randomFactor * 50 + (dayFactor * 10));
                    break;
            }
        });
        
        pythonResponse.data.weather_data.push(dayData);
    }
    
    pythonResponse.metadata.data_points = pythonResponse.data.weather_data.length;
    
    return pythonResponse.data.weather_data;
}

// Obtener nombre de ubicación (simulado)
async function getLocationName(lat, lng) {
    const cities = [
        'Santa Cruz de la Sierra', 'La Paz', 'Cochabamba', 'Sucre', 'Oruro',
        'Potosí', 'Tarija', 'Trinidad', 'Cobija', 'Riberalta'
    ];
    return cities[Math.floor(Math.random() * cities.length)];
}

// Generar datos locales como fallback
function generateLocalWeatherData(lat, lng, startDate, endDate, variables) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const daysDiff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    
    const data = [];
    
    for (let i = 0; i < daysDiff; i++) {
        const currentDate = new Date(start);
        currentDate.setDate(start.getDate() + i);
        
        const dayData = {
            fecha: currentDate.toISOString().split('T')[0],
            latitud: lat,
            longitud: lng
        };
        
        variables.forEach(variable => {
            switch (variable.id) {
                case 'temperature':
                    dayData.temperatura = Math.round((20 + Math.random() * 20) * 10) / 10;
                    break;
                case 'humidity':
                    dayData.humedad = Math.round((40 + Math.random() * 40) * 10) / 10;
                    break;
                case 'wind-speed':
                    dayData.velocidad_viento = Math.round((2 + Math.random() * 15) * 10) / 10;
                    break;
                case 'pressure':
                    dayData.presion = Math.round(1000 + Math.random() * 50);
                    break;
                case 'uv-index':
                    dayData.radiacion_uv = Math.round((1 + Math.random() * 10) * 10) / 10;
                    break;
                case 'air-quality':
                    dayData.calidad_aire = Math.round(20 + Math.random() * 50);
                    break;
            }
        });
        
        data.push(dayData);
    }
    
    return data;
}

// Descargar archivo
function downloadFile(data, format, startDate, endDate) {
    const filename = `huya_weather_${startDate}_to_${endDate}.${format}`;
    
    let content, mimeType;
    
    switch (format) {
        case 'csv':
            content = convertToCSV(data);
            mimeType = 'text/csv';
            break;
        case 'json':
            content = JSON.stringify(data, null, 2);
            mimeType = 'application/json';
            break;
        case 'excel':
            // Para Excel, usaremos CSV con extensión .xlsx
            content = convertToCSV(data);
            mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
            break;
        default:
            throw new Error('Formato no soportado');
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Convertir a CSV
function convertToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => row[header] || '').join(','))
    ].join('\n');
    
    return csvContent;
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    let bgColor = '#3498DB';
    if (type === 'success') bgColor = '#27AE60';
    if (type === 'error') bgColor = '#E74C3C';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 500;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}
