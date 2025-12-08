#!/usr/local/bin/python3.11
import sys
import os
import site

# CONFIGURACIÓN DE LIBRERÍAS DE USUARIO
# Como instalamos Flask y SymPy en el usuario local (no somos root),
# necesitamos decirle a Python explícitamente dónde buscarlas.
site.addsitedir('/home/users/grosa/.local/lib/python3.11/site-packages')

# Agregamos el directorio actual al path para encontrar app.py
sys.path.insert(0, os.path.dirname(__file__))

from wsgiref.handlers import CGIHandler

try:
    # Intentamos importar la aplicación Flask
    from app import app
except Exception as e:
    # Si falla la importación, mostramos el error en pantalla para depurar
    print("Content-type: text/html\n\n")
    print(f"<h1>Error Crítico al importar App</h1><p>{e}</p>")
    sys.exit()

# Middleware para corregir rutas en entornos CGI
class ProxyFix(object):
   def __init__(self, app):
       self.app = app
   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

if __name__ == '__main__':
    # Aplicamos el fix y ejecutamos mediante CGIHandler
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)
