import sympy as sp
from sympy.calculus.util import continuous_domain, function_range

# --- FUNCION 1: ANALISIS 2D (Rúbrica Principal) ---
def analizar_funcion(expresion_texto, valor_z=None):
    """
    Analiza f(x) detectando variable automáticamente.
    """
    resultado = {
        'error': None, 'pasos': [], 'grafico_datos': None,
        'dominio': '', 'recorrido': '', 'intersecciones_y': '',
        'intersecciones_x': '', 'evaluacion_z': None
    }

    try:
        # 1. PARSEO Y SEGURIDAD
        try:
            funcion = sp.sympify(expresion_texto)
        except:
            raise ValueError("Sintaxis inválida. Revisa paréntesis y operadores (*).")

        simbolos = funcion.free_symbols
        letras_permitidas = {'x', 'y', 't', 'z', 'theta'}
        
        for s in simbolos:
            if str(s) not in letras_permitidas:
                raise ValueError(f"Variable '{s}' no permitida. Usa: x, y, z, t.")

        if len(simbolos) > 1:
            raise ValueError(f"Para el análisis 2D usa solo UNA variable. Para dos variables, ve a la pestaña 3D.")

        variable = list(simbolos)[0] if simbolos else sp.Symbol('x')
        resultado['pasos'].append(f"1. Función detectada: f({variable}) = {sp.latex(funcion)}")

        # 2. CÁLCULOS
        try:
            dom = continuous_domain(funcion, variable, sp.S.Reals)
            resultado['dominio'] = sp.latex(dom)
        except: resultado['dominio'] = "Complejo"

        try:
            rec = function_range(funcion, variable, sp.S.Reals)
            resultado['recorrido'] = sp.latex(rec)
        except: resultado['recorrido'] = "Complejo"

        try:
            corte_y = funcion.subs(variable, 0)
            if corte_y.is_real: resultado['intersecciones_y'] = f"(0, {float(corte_y):.2f})"
        except: pass

        cortes_x = []
        try:
            sols = sp.solveset(funcion, variable, domain=sp.Interval(-10, 10))
            for s in list(sols)[:5]:
                if s.is_real: cortes_x.append(sp.latex(s))
        except: pass
        resultado['intersecciones_x'] = ", ".join(cortes_x) if cortes_x else "Ninguna cercana"

        # 3. EVALUACION Z
        if valor_z:
            try:
                z_v = float(valor_z)
                res = float(funcion.subs(variable, z_v))
                resultado['evaluacion_z'] = {'texto': f"f({z_v}) = {res:.4f}", 'x': z_v, 'y': res}
            except: pass

        # 4. DATOS GRÁFICO 2D
        datos_x, datos_y = [], []
        actual, max_val = -10.0, 10.0
        while actual <= max_val:
            try:
                val = float(funcion.subs(variable, actual))
                if abs(val) < 50:
                    datos_x.append(round(actual, 2))
                    datos_y.append(val)
                else:
                    datos_x.append(round(actual, 2))
                    datos_y.append(None)
            except: pass
            actual += 0.2
        
        resultado['grafico_datos'] = {'x': datos_x, 'y': datos_y}

    except Exception as e:
        resultado['error'] = str(e)

    return resultado

# --- FUNCION 2: GENERADOR 3D (Bonus) ---
def generar_datos_3d(expresion_texto):
    """
    Genera matriz Z para f(x, y).
    """
    resultado = {'error': None, 'x': [], 'y': [], 'z': []}
    try:
        x, y = sp.symbols('x y')
        try:
            funcion = sp.sympify(expresion_texto)
        except:
            raise ValueError("Sintaxis incorrecta.")

        rango = list(range(-5, 6)) # -5 a 5
        matriz_z = []
        
        for val_y in rango:
            fila = []
            for val_x in rango:
                try:
                    val = float(funcion.subs({x: val_x, y: val_y}))
                    if abs(val) > 50: val = None
                    fila.append(val)
                except: fila.append(None)
            matriz_z.append(fila)

        resultado['x'] = rango
        resultado['y'] = rango
        resultado['z'] = matriz_z

    except Exception as e:
        resultado['error'] = str(e)
    return resultado