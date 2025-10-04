#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Datos Meteorológicos - Huya Weather
Simula la generación de datos meteorológicos para descarga

Autor: Equipo Huya Weather
Fecha: 2025
"""

import sys
import json
import random
import math
from datetime import datetime, timedelta
import argparse

def generate_weather_data(latitude, longitude, start_date, end_date, variables):
    """
    Genera datos meteorológicos simulados basados en coordenadas y fechas
    
    Args:
        latitude (float): Latitud de la ubicación
        longitude (float): Longitud de la ubicación
        start_date (str): Fecha de inicio (YYYY-MM-DD)
        end_date (str): Fecha de fin (YYYY-MM-DD)
        variables (list): Lista de variables a incluir
    
    Returns:
        dict: Datos meteorológicos generados
    """
    
    # Convertir fechas
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Calcular días de diferencia
    days_diff = (end - start).days + 1
    
    # Factores basados en coordenadas geográficas
    lat_factor = abs(latitude) / 90.0  # 0-1
    lon_factor = (longitude + 180) / 360.0  # 0-1
    
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
        seasonal_factor = math.sin((i * 2 * math.pi) / 365)  # Variación estacional
        random_factor = random.uniform(0.8, 1.2)  # Factor aleatorio
        
        # Calcular métricas
        temperature = round(base_temp + (day_factor * 5) + (seasonal_factor * 3) + (random_factor - 1) * 10, 1)
        humidity = round(base_humidity + (day_factor * 10) + (seasonal_factor * 5) + (random_factor - 1) * 20, 1)
        pressure = round(base_pressure + (day_factor * 20) + (seasonal_factor * 10) + (random_factor - 1) * 30, 0)
        wind_speed = round(base_wind + (day_factor * 3) + (seasonal_factor * 2) + (random_factor - 1) * 5, 1)
        uv_index = round(base_uv + (day_factor * 2) + (seasonal_factor * 1) + (random_factor - 1) * 3, 1)
        
        # Asegurar rangos válidos
        temperature = max(-10, min(45, temperature))
        humidity = max(10, min(100, humidity))
        pressure = max(950, min(1050, pressure))
        wind_speed = max(0, min(50, wind_speed))
        uv_index = max(0, min(15, uv_index))
        
        # Calcular calidad del aire (AQI)
        aqi = calculate_aqi(pressure, humidity, wind_speed, uv_index)
        
        day_data = {
            'fecha': current_date.strftime('%Y-%m-%d'),
            'latitud': latitude,
            'longitud': longitude,
            'timestamp': int(current_date.timestamp())
        }
        
        # Agregar variables seleccionadas
        if 'temperature' in variables:
            day_data['temperatura'] = temperature
        if 'humidity' in variables:
            day_data['humedad'] = humidity
        if 'pressure' in variables:
            day_data['presion'] = pressure
        if 'wind-speed' in variables:
            day_data['velocidad_viento'] = wind_speed
        if 'uv-index' in variables:
            day_data['radiacion_uv'] = uv_index
        if 'air-quality' in variables:
            day_data['calidad_aire'] = aqi
        
        weather_data.append(day_data)
    
    return {
        'status': 'success',
        'data': {
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'name': get_location_name(latitude, longitude)
            },
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'variables': variables,
            'weather_data': weather_data
        },
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'processing_time': '1.2s',
            'data_points': len(weather_data),
            'algorithm_version': '1.0.0'
        }
    }

def calculate_aqi(pressure, humidity, wind_speed, uv_index):
    """
    Calcula un índice de calidad del aire simplificado
    
    Args:
        pressure (float): Presión atmosférica
        humidity (float): Humedad relativa
        wind_speed (float): Velocidad del viento
        uv_index (float): Índice UV
    
    Returns:
        int: Índice de calidad del aire (0-100)
    """
    # Factores que afectan la calidad del aire
    pressure_factor = max(0, (1013 - pressure) / 100)  # Presión baja = peor calidad
    humidity_factor = max(0, (humidity - 50) / 50)  # Humedad alta = peor calidad
    wind_factor = max(0, (10 - wind_speed) / 10)  # Viento bajo = peor calidad
    uv_factor = uv_index / 15  # UV alto = peor calidad
    
    # Calcular AQI (0-100)
    aqi = 20 + (pressure_factor * 20) + (humidity_factor * 15) + (wind_factor * 25) + (uv_factor * 20)
    
    return max(0, min(100, round(aqi)))

def get_location_name(latitude, longitude):
    """
    Obtiene el nombre de la ubicación basado en coordenadas
    
    Args:
        latitude (float): Latitud
        longitude (float): Longitud
    
    Returns:
        str: Nombre de la ubicación
    """
    # Simulación de geocodificación inversa
    cities = [
        'Santa Cruz de la Sierra', 'La Paz', 'Cochabamba', 'Sucre', 'Oruro',
        'Potosí', 'Tarija', 'Trinidad', 'Cobija', 'Riberalta'
    ]
    return cities[random.randint(0, len(cities) - 1)]

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description='Generador de datos meteorológicos')
    parser.add_argument('latitude', type=float, help='Latitud de la ubicación')
    parser.add_argument('longitude', type=float, help='Longitud de la ubicación')
    parser.add_argument('start_date', type=str, help='Fecha de inicio (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, help='Fecha de fin (YYYY-MM-DD)')
    parser.add_argument('--variables', type=str, default='temperature,humidity,wind-speed,pressure,uv-index,air-quality',
                       help='Variables separadas por comas')
    
    args = parser.parse_args()
    
    try:
        # Validar coordenadas
        if not (-90 <= args.latitude <= 90) or not (-180 <= args.longitude <= 180):
            print(json.dumps({'error': 'Coordenadas inválidas'}))
            sys.exit(1)
        
        # Procesar variables
        variables = [v.strip() for v in args.variables.split(',')]
        
        # Generar datos meteorológicos
        weather_data = generate_weather_data(
            args.latitude, 
            args.longitude, 
            args.start_date, 
            args.end_date, 
            variables
        )
        
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
