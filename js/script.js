// Inicializar el mapa cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
});

// Inicializar el mapa de Leaflet
function initializeMap() {
    // Coordenadas centradas en Sudamérica (Chile, Argentina, Uruguay)
    const map = L.map('map').setView([-35.0, -65.0], 4);
    
    // Almacenar instancia globalmente
    window.mapInstance = map;
    
    // Agregar capa de tiles de OpenStreetMap con estilo personalizado
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Leaflet | © OpenStreetMap contributors | CARTO',
        maxZoom: 18,
        className: 'custom-tile'
    }).addTo(map);
    
    // Aplicar filtro de escala de grises al mapa
    const style = document.createElement('style');
    style.textContent = `
        .custom-tile {
            filter: grayscale(100%) contrast(1.2);
        }
    `;
    document.head.appendChild(style);
    
    // Variable para almacenar el marcador actual
    let currentMarker = null;
    
    // Agregar evento de clic en el mapa para colocar marcador
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Almacenar coordenadas del último clic
        map._lastClick = { lat: lat, lng: lng };
        
        // Remover marcador anterior si existe
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
        
        // Actualizar la información de ubicación
        updateLocationInfo(lat, lng);
        
        // Actualizar las coordenadas en la tarjeta de clima actual
        updateWeatherLocation(lat, lng);
    });
    
    // Estilo personalizado para el marcador
    const markerStyle = document.createElement('style');
    markerStyle.textContent = `
        .custom-marker {
            background: transparent;
            border: none;
        }
        .marker-pin {
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, #0066CC, #00A8FF);
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            border: 3px solid white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
    `;
    document.head.appendChild(markerStyle);
}

// Configurar event listeners
function setupEventListeners() {
    // Botón Calculate
    const calculateBtn = document.querySelector('.calculate-btn');
    calculateBtn.addEventListener('click', function() {
        calculateWeather();
    });
    
    // Botón del dashboard en el sidebar
    const dashboardIcon = document.querySelector('.sidebar-icon:nth-child(1)');
    if (dashboardIcon) {
        dashboardIcon.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
    
    // Botón de descarga en el sidebar
    const downloadIcon = document.querySelector('.sidebar-icon:nth-child(2)');
    if (downloadIcon) {
        downloadIcon.addEventListener('click', function() {
            window.location.href = 'download.html';
        });
    }
    
    // Botón de sobre nosotros en el sidebar
    const aboutIcon = document.querySelector('.sidebar-icon:nth-child(3)');
    if (aboutIcon) {
        aboutIcon.addEventListener('click', function() {
            window.location.href = 'about.html';
        });
    }
    
    // Cambios en las fechas
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    startDate.addEventListener('change', function() {
        validateDateRange();
    });
    
    endDate.addEventListener('change', function() {
        validateDateRange();
    });
    
    // Cambios en las unidades de las métricas
    const unitSelects = document.querySelectorAll('.metric-unit select');
    unitSelects.forEach(select => {
        select.addEventListener('change', function() {
            convertMetric(this);
        });
    });
}

// Actualizar información de ubicación
function updateLocationInfo(lat, lng) {
    const locationText = document.querySelector('.location-text');
    
    // Obtener nombre de la ciudad usando geocodificación inversa
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.display_name) {
                const cityName = data.display_name.split(',')[0];
                locationText.textContent = cityName;
            } else {
                locationText.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
            }
        })
        .catch(error => {
            console.error('Error al obtener nombre de la ciudad:', error);
            locationText.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
        });
}

// Actualizar ubicación en la tarjeta de clima
function updateWeatherLocation(lat, lng) {
    const locationInfo = document.querySelector('.location-info span');
    locationInfo.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
}

// Validar rango de fechas
function validateDateRange() {
    const startDate = new Date(document.getElementById('start-date').value);
    const endDate = new Date(document.getElementById('end-date').value);
    
    if (startDate > endDate) {
        alert('Start date cannot be later than end date.');
        document.getElementById('end-date').value = document.getElementById('start-date').value;
    }
}

