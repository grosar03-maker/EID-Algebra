# Analizador de Funciones Trigonométricas 📐

![Estado del Proyecto](https://img.shields.io/badge/Estado-Finalizado-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Math](https://img.shields.io/badge/Lib-SymPy-orange)

## 📖 Descripción del Proyecto

Este proyecto es una aplicación web desarrollada para la asignatura **MAT1185 - Álgebra para la Computación** de la carrera de Ingeniería Civil en Informática (UCT).

El objetivo principal es proveer una herramienta interactiva que permita el análisis profundo de funciones trigonométricas (básicas, inversas y recíprocas). La aplicación no solo visualiza la función, sino que realiza un estudio analítico completo (dominio, recorrido, intersecciones) y detalla el procedimiento matemático paso a paso.

El sistema ha sido diseñado con un enfoque en la **robustez** y la **experiencia de usuario**, implementando validaciones estrictas de sintaxis y optimizaciones de rendimiento para operar en entornos de servidor compartido con recursos limitados.

## 🚀 Características Principales

### 1. Análisis Matemático Simbólico
Utilizando la potencia de **SymPy**, el sistema es capaz de:
* Calcular el **Dominio** y **Recorrido** de forma exacta (no aproximada).
* Encontrar intersecciones con los ejes $X$ e $Y$.
* Detectar y manejar asíntotas verticales.
* Interpretar transformaciones: amplitud, periodo, fase y desplazamientos.

### 2. Visualización Interactiva (High Definition)
A diferencia de las gráficas estáticas tradicionales, este proyecto implementa **Plotly.js** para generar un plano cartesiano interactivo:
* **Zoom y Paneo:** Navegación fluida por los 4 cuadrantes.
* **Renderizado HD:** Algoritmo optimizado con paso dinámico (`0.05`) para curvas suaves.
* **Control de UI:** Deslizador para ajustar el grosor de la línea en tiempo real.
* **Escala 1:1:** Configuración `scaleanchor` para evitar deformaciones visuales.

### 3. Motor de Parseo Inteligente
El sistema incluye un módulo de lógica matemática (`logica_matematica.py`) capaz de:
* Entender multiplicación implícita (ej: `2x` se interpreta como `2*x`).
* Soportar sintaxis de potencias naturales (ej: `x^2` o `x**2`).
* Validar estrictamente variables (bloqueo de variables no permitidas como `y` o `z` en entrada 2D).
* **Optimización Lambdify:** Compilación de funciones matemáticas a código máquina en tiempo de ejecución para evitar *timeouts* en funciones complejas como $\sin(x^2)$.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.11 (Flask).
* **Matemáticas:** SymPy (Cálculo Simbólico), Math (Cálculo Numérico).
* **Frontend:** HTML5, Jinja2, Bootstrap 5 (Diseño Responsivo).
* **Gráficos:** Plotly.js (Renderizado en cliente para optimizar RAM del servidor).
* **Renderizado LaTeX:** MathJax.
* **Despliegue:** CGI (Common Gateway Interface) a través de un puente PHP para servidores FreeBSD/Apache.

## 📂 Estructura del Proyecto

```text
proyecto_eid/
│
├── app.py                 # Controlador principal (Flask App)
├── logica_matematica.py   # Módulo de cálculo, validación y optimización
├── requirements.txt       # Dependencias del proyecto
├── index.cgi              # Script de ejecución para el servidor (Python)
├── index.php              # Puente y limpiador de cabeceras (PHP)
│
├── templates/             # Plantillas HTML (Jinja2)
    ├── base.html          # Estructura maestra y diseño común
    └── index.html         # Interfaz de usuario y scripts de Plotly
