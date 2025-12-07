<?php
echo "<h2>Buscando Python en el servidor...</h2>";

$comandos = [
    '/usr/bin/python3',
    '/usr/local/bin/python3',
    '/usr/bin/python3.9',
    '/usr/bin/python3.8',
    '/usr/bin/python3.6',
    'python3',
    'python'
];

foreach ($comandos as $cmd) {
    $salida = shell_exec("$cmd --version 2>&1");
    if ($salida) {
        echo "<p style='color:green'>✅ <b>FUNCIONA:</b> $cmd <br> Versión: $salida</p>";
    } else {
        echo "<p style='color:red'>❌ NO ENCONTRADO: $cmd</p>";
    }
}
?>