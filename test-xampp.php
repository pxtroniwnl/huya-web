<?php
// Script de prueba para XAMPP
header('Content-Type: text/html; charset=utf-8');

echo "<h1>Prueba de configuración XAMPP</h1>";

// Verificar PHP
echo "<h2>1. Verificación de PHP</h2>";
echo "✅ PHP versión: " . PHP_VERSION . "<br>";
echo "✅ Sistema operativo: " . PHP_OS . "<br>";

// Verificar Python
echo "<h2>2. Verificación de Python</h2>";
$python_version = shell_exec("python --version 2>&1");
if ($python_version) {
    echo "✅ Python: " . trim($python_version) . "<br>";
} else {
    echo "❌ Python no encontrado<br>";
}

// Verificar archivos
echo "<h2>3. Verificación de archivos</h2>";
$files = [
    'backend/calculate_weather.php',
    'backend/python.py',
    'pages/index.html',
    'js/script.js'
];

foreach ($files as $file) {
    if (file_exists($file)) {
        echo "✅ $file existe<br>";
    } else {
        echo "❌ $file NO existe<br>";
    }
}

// Verificar permisos de escritura
echo "<h2>4. Verificación de permisos</h2>";
$backend_dir = 'backend';
if (is_writable($backend_dir)) {
    echo "✅ Carpeta backend es escribible<br>";
} else {
    echo "❌ Carpeta backend NO es escribible<br>";
}

// Probar ejecución de Python
echo "<h2>5. Prueba de Python</h2>";
$test_command = "python backend/python.py 2>&1";
$output = shell_exec($test_command);
if ($output) {
    echo "✅ Python se ejecuta correctamente<br>";
    echo "<pre>Salida: " . htmlspecialchars($output) . "</pre>";
} else {
    echo "❌ Error al ejecutar Python<br>";
}

echo "<h2>6. Enlaces</h2>";
echo '<a href="pages/index.html">🚀 Ir al proyecto</a><br>';
echo '<a href="backend/calculate_weather.php">🔧 Probar API PHP</a><br>';
?>
