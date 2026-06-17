import os
import json
import logging
from datetime import datetime

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from python import run_prediction

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(PROJECT_ROOT, 'pages')
JS_DIR = os.path.join(PROJECT_ROOT, 'js')
STYLES_DIR = os.path.join(PROJECT_ROOT, 'styles')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'images')

RESULTADOS_FILE = os.path.join(BACKEND_DIR, 'resultados.json')


def determine_condition(medias):
    precip = medias.get('Precipitacion (%)', 0)
    temp = medias.get('Temperatura (°C)', 25)
    humidity = medias.get('Humedad (%)', 50)

    if precip > 70:
        return 'Rainy'
    if temp > 30 and humidity < 40:
        return 'Sunny'
    if temp > 25 and humidity < 60:
        return 'Partly Cloudy'
    if humidity > 70:
        return 'Cloudy'
    if temp < 15:
        return 'Overcast'
    return 'Cloudy & Sunny'


@app.route('/api/calculate-weather', methods=['POST'])
def calculate_weather():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Cuerpo JSON requerido'}), 400

    logger.info('Solicitud calculo desde %s,%s (%s a %s)',
                data.get('latitude'), data.get('longitude'),
                data.get('start_date'), data.get('end_date'))

    required_fields = ['start_date', 'end_date', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Campo requerido faltante: {field}'
            }), 400

    try:
        weather_data = run_prediction(
            float(data['latitude']),
            float(data['longitude']),
            data['start_date'],
            data['end_date']
        )

        weather_data['error'] = False

        with open(RESULTADOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)

        medias = weather_data.get('medias', {})
        condition = determine_condition(medias)

        return jsonify({
            'success': True,
            'data': {
                'current_weather': {
                    'temperature': medias.get('Temperatura (°C)', 0),
                    'condition': condition,
                    'humidity': medias.get('Humedad (%)', 0),
                    'pressure': medias.get('PresionAtm (hPa)', 1013),
                    'wind_speed': medias.get('Viento (km/h)', 0),
                    'precipitation': medias.get('Precipitacion (%)', 0)
                },
                'location': {
                    'latitude': float(data['latitude']),
                    'longitude': float(data['longitude'])
                },
                'date_range': {
                    'start': data['start_date'],
                    'end': data['end_date']
                },
                'time_series': weather_data.get('datos', [])
            },
            'message': 'Calculo completado exitosamente'
        })

    except Exception as e:
        logger.error('Error en calculo: %s', str(e))
        return jsonify({
            'success': False,
            'error': f'Error en calculo: {str(e)}'
        }), 500


@app.route('/api/resultados', methods=['GET'])
def get_resultados():
    if os.path.exists(RESULTADOS_FILE):
        with open(RESULTADOS_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'No hay resultados disponibles'}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API Flask funcionando correctamente',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/')
def serve_index():
    return send_from_directory(PAGES_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    if filename.startswith('js/'):
        return send_from_directory(JS_DIR, filename[3:])
    if filename.startswith('styles/'):
        return send_from_directory(STYLES_DIR, filename[7:])
    if filename.startswith('images/'):
        return send_from_directory(IMAGES_DIR, filename[7:])
    if filename.endswith('.html'):
        return send_from_directory(PAGES_DIR, filename)
    return send_from_directory(PROJECT_ROOT, filename)


if __name__ == '__main__':
    from python import run_prediction
    print("Iniciando API Flask...")
    logger.info("Iniciando servidor Flask")
    print("API disponible en: http://localhost:5000")
    print("Logs: " + LOG_FILE)
    print("Endpoints:")
    print("   POST /api/calculate-weather")
    print("   GET /api/resultados")
    print("   GET /api/health")
    print("   GET / (Frontend)")
    print("Presione Ctrl+C para detener el servidor")

    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except OSError as e:
        logger.error("Error al iniciar servidor: %s", str(e))
        print(f"\nError: No se pudo iniciar el servidor en el puerto 5000.")
        print(f"Posible causa: {e}")
        print("Pruebe: (1) Cerrar otros procesos en el puerto 5000")
        print("       (2) Usar un puerto diferente editando app.py")
