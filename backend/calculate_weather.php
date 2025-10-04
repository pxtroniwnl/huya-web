<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Método no permitido']);
    exit;
}

// Obtener datos del POST
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Datos inválidos']);
    exit;
}

$startDate = $input['start_date'] ?? null;
$endDate = $input['end_date'] ?? null;
$latitude = $input['latitude'] ?? null;
$longitude = $input['longitude'] ?? null;

// Validar datos requeridos
if (!$startDate || !$endDate || !$latitude || !$longitude) {
    http_response_code(400);
    echo json_encode(['error' => 'Faltan datos requeridos']);
    exit;
}

// Validar fechas
$start = new DateTime($startDate);
$end = new DateTime($endDate);

if ($start > $end) {
    http_response_code(400);
    echo json_encode(['error' => 'La fecha de inicio no puede ser posterior a la fecha de fin']);
    exit;
}

try {
    // Ejecutar script Python
    $pythonScript = 'python weather_processor.py ' . escapeshellarg($latitude) . ' ' . escapeshellarg($longitude) . ' ' . escapeshellarg($startDate) . ' ' . escapeshellarg($endDate);
    
    $output = shell_exec($pythonScript);
    
    if ($output === null) {
        throw new Exception('Error al ejecutar el script de Python');
    }
    
    $weatherData = json_decode($output, true);
    
    if (!$weatherData) {
        throw new Exception('Error al procesar los datos meteorológicos');
    }
    
    // Respuesta exitosa
    echo json_encode([
        'success' => true,
        'data' => $weatherData,
        'message' => 'Cálculo completado exitosamente'
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => 'Error interno del servidor',
        'message' => $e->getMessage()
    ]);
}
?>
