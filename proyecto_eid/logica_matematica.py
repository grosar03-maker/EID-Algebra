import sympy as sp
from sympy.calculus.util import continuous_domain, function_range
# Importamos las herramientas de parseo avanzadas para entender escritura natural (ej: 2x, x^2)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import math

def analizar_funcion(expresion_texto, valor_z=None):
    """
    Analiza una función matemática dada en formato de texto.
    Realiza validaciones de seguridad, cálculos simbólicos (dominio, recorrido)
    y genera los puntos optimizados para el gráfico.
    """
    
    # Estructura base que devolveremos a la vista (frontend)
    resultado = {
        'error': None,
        'pasos': [],
        'grafico_datos': None,
        'dominio': '',
        'recorrido': '',
        'intersecciones_x': '',
        'intersecciones_y': '',
        'evaluacion_z': None
    }

    try:
        # ------------------------------------------------------------------
        # 1. PARSEO Y VALIDACIÓN DE ENTRADA (Seguridad y UX)
        # ------------------------------------------------------------------
        try:
            # Configuramos las transformaciones para que SymPy sea "inteligente":
            # - standard_transformations: Reglas base.
            # - implicit_multiplication: Permite escribir "2x" en vez de "2*x".
            # - convert_xor: Permite usar "^" para potencias (x^2) en vez de "**".
            transformaciones = (standard_transformations + (implicit_multiplication_application, convert_xor))
            
            # Convertimos el texto del usuario en una expresión matemática real
            funcion = parse_expr(expresion_texto, transformations=transformaciones)
        except Exception as e:
            # Si falla aquí, es porque escribieron algo que no es matemática válida
            raise ValueError(f"Sintaxis no reconocida. Error: {e}")

        # Validación de Seguridad 1: Evitar colapsos por división por cero o infinitos
        # Si la expresión es algo como "1/0" o "tan(pi/2)", SymPy devuelve 'zoo' (infinito complejo)
        if funcion.has(sp.zoo) or funcion.has(sp.oo) or funcion.has(-sp.oo):
            raise ValueError("Error Matemático: División por cero detectada.")

        # Validación de Seguridad 2: Restricción de variables
        # Para cumplir la rúbrica de funciones f(x), bloqueamos 'y', 'z', etc.
        simbolos = funcion.free_symbols
        for s in simbolos:
            if str(s) != 'x':
                raise ValueError(f"Variable '{s}' no permitida. Por favor usa solo 'x'.")

        # Definimos 'x' como nuestro símbolo principal
        variable = sp.Symbol('x')
        
        # Registramos el primer paso para mostrarlo al usuario
        resultado['pasos'].append({'titulo': '1. Análisis', 'detalle': f"Función interpretada: $${sp.latex(funcion)}$$"})

        # ------------------------------------------------------------------
        # 2. CÁLCULOS DE PROPIEDADES MATEMÁTICAS (Núcleo Algebraico)
        # ------------------------------------------------------------------
        
        # Cálculo del Dominio
        try:
            # Buscamos dónde la función es continua en los Reales
            dom = continuous_domain(funcion, variable, sp.S.Reals)
            resultado['dominio'] = sp.latex(dom)
            resultado['pasos'].append({'titulo': '2. Dominio', 'detalle': f"$$ {sp.latex(dom)} $$"})
        except: 
            resultado['dominio'] = "Complejo" # Fallback si el cálculo es muy pesado

        # Cálculo del Recorrido (Rango)
        try:
            rec = function_range(funcion, variable, sp.S.Reals)
            resultado['recorrido'] = sp.latex(rec)
            resultado['pasos'].append({'titulo': '3. Recorrido', 'detalle': f"$$ {sp.latex(rec)} $$"})
        except: 
            resultado['recorrido'] = "Complejo"

        # Intersección con Eje Y (Evaluamos x=0)
        corte_y_txt = "No existe"
        try:
            corte_y = funcion.subs(variable, 0)
            if corte_y.is_real:
                corte_y_txt = f"(0, {float(corte_y):.4f})"
                resultado['intersecciones_y'] = corte_y_txt
            else:
                resultado['intersecciones_y'] = "Indefinido"
        except: pass

        # Intersección con Eje X (Raíces/Ceros)
        cortes_x = []
        try:
            # Resolvemos f(x) = 0. Limitamos el intervalo a -10, 10 para que sea rápido.
            sols = sp.solveset(funcion, variable, domain=sp.Interval(-10, 10))
            # Tomamos solo las primeras 5 soluciones para no saturar la pantalla
            for s in list(sols)[:5]:
                if s.is_real: cortes_x.append(sp.latex(s))
        except: pass
        
        str_cortes = ", ".join(cortes_x) if cortes_x else "Ninguna visible"
        resultado['intersecciones_x'] = str_cortes
        
        resultado['pasos'].append({'titulo': '4. Intersecciones', 'detalle': f"Y: {corte_y_txt}<br>X: $${str_cortes}$$"})

        # ------------------------------------------------------------------
        # 3. EVALUACIÓN DE PUNTO Z (Requerimiento opcional)
        # ------------------------------------------------------------------
        if valor_z:
            try:
                z_v = float(valor_z)
                # Sustituimos la x por el valor ingresado
                res = float(funcion.subs(variable, z_v))
                resultado['evaluacion_z'] = {'texto': f"f({z_v}) = {res:.4f}", 'x': z_v, 'y': res}
                resultado['pasos'].append({'titulo': f'5. Evaluación Z={z_v}', 'detalle': f"Resultado: {res:.4f}"})
            except: pass

        # ------------------------------------------------------------------
        # 4. GENERACIÓN DE DATOS PARA GRÁFICO (Optimización Crítica)
        # ------------------------------------------------------------------
        datos_x, datos_y = [], []
        actual, max_val = -10.0, 10.0 # Rango de visualización
        paso = 0.1 # Resolución: menor paso = mejor curva, pero más carga
        
        # TRUCO DE RENDIMIENTO:
        # Usamos 'lambdify' para convertir la ecuación simbólica en una función Python nativa.
        # Esto es vital para funciones complejas como sin(x^2), ya que evita recalcular
        # toda la estructura matemática punto por punto.
        try:
            f_rapida = sp.lambdify(variable, funcion, modules=['math'])
        except:
            # Si falla la compilación (raro), usamos el método lento .subs() como respaldo
            f_rapida = lambda v: float(funcion.subs(variable, v))

        # Barrido numérico para generar los puntos (X, Y)
        while actual <= max_val:
            try:
                val = f_rapida(actual)
                
                # Filtro de visualización:
                # Si el valor se dispara (asíntota vertical), cortamos la línea
                # insertando un None, para que Plotly no dibuje una raya vertical fea.
                if abs(val) < 25: 
                    datos_x.append(round(actual, 2))
                    datos_y.append(val)
                else:
                    datos_x.append(round(actual, 2))
                    datos_y.append(None) # Corte limpio
            except: 
                pass # Si hay error en un punto específico, lo saltamos
            actual += paso
            
        resultado['grafico_datos'] = {'x': datos_x, 'y': datos_y}

    except Exception as e:
        # Capturamos cualquier error inesperado y lo mostramos en la web
        resultado['error'] = str(e)

    return resultado
