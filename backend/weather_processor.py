#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import random
import math
from datetime import datetime, timedelta

def generate_weather_data(latitude, longitude, start_date, end_date):
    """
    Genera datos meteorológicos simulados basados en coordenadas y fechas
    """
    
    # Convertir fechas
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Calcular días de diferencia
    days_diff = (end - start).days + 1
    
    # Factores basados en coordenadas geográficas
    lat_factor = abs(float(latitude)) / 90.0  # 0-1
    lon_factor = (float(longitude) + 180) / 360.0  # 0-1
    
    # Generar datos base
    base_temp = 25 + (lat_factor * 15) - (lat_factor * 20)  # Temperatura base según latitud
    base_humidity = 50 + (lat_factor * 30)  # Humedad base
    base_pressure = 1013 + (lat_factor * 50)  # Presión base
    base_wind = 5 + (lat_factor * 10)  # Viento base
    base_uv = 3 + (lat_factor * 8)  # UV base
    
    # Simular variaciones diarias
    weather_data = []
    
    for i in range(days_diff):
        current_date = start + timedelta(days=i)
        
        # Factores de variación diaria
        day_factor = math.sin((i * 2 * math.pi) / 7)  # Variación semanal
        random_factor = random.uniform(0.8, 1.2)  # Factor aleatorio
        
        # Calcular métricas
        temperature = round(base_temp + (day_factor * 5) + (random_factor - 1) * 10, 1)
        humidity = round(base_humidity + (day_factor * 10) + (random_factor - 1) * 20, 1)
        pressure = round(base_pressure + (day_factor * 20) + (random_factor - 1) * 30, 0)
        wind_speed = round(base_wind + (day_factor * 3) + (random_factor - 1) * 5, 1)
        uv_index = round(base_uv + (day_factor * 2) + (random_factor - 1) * 3, 1)
        
        # Asegurar rangos válidos
        temperature = max(-10, min(45, temperature))
        humidity = max(10, min(100, humidity))
        pressure = max(950, min(1050, pressure))
        wind_speed = max(0, min(50, wind_speed))
        uv_index = max(0, min(15, uv_index))
        
        # Determinar condición del clima
        if temperature > 30 and humidity < 40:
            condition = "Sunny"
        elif temperature > 25 and humidity < 60:
            condition = "Partly Cloudy"
        elif humidity > 70:
            condition = "Cloudy"
        elif temperature < 15:
            condition = "Overcast"
        else:
            condition = "Cloudy & Sunny"
        
        # Calcular calidad del aire (AQI)
        aqi = calculate_aqi(pressure, humidity, wind_speed, uv_index)
        
        day_data = {
            'date': current_date.strftime('%Y-%m-%d'),
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'uv_index': uv_index,
            'air_quality': aqi,
            'condition': condition,
            'coordinates': {
                'latitude': float(latitude),
                'longitude': float(longitude)
            }
        }
        
        weather_data.append(day_data)
    
    # Calcular promedio para mostrar en la tarjeta principal
    avg_temp = round(sum(day['temperature'] for day in weather_data) / len(weather_data), 1)
    avg_humidity = round(sum(day['humidity'] for day in weather_data) / len(weather_data), 1)
    avg_pressure = round(sum(day['pressure'] for day in weather_data) / len(weather_data), 0)
    avg_wind = round(sum(day['wind_speed'] for day in weather_data) / len(weather_data), 1)
    avg_uv = round(sum(day['uv_index'] for day in weather_data) / len(weather_data), 1)
    avg_aqi = round(sum(day['air_quality'] for day in weather_data) / len(weather_data), 0)
    
    # Condición más frecuente
    conditions = [day['condition'] for day in weather_data]
    most_common_condition = max(set(conditions), key=conditions.count)
    
    return {
        'current_weather': {
            'temperature': avg_temp,
            'condition': most_common_condition,
            'humidity': avg_humidity,
            'pressure': avg_pressure,
            'wind_speed': avg_wind,
            'uv_index': avg_uv,
            'air_quality': avg_aqi
        },
        'forecast': weather_data,
        'location': {
            'latitude': float(latitude),
            'longitude': float(longitude)
        },
        'date_range': {
            'start': start_date,
            'end': end_date
        }
    }

def calculate_aqi(pressure, humidity, wind_speed, uv_index):
    """
    Calcula un índice de calidad del aire simplificado
    """
    # Factores que afectan la calidad del aire
    pressure_factor = max(0, (1013 - pressure) / 100)  # Presión baja = peor calidad
    humidity_factor = max(0, (humidity - 50) / 50)  # Humedad alta = peor calidad
    wind_factor = max(0, (10 - wind_speed) / 10)  # Viento bajo = peor calidad
    uv_factor = uv_index / 15  # UV alto = peor calidad
    
    # Calcular AQI (0-100)
    aqi = 20 + (pressure_factor * 20) + (humidity_factor * 15) + (wind_factor * 25) + (uv_factor * 20)
    
    return max(0, min(100, round(aqi)))

def main():
    if len(sys.argv) != 5:
        print(json.dumps({'error': 'Número incorrecto de argumentos'}))
        sys.exit(1)
    
    try:
        latitude = sys.argv[1]
        longitude = sys.argv[2]
        start_date = sys.argv[3]
        end_date = sys.argv[4]
        
        # Validar coordenadas
        lat = float(latitude)
        lon = float(longitude)
        
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            print(json.dumps({'error': 'Coordenadas inválidas'}))
            sys.exit(1)
        
        # Generar datos meteorológicos
        weather_data = generate_weather_data(latitude, longitude, start_date, end_date)
        
        # Imprimir resultado como JSON
        print(json.dumps(weather_data, ensure_ascii=False, indent=2))
        
    except ValueError as e:
        print(json.dumps({'error': f'Error de formato: {str(e)}'}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': f'Error interno: {str(e)}'}))
        sys.exit(1)

if __name__ == '__main__':
    main()