// Calcular clima usando PHP y Python (con fallback a simulación)
async function calculateWeather() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (!startDate || !endDate) {
        alert('Please select both dates.');
        return;
    }
    
    // Obtener coordenadas del marcador del mapa
    const map = window.mapInstance;
    if (!map || !map._lastClick) {
        alert('Please select a location on the map by clicking.');
        return;
    }
    
    const calculateBtn = document.querySelector('.calculate-btn');
    const originalText = calculateBtn.textContent;
    
    calculateBtn.textContent = 'Calculating...';
    calculateBtn.disabled = true;
    
    try {
        // Preparar datos para enviar
        const requestData = {
            start_date: startDate,
            end_date: endDate,
            latitude: map._lastClick.lat,
            longitude: map._lastClick.lng
        };
        
        // Intentar conectar con PHP primero
        const response = await fetch('../backend/calculate_weather.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (response.ok) {
            const result = await response.json();
            
            if (result.success) {
            // Actualizar la interfaz con los datos reales
            updateWeatherDisplay(result.data);
            showNotification('Calculation completed successfully (Backend)', 'success');
                return;
            } else {
                throw new Error(result.message || 'Error calculating weather');
            }
        } else {
            throw new Error('Server not available');
        }
        
    } catch (error) {
        console.log('Using simulation mode:', error.message);
        
        // Fallback: usar datos simulados
        try {
            const simulatedData = generateSimulatedWeatherData(map._lastClick.lat, map._lastClick.lng, startDate, endDate);
            updateWeatherDisplay(simulatedData);
            showNotification('Calculation completed (Simulation mode)', 'info');
        } catch (simError) {
            console.error('Error in simulation:', simError);
            showNotification('Error calculating weather', 'error');
        }
    } finally {
        calculateBtn.textContent = originalText;
        calculateBtn.disabled = false;
    }
}

// Generar datos meteorológicos simulados (fallback)
function generateSimulatedWeatherData(lat, lng, startDate, endDate) {
    // Calcular días de diferencia
    const start = new Date(startDate);
    const end = new Date(endDate);
    const daysDiff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    
    // Factores basados en coordenadas geográficas
    const latFactor = Math.abs(lat) / 90.0;
    const lonFactor = (lng + 180) / 360.0;
    
    // Generar datos base
    const baseTemp = 25 + (latFactor * 15) - (latFactor * 20);
    const baseHumidity = 50 + (latFactor * 30);
    const basePressure = 1013 + (latFactor * 50);
    const baseWind = 5 + (latFactor * 10);
    const baseUV = 3 + (latFactor * 8);
    
    // Simular variaciones
    const temperature = Math.round((baseTemp + (Math.random() - 0.5) * 10) * 10) / 10;
    const humidity = Math.round((baseHumidity + (Math.random() - 0.5) * 20) * 10) / 10;
    const pressure = Math.round(basePressure + (Math.random() - 0.5) * 30);
    const windSpeed = Math.round((baseWind + (Math.random() - 0.5) * 5) * 10) / 10;
    const uvIndex = Math.round((baseUV + (Math.random() - 0.5) * 3) * 10) / 10;
    const airQuality = Math.round(20 + Math.random() * 50);
    
    // Determinar condición del clima
    let condition = "Cloudy & Sunny";
    if (temperature > 30 && humidity < 40) condition = "Sunny";
    else if (temperature > 25 && humidity < 60) condition = "Partly Cloudy";
    else if (humidity > 70) condition = "Cloudy";
    else if (temperature < 15) condition = "Overcast";
    
    return {
        current_weather: {
            temperature: temperature,
            condition: condition,
            humidity: humidity,
            pressure: pressure,
            wind_speed: windSpeed,
            uv_index: uvIndex,
            air_quality: airQuality
        },
        location: {
            latitude: lat,
            longitude: lng
        },
        date_range: {
            start: startDate,
            end: endDate
        }
    };
}

// Actualizar visualización con datos del backend
function updateWeatherDisplay(data) {
    const currentWeather = data.current_weather;
    
    // Actualizar temperatura
    document.querySelector('.temperature').textContent = `${currentWeather.temperature}°C`;
    
    // Actualizar métricas (en orden: Wind Speed, Humidity, UV, Pressure, Air Quality)
    const metricCards = document.querySelectorAll('.metric-card');
    
    // Wind Speed
    metricCards[0].querySelector('.metric-value').textContent = `${currentWeather.wind_speed} km/h`;
    
    // Humidity
    metricCards[1].querySelector('.metric-value').textContent = `${currentWeather.humidity}%`;
    
    // UV Index
    metricCards[2].querySelector('.metric-value').textContent = `${currentWeather.uv_index} UV`;
    
    // Pressure
    metricCards[3].querySelector('.metric-value').textContent = `${currentWeather.pressure} hPa`;
    
    // Air Quality
    metricCards[4].querySelector('.metric-value').textContent = `${currentWeather.air_quality} AQI`;
    
    // Actualizar condición del clima
    document.querySelector('.weather-condition').textContent = currentWeather.condition;
    
    // Actualizar icono del clima
    updateWeatherIcon(currentWeather.condition);
    
    // Actualizar coordenadas en la tarjeta de clima
    const locationInfo = document.querySelector('.location-info span');
    locationInfo.textContent = `${data.location.latitude.toFixed(4)}, ${data.location.longitude.toFixed(4)}`;
}

