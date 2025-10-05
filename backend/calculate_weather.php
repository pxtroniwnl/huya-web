<?php
header('Content-Type: application/json'); // Respuesta en formato JSON
header('Access-Control-Allow-Origin: *'); // Permitir CORS para cualquier origen (demo)
header('Access-Control-Allow-Methods: POST'); // Solo aceptar método POST
header('Access-Control-Allow-Headers: Content-Type'); // Permitir cabecera Content-Type

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { // Verificar que el método sea POST
    http_response_code(405); // 405: Method Not Allowed
    echo json_encode(['error' => 'Método no permitido']); // Mensaje de error
    exit; // Detener ejecución
}

// Obtener y decodificar cuerpo JSON del POST
$input = json_decode(file_get_contents('php://input'), true); // true -> arreglo asociativo

if (!$input) { // Validar que el JSON sea válido
    http_response_code(400); // 400: Bad Request
    echo json_encode(['error' => 'Datos inválidos']); // Notificar error de entrada
    exit; // Detener ejecución
}

// Extraer parámetros principales del cuerpo
$startDate = $input['start_date'] ?? null; // Fecha inicio (YYYY-MM-DD)
$endDate = $input['end_date'] ?? null; // Fecha fin (YYYY-MM-DD)
$latitude = $input['latitude'] ?? null; // Latitud
$longitude = $input['longitude'] ?? null; // Longitud

// Validar presencia de todos los campos requeridos
if (!$startDate || !$endDate || !$latitude || !$longitude) { // Falta al menos uno
    http_response_code(400); // 400: Bad Request
    echo json_encode(['error' => 'Faltan datos requeridos']); // Mensaje de error
    exit; // Detener ejecución
}

// Validar rango de fechas
$start = new DateTime($startDate); // Crear objeto fecha inicio
$end = new DateTime($endDate); // Crear objeto fecha fin

if ($start > $end) { // La fecha inicio no debe ser posterior a la fin
    http_response_code(400); // 400: Bad Request
    echo json_encode(['error' => 'La fecha de inicio no puede ser posterior a la fecha de fin']); // Error específico
    exit; // Detener ejecución
}

try { // Bloque principal protegido ante errores de ejecución
    // Crear archivo temporal con parámetros para Python
    $params_file = __DIR__ . '/temp_params.json';
    $params_data = [
        'latitud' => floatval($latitude),
        'longitud' => floatval($longitude),
        'fecha_inicio' => $startDate,
        'fecha_fin' => $endDate
    ];
    file_put_contents($params_file, json_encode($params_data));
    
    // Construir comando para ejecutar script Python con parámetros escapados
    $pythonScript = __DIR__ . '/python.py';
    $command = "python3 " . escapeshellarg($pythonScript) . " " . escapeshellarg($params_file) . " 2>&1";
    
    $output = shell_exec($command); // Ejecutar y capturar salida estándar
    
    // Eliminar archivo temporal
    if (file_exists($params_file)) {
        unlink($params_file);
    }
    
    if ($output === null) { // Verificar que el comando se ejecutó
        throw new Exception('Error al ejecutar el script de Python'); // Lanzar excepción si falla
    }
    
    // Leer resultados del JSON generado por Python
    $results_file = __DIR__ . '/resultados.json';
    if (!file_exists($results_file)) {
        throw new Exception('No se generó archivo de resultados');
    }
    
    $weatherData = json_decode(file_get_contents($results_file), true); // Decodificar JSON producido por Python
    
    if (!$weatherData) { // Validar que el JSON sea válido/no vacío
        throw new Exception('Error al procesar los datos meteorológicos');
    }
    
    // Preparar respuesta para el frontend
    $response = [
        'success' => true,
        'data' => [
            'current_weather' => [
                'temperature' => $weatherData['medias']['Temperatura (°C)'],
                'condition' => determineCondition($weatherData['medias']),
                'humidity' => $weatherData['medias']['Humedad (%)'],
                'pressure' => $weatherData['medias']['PresionAtm (hPa)'],
                'wind_speed' => $weatherData['medias']['Viento (km/h)'],
                'precipitation' => $weatherData['medias']['Precipitacion (%)']
            ],
            'location' => [
                'latitude' => floatval($latitude),
                'longitude' => floatval($longitude)
            ],
            'date_range' => [
                'start' => $startDate,
                'end' => $endDate
            ],
            'time_series' => $weatherData['datos']
        ],
        'message' => 'Cálculo completado exitosamente'
    ];
    
    // Responder éxito con los datos procesados
    echo json_encode($response);
    
} catch (Exception $e) { // Manejo de errores globales
    http_response_code(500); // 500: Internal Server Error
    echo json_encode([
        'success' => false,
        'error' => 'Error interno del servidor', // Mensaje genérico
        'message' => $e->getMessage() // Detalle del error para diagnóstico
    ]);
}

// Función auxiliar para determinar condición del clima
function determineCondition($medias) {
    $temp = $medias['Temperatura (°C)'];
    $humidity = $medias['Humedad (%)'];
    $precip = $medias['Precipitacion (%)'];
    
    if ($precip > 70) return "Rainy";
    if ($temp > 30 && $humidity < 40) return "Sunny";
    if ($temp > 25 && $humidity < 60) return "Partly Cloudy";
    if ($humidity > 70) return "Cloudy";
    if ($temp < 15) return "Overcast";
    return "Cloudy & Sunny";
}
?>
