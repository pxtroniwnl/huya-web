from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir CORS para el frontend

# Configuración
PYTHON_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'python.py')

@app.route('/api/calculate-weather', methods=['POST'])
def calculate_weather():
    """
    Endpoint para calcular datos meteorológicos
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['start_date', 'end_date', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido faltante: {field}'
                }), 400
        
        # Preparar parámetros para el script Python
        params = {
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'latitude': float(data['latitude']),
            'longitude': float(data['longitude'])
        }
        
        # Crear archivo temporal con parámetros
        params_file = os.path.join(os.path.dirname(__file__), 'temp_params.json')
        with open(params_file, 'w') as f:
            json.dump(params, f)
        
        # Ejecutar script Python
        try:
            result = subprocess.run([
                sys.executable, PYTHON_SCRIPT_PATH, params_file
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Leer resultado del archivo JSON
                result_file = os.path.join(os.path.dirname(__file__), 'resultados.json')
                if os.path.exists(result_file):
                    with open(result_file, 'r') as f:
                        weather_data = json.load(f)
                    
                    # Limpiar archivos temporales
                    if os.path.exists(params_file):
                        os.remove(params_file)
                    if os.path.exists(result_file):
                        os.remove(result_file)
                    
                    return jsonify({
                        'success': True,
                        'data': weather_data,
                        'message': 'Datos meteorológicos calculados exitosamente'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'No se generó el archivo de resultados'
                    }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': f'Error en el script Python: {result.stderr}'
                }), 500
                
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': 'Timeout: El cálculo tardó demasiado tiempo'
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error ejecutando Python: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return jsonify({
        'status': 'OK',
        'message': 'API Flask funcionando correctamente',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test-python', methods=['GET'])
def test_python():
    """
    Endpoint para probar la conexión con Python
    """
    try:
        # Crear parámetros de prueba
        test_params = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-02',
            'latitude': 4.6097,
            'longitude': -74.0817
        }
        
        params_file = os.path.join(os.path.dirname(__file__), 'test_params.json')
        with open(params_file, 'w') as f:
            json.dump(test_params, f)
        
        # Ejecutar script Python
        result = subprocess.run([
            sys.executable, PYTHON_SCRIPT_PATH, params_file
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Conexión con Python exitosa',
                'python_output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error en Python: {result.stderr}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error probando Python: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando API Flask...")
    print(f"📁 Script Python: {PYTHON_SCRIPT_PATH}")
    print("🌐 API disponible en: http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   - POST /api/calculate-weather")
    print("   - GET /api/health")
    print("   - GET /api/test-python")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
