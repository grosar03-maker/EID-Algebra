import sys
import os

# TRUCO CRÍTICO: Forzamos a Python a mirar en la carpeta actual
# para encontrar 'logica_matematica.py' y 'templates'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
# Importamos ambas funciones de tu lógica (2D y 3D)
from logica_matematica import analizar_funcion, generar_datos_3d

app = Flask(__name__)
# Clave secreta necesaria para formularios seguros
app.config['SECRET_KEY'] = 'clave_secreta_eid_2025'

# --- RUTA 1: EL ANALIZADOR 2D (Página Principal) ---
@app.route('/', methods=['GET', 'POST'])
def inicio():
    datos = None
    func = ""
    z_val = ""
    
    if request.method == 'POST':
        # Capturamos datos del formulario 2D
        func = request.form.get('funcion', '')
        z_val = request.form.get('valor_z', '')
        
        if func:
            # Llamamos a la lógica 2D
            datos = analizar_funcion(func, z_val)
            
    return render_template('index.html', resultado=datos, func_prev=func, z_prev=z_val)

# --- RUTA 2: EL GENERADOR 3D (El Bonus) ---
@app.route('/3d', methods=['GET', 'POST'])
def pagina_3d():
    datos = None
    func = ""
    
    if request.method == 'POST':
        # Capturamos datos del formulario 3D
        func = request.form.get('funcion', '')
        
        if func:
            # Llamamos a la lógica 3D
            datos = generar_datos_3d(func)
            
    return render_template('3d.html', datos=datos, func_prev=func)

if __name__ == '__main__':
    app.run(debug=True)