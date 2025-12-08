import sys
import os

# --- CONFIGURACIÓN CRÍTICA PARA SERVIDOR PILLAN ---
# Forzamos a Python a mirar en el directorio actual para encontrar los módulos.
# Sin esto, el servidor CGI a veces pierde la referencia de dónde están los archivos.
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, directorio_actual)
# --------------------------------------------------

from flask import Flask, render_template, request
from logica_matematica import analizar_funcion

app = Flask(__name__)

# Clave secreta necesaria para proteger los formularios contra ataques CSRF, etc.
app.config['SECRET_KEY'] = 'clave_secreta_eid_algebra_2025'

# Ruta principal: Maneja tanto la carga inicial (GET) como el envío del formulario (POST)
@app.route('/', methods=['GET', 'POST'])
def inicio():
    datos_resultado = None
    funcion_ingresada = ""
    valor_z = ""

    if request.method == 'POST':
        # 1. Recibimos los datos que el usuario escribió en el HTML
        funcion_ingresada = request.form.get('funcion', '')
        valor_z = request.form.get('valor_z', '')

        # 2. Validación básica: que no esté vacío
        if not funcion_ingresada.strip():
            datos_resultado = {
                'error': "Por favor, ingresa una función trigonométrica válida (ej: sin(x))."
            }
        else:
            # 3. Delegamos el trabajo pesado a nuestro módulo de lógica
            datos_resultado = analizar_funcion(funcion_ingresada, valor_z)

    # 4. Enviamos la respuesta al navegador pintando la plantilla 'index.html'
    return render_template('index.html', 
                           resultado=datos_resultado, 
                           func_prev=funcion_ingresada,
                           z_prev=valor_z)

if __name__ == '__main__':
    # Modo debug activado para desarrollo local
    app.run(debug=True)
