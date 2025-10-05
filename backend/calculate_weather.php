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
    // Construir comando para ejecutar script Python con parámetros escapados
    $pythonScript = 'python weather_processor.py ' .
        escapeshellarg($latitude) . ' ' .
        escapeshellarg($longitude) . ' ' .
        escapeshellarg($startDate) . ' ' .
        escapeshellarg($endDate); // Evita inyección en shell
    
    $output = shell_exec($pythonScript); // Ejecutar y capturar salida estándar
    
    if ($output === null) { // Verificar que el comando se ejecutó
        throw new Exception('Error al ejecutar el script de Python'); // Lanzar excepción si falla
    }
    
    $weatherData = json_decode($output, true); // Decodificar JSON producido por Python
    
    if (!$weatherData) { // Validar que el JSON sea válido/no vacío
        throw new Exception('Error al procesar los datos meteorológicos');
    }
    
    // Responder éxito con los datos procesados
    echo json_encode([
        'success' => true, // Indicador de éxito
        'data' => $weatherData, // Payload con datos meteorológicos
        'message' => 'Cálculo completado exitosamente' // Mensaje informativo
    ]);
    
} catch (Exception $e) { // Manejo de errores globales
    http_response_code(500); // 500: Internal Server Error
    echo json_encode([
        'error' => 'Error interno del servidor', // Mensaje genérico
        'message' => $e->getMessage() // Detalle del error para diagnóstico
    ]);
}
?>
