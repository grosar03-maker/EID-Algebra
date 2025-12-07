<?php
// Puente para ejecutar Python 3.11 en Pillan
ini_set('display_errors', 1);
error_reporting(E_ALL);

$python_executable = '/usr/local/bin/python3.11';
$script_cgi = __DIR__ . '/index.cgi';

$env = array_merge($_SERVER, [
    'PYTHONPATH' => __DIR__,
    'SCRIPT_FILENAME' => $script_cgi,
    'REQUEST_URI' => $_SERVER['REQUEST_URI'],
    'SCRIPT_NAME' => $_SERVER['SCRIPT_NAME']
]);

$descriptors = [0 => ["pipe", "r"], 1 => ["pipe", "w"], 2 => ["pipe", "w"]];
$process = proc_open("$python_executable $script_cgi", $descriptors, $pipes, __DIR__, $env);

if (is_resource($process)) {
    fwrite($pipes[0], file_get_contents("php://input"));
    fclose($pipes[0]);
    echo stream_get_contents($pipes[1]);
    $errors = stream_get_contents($pipes[2]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    if ($errors) { echo "<pre style='color:red'>$errors</pre>"; }
    proc_close($process);
}
?>