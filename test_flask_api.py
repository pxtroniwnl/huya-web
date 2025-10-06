#!/usr/bin/env python3
"""
Script para probar la API Flask
"""
import requests
import json

def test_flask_api():
    """Probar la API Flask"""
    
    print("🧪 Probando API Flask...")
    print("=" * 50)
    
    # URL base de la API
    base_url = "http://localhost:5000"
    
    # 1. Probar health check
    print("1️⃣ Probando health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Health check: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Health check: Error de conexión - {e}")
        return False
    
    print()
    
    # 2. Probar test-python
    print("2️⃣ Probando conexión con Python...")
    try:
        response = requests.get(f"{base_url}/api/test-python")
        if response.status_code == 200:
            print("✅ Test Python: OK")
            result = response.json()
            print(f"   Mensaje: {result.get('message', 'N/A')}")
        else:
            print(f"❌ Test Python: Error {response.status_code}")
            print(f"   Error: {response.json().get('error', 'N/A')}")
    except Exception as e:
        print(f"❌ Test Python: Error de conexión - {e}")
    
    print()
    
    # 3. Probar calculate-weather
    print("3️⃣ Probando calculate-weather...")
    test_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "latitude": 4.6097,
        "longitude": -74.0817
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/calculate-weather",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Calculate Weather: OK")
            result = response.json()
            print(f"   Success: {result.get('success', False)}")
            print(f"   Message: {result.get('message', 'N/A')}")
            if 'data' in result:
                print(f"   Datos recibidos: {len(result['data'])} elementos")
        else:
            print(f"❌ Calculate Weather: Error {response.status_code}")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'N/A')}")
    except Exception as e:
        print(f"❌ Calculate Weather: Error de conexión - {e}")
    
    print()
    print("=" * 50)
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    test_flask_api()