// Actualizar icono del clima según la condición
function updateWeatherIcon(condition) {
    const weatherIcon = document.querySelector('.weather-icon i');
    
    switch(condition.toLowerCase()) {
        case 'sunny':
            weatherIcon.className = 'fas fa-sun';
            break;
        case 'cloudy':
            weatherIcon.className = 'fas fa-cloud';
            break;
        case 'partly cloudy':
            weatherIcon.className = 'fas fa-cloud-sun';
            break;
        case 'cloudy & sunny':
            weatherIcon.className = 'fas fa-cloud-sun';
            break;
        case 'overcast':
            weatherIcon.className = 'fas fa-cloud';
            break;
        default:
            weatherIcon.className = 'fas fa-sun';
    }
}

// Convertir métricas según la unidad seleccionada
function convertMetric(selectElement) {
    const metricCard = selectElement.closest('.metric-card');
    const metricValue = metricCard.querySelector('.metric-value');
    const currentValue = parseFloat(metricValue.textContent);
    const selectedUnit = selectElement.value;
    
    // Obtener el tipo de métrica
    const metricLabel = metricCard.querySelector('.metric-label').textContent;
    
    let convertedValue = currentValue;
    
    switch(metricLabel) {
        case 'Wind Speed':
            if (selectedUnit === 'm/s') {
                convertedValue = (currentValue / 3.6).toFixed(1);
            } else if (selectedUnit === 'mph') {
                convertedValue = (currentValue * 0.621371).toFixed(1);
            }
            break;
        case 'Pressure':
            if (selectedUnit === 'atm') {
                convertedValue = (currentValue / 1013.25).toFixed(2);
            } else if (selectedUnit === 'bar') {
                convertedValue = (currentValue / 1000).toFixed(2);
            }
            break;
        case 'UV Radiation':
            if (selectedUnit === 'Index') {
                convertedValue = currentValue.toFixed(1);
            }
            break;
    }
    
    metricValue.textContent = `${convertedValue} ${selectedUnit}`;
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Colores según el tipo
    let bgColor = '#3498DB'; // Azul por defecto
    if (type === 'success') bgColor = '#27AE60'; // Verde
    if (type === 'error') bgColor = '#E74C3C'; // Rojo
    
    // Estilos de la notificación
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
    
    // Agregar animación CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remover notificación después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Efectos de hover para las tarjetas
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.metric-card, .current-weather-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// ===== TIME SERIES CHART FUNCTIONALITY =====
let timeSeriesChart = null;

// Initialize chart functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeChartFunctionality();
});

function initializeChartFunctionality() {
    const generateBtn = document.querySelector('.generate-chart-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateTimeSeriesChart);
    }
}

async function generateTimeSeriesChart() {
    // Check if location is selected
    if (!window.mapInstance || !window.mapInstance._lastClick) {
        showNotification('Please select a location on the map first', 'warning');
        return;
    }

    // Get selected variable and time aggregation
    const selectedVariable = document.querySelector('input[name="chart-variable"]:checked').value;
    const selectedAggregation = document.querySelector('input[name="time-aggregation"]:checked').value;
    
    // Get date range
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (!startDate || !endDate) {
        showNotification('Please select start and end dates', 'warning');
        return;
    }

    // Show loading state
    showChartLoading(true);
    hideChartError();

    try {
        // Generate time series data
        const chartData = await generateTimeSeriesData(
            window.mapInstance._lastClick.lat,
            window.mapInstance._lastClick.lng,
            startDate,
            endDate,
            selectedVariable,
            selectedAggregation
        );

        // Create or update chart
        createTimeSeriesChart(chartData, selectedVariable, selectedAggregation);
        
    } catch (error) {
        console.error('Error generating chart:', error);
        showChartError();
    } finally {
        showChartLoading(false);
    }
}

async function generateTimeSeriesData(lat, lng, startDate, endDate, variable, aggregation) {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Generate realistic time series data based on variable and aggregation
    const start = new Date(startDate);
    const end = new Date(endDate);
    const dataPoints = generateDataPoints(start, end, aggregation);
    
    const labels = dataPoints.map(point => point.date);
    const values = dataPoints.map(point => point.value);
    
    return {
        labels: labels,
        data: values,
        variable: variable,
        aggregation: aggregation,
        location: { lat, lng }
    };
}

