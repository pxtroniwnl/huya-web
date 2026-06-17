document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
    setDefaultDates();
});

function initializeMap() {
    const map = L.map('map').setView([-35.0, -65.0], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Leaflet | © OpenStreetMap contributors | CARTO',
        maxZoom: 18,
        className: 'custom-tile'
    }).addTo(map);

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

        window.selectedLocation = { lat: lat, lng: lng };

        if (currentMarker) {
            map.removeLayer(currentMarker);
        }

        currentMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'custom-marker',
                html: '<div class="marker-pin"></div>',
                iconSize: [20, 20],
                iconAnchor: [10, 20]
            })
        }).addTo(map);

        updateLocationInfo(lat, lng);
    });

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

function setupEventListeners() {
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.addEventListener('click', downloadData);

    const backBtn = document.querySelector('.back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'index.html';
        });
    }

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

    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');

    startDate.addEventListener('change', validateDates);
    endDate.addEventListener('change', validateDates);
}

function setDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');

    startDate.value = today.toISOString().split('T')[0];
    endDate.value = tomorrow.toISOString().split('T')[0];
}

function validateDates() {
    const startDate = new Date(document.getElementById('start-date').value);
    const endDate = new Date(document.getElementById('end-date').value);

    if (startDate > endDate) {
        showNotification('Start date cannot be later than end date', 'error');
        document.getElementById('end-date').value = document.getElementById('start-date').value;
    }
}

function updateLocationInfo(lat, lng) {
    const locationInfo = document.getElementById('locationInfo');
    locationInfo.innerHTML = `
        <i class="fas fa-map-marker-alt"></i>
        <span>Selected location: ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
    `;
}

async function downloadData() {
    if (!window.selectedLocation) {
        showNotification('Please select a location on the map', 'error');
        return;
    }

    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    if (!startDate || !endDate) {
        showNotification('Please select both dates', 'error');
        return;
    }

    const selectedVariables = getSelectedVariables();
    if (selectedVariables.length === 0) {
        showNotification('Please select at least one variable', 'error');
        return;
    }

    const format = document.querySelector('input[name="format"]:checked').value;

    const downloadBtn = document.getElementById('downloadBtn');
    const originalText = downloadBtn.innerHTML;

    downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Fetching data from NASA POWER...';
    downloadBtn.disabled = true;
    downloadBtn.classList.add('loading');

    try {
        const weatherData = await fetchWeatherData(
            window.selectedLocation.lat,
            window.selectedLocation.lng,
            startDate,
            endDate,
            selectedVariables
        );

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

function getSelectedVariables() {
    const checkboxes = document.querySelectorAll('.variable-item input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => ({
        id: cb.id,
        name: cb.nextElementSibling.textContent.trim()
    }));
}

const VAR_MAP = {
    'temperature': { key: 'Temperatura (°C)', label: 'Temperature (C)' },
    'humidity': { key: 'Humedad (%)', label: 'Humidity (%)' },
    'pressure': { key: 'PresionAtm (hPa)', label: 'Pressure (hPa)' },
    'wind-speed': { key: 'Viento (km/h)', label: 'Wind Speed (km/h)' },
    'precipitation': { key: 'Precipitacion (%)', label: 'Precipitation (%)' }
};

async function fetchWeatherData(lat, lng, startDate, endDate, variables) {
    const response = await fetch('/api/calculate-weather', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            latitude: lat,
            longitude: lng,
            start_date: startDate,
            end_date: endDate
        })
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || `Server error: ${response.status}`);
    }

    const result = await response.json();
    if (!result.success) {
        throw new Error(result.error || 'Error processing weather data');
    }

    const timeSeries = result.data.time_series || [];
    if (timeSeries.length === 0) {
        throw new Error('No data returned for the selected range');
    }

    const selectedMaps = variables
        .map(v => VAR_MAP[v.id])
        .filter(Boolean);

    return timeSeries.map((record, idx) => {
        const row = { '#': idx + 1, Date: record.Fecha };
        selectedMaps.forEach(m => {
            row[m.label] = record[m.key] !== undefined ? record[m.key] : '';
        });
        return row;
    });
}

function s2ab(s) {
    const buf = new ArrayBuffer(s.length);
    const view = new Uint8Array(buf);
    for (let i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
    return buf;
}

function downloadFile(data, format, startDate, endDate) {
    const ext = format === 'excel' ? 'xlsx' : format;
    const filename = `huya_weather_${startDate}_to_${endDate}.${ext}`;
    let blob;

    switch (format) {
        case 'csv':
            blob = new Blob(['\uFEFF' + convertToCSV(data)], { type: 'text/csv;charset=utf-8' });
            break;
        case 'json':
            blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' });
            break;
        case 'excel': {
            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.json_to_sheet(data);
            XLSX.utils.book_append_sheet(wb, ws, 'Weather Data');
            const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });
            blob = new Blob([s2ab(wbout)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            break;
        }
        default:
            throw new Error('Unsupported format');
    }

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    if (data.length === 0) return '';
    const headers = Object.keys(data[0]);
    const escape = v => {
        const s = String(v ?? '');
        return s.includes(',') || s.includes('"') || s.includes('\n') ? '"' + s.replace(/"/g, '""') + '"' : s;
    };
    return [
        headers.join(','),
        ...data.map(row => headers.map(h => escape(row[h])).join(','))
    ].join('\n');
}

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
