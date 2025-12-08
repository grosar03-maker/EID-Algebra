<?php
// index.php - Puente PHP->Python (Versión Blindada)
// Este archivo actúa como intermediario. Recibe la petición web y la pasa al script de Python.
// Además, se encarga de limpiar cualquier basura técnica que el servidor imprima antes del HTML.

ini_set('display_errors', 1);
error_reporting(E_ALL);

// Ruta específica a Python 3.11 en el servidor Pillan (UCT)
$python_executable = '/usr/local/bin/python3.11';
$script_cgi = __DIR__ . '/index.cgi';

// Preparamos el entorno para que Flask crea que se está ejecutando normalmente
$env = array_merge($_SERVER, [
    'PYTHONPATH' => __DIR__,
    'SCRIPT_FILENAME' => $script_cgi,
    'REQUEST_URI' => $_SERVER['REQUEST_URI'],
    'SCRIPT_NAME' => $_SERVER['SCRIPT_NAME']
]);

// Abrimos tuberías (pipes) para comunicarnos con el proceso de Python
$descriptors = [
    0 => ["pipe", "r"], // Entrada (Lo que manda el navegador)
    1 => ["pipe", "w"], // Salida (Lo que responde Python)
    2 => ["pipe", "w"]  // Errores
];

$process = proc_open("$python_executable $script_cgi", $descriptors, $pipes, __DIR__, $env);

if (is_resource($process)) {
    // Pasar los datos del formulario (POST) a Python
    fwrite($pipes[0], file_get_contents("php://input"));
    fclose($pipes[0]);

    // Leer toda la respuesta que generó Python (Flask)
    $raw_output = stream_get_contents($pipes[1]);
    $errors = stream_get_contents($pipes[2]);

    fclose($pipes[1]);
    fclose($pipes[2]);
    proc_close($process);

    if ($errors) {
        // Si Python falló (ej: error de sintaxis en el código), lo mostramos en rojo
        echo "<pre style='color:red'>$errors</pre>";
    } else {
        // --- LIMPIEZA DE CABECERAS (CRÍTICO PARA EL DISEÑO) ---
        // A veces el servidor CGI devuelve cabeceras técnicas ("Status: 200 OK")
        // visibles en la página. Este bloque busca dónde empieza el código HTML real
        // y borra todo lo anterior.
        
        $inicio_html = strpos($raw_output, '<!DOCTYPE');
        
        if ($inicio_html === false) {
            // Si no tiene doctype, buscamos la etiqueta html
            $inicio_html = strpos($raw_output, '<html');
        }

        if ($inicio_html !== false) {
            // ¡ENCONTRADO! Imprimimos solo desde el HTML hacia abajo.
            // Esto asegura que la página empiece limpia.
            echo substr($raw_output, $inicio_html);
        } else {
            // Fallback: Si no encontramos HTML, intentamos separar por doble salto de línea
            $parts = preg_split('/(\r\n\r\n|\n\n)/', $raw_output, 2);
            if (count($parts) == 2) {
                echo $parts[1];
            } else {
                echo $raw_output; 
            }
        }
    }
} else {
    echo "Error crítico: No se pudo iniciar el proceso de Python.";
}
?>