function generateDataPoints(startDate, endDate, aggregation) {
    const points = [];
    const current = new Date(startDate);
    
    // Base values for different variables
    const baseValues = {
        temperature: 25,
        humidity: 60,
        wind: 10,
        pressure: 1013,
        uv: 5,
        'air-quality': 50
    };
    
    while (current <= endDate) {
        const dateStr = formatDateForChart(current, aggregation);
        
        // Generate realistic values with seasonal and daily patterns
        const dayOfYear = Math.floor((current - new Date(current.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
        const hour = current.getHours();
        
        // Seasonal variation (simplified)
        const seasonalFactor = 1 + 0.3 * Math.sin((dayOfYear / 365) * 2 * Math.PI);
        
        // Daily variation
        const dailyFactor = 1 + 0.2 * Math.sin((hour / 24) * 2 * Math.PI);
        
        // Random variation
        const randomFactor = 0.8 + Math.random() * 0.4;
        
        // Calculate value based on aggregation
        let value;
        switch (aggregation) {
            case 'daily':
                value = baseValues.temperature * seasonalFactor * dailyFactor * randomFactor;
                break;
            case 'weekly':
                value = baseValues.temperature * seasonalFactor * (0.9 + Math.random() * 0.2);
                break;
            case 'monthly':
                value = baseValues.temperature * seasonalFactor * (0.95 + Math.random() * 0.1);
                break;
            case 'yearly':
                value = baseValues.temperature * seasonalFactor;
                break;
        }
        
        // Adjust value based on variable type
        switch (document.querySelector('input[name="chart-variable"]:checked').value) {
            case 'temperature':
                value = Math.round(value * 10) / 10;
                break;
            case 'humidity':
                value = Math.min(100, Math.max(0, Math.round(value * 0.6)));
                break;
            case 'wind':
                value = Math.round(value * 0.3 * 10) / 10;
                break;
            case 'pressure':
                value = Math.round(1000 + value * 0.1);
                break;
            case 'uv':
                value = Math.min(11, Math.max(0, Math.round(value * 0.2 * 10) / 10));
                break;
            case 'air-quality':
                value = Math.min(500, Math.max(0, Math.round(value * 0.8)));
                break;
        }
        
        points.push({
            date: dateStr,
            value: value
        });
        
        // Move to next period based on aggregation
        switch (aggregation) {
            case 'daily':
                current.setDate(current.getDate() + 1);
                break;
            case 'weekly':
                current.setDate(current.getDate() + 7);
                break;
            case 'monthly':
                current.setMonth(current.getMonth() + 1);
                break;
            case 'yearly':
                current.setFullYear(current.getFullYear() + 1);
                break;
        }
    }
    
    return points;
}

function formatDateForChart(date, aggregation) {
    switch (aggregation) {
        case 'daily':
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        case 'weekly':
            return `Week ${Math.ceil(date.getDate() / 7)} ${date.toLocaleDateString('en-US', { month: 'short' })}`;
        case 'monthly':
            return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
        case 'yearly':
            return date.getFullYear().toString();
    }
}

function createTimeSeriesChart(chartData, variable, aggregation) {
    const ctx = document.getElementById('timeSeriesChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (timeSeriesChart) {
        timeSeriesChart.destroy();
    }
    
    const variableNames = {
        temperature: 'Temperature (°C)',
        humidity: 'Humidity (%)',
        wind: 'Wind Speed (km/h)',
        pressure: 'Pressure (hPa)',
        uv: 'UV Index',
        'air-quality': 'Air Quality (AQI)'
    };
    
    const variableColors = {
        temperature: '#FF6CAB',
        humidity: '#FF6CAB',
        wind: '#FF6CAB',
        pressure: '#FF6CAB',
        uv: '#FF6CAB',
        'air-quality': '#FF6CAB'
    };
    
    timeSeriesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: variableNames[variable],
                data: chartData.data,
                borderColor: variableColors[variable],
                backgroundColor: variableColors[variable] + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: variableColors[variable],
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `${variableNames[variable]} - ${aggregation.charAt(0).toUpperCase() + aggregation.slice(1)} Data`,
                    color: '#FF6CAB',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    labels: {
                        color: '#B0B0B0',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#B0B0B0',
                        maxRotation: 45
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#B0B0B0'
                    },
                    title: {
                        display: true,
                        text: variableNames[variable],
                        color: '#FFD700',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    hoverBackgroundColor: variableColors[variable]
                }
            }
        }
    });
}

function showChartLoading(show) {
    const loading = document.getElementById('chartLoading');
    const chart = document.getElementById('timeSeriesChart');
    
    if (show) {
        loading.style.display = 'flex';
        chart.style.display = 'none';
    } else {
        loading.style.display = 'none';
        chart.style.display = 'block';
    }
}

function showChartError() {
    const error = document.getElementById('chartError');
    const chart = document.getElementById('timeSeriesChart');
    
    error.style.display = 'flex';
    chart.style.display = 'none';
}

function hideChartError() {
    const error = document.getElementById('chartError');
    error.style.display = 'none';
}
