#!/usr/local/bin/python3.11
import sys
import os
import site

# IMPORTANTE: Ruta de tus librerías (flask, sympy)
# Esta es la ruta que vimos en tu captura de pantalla
site.addsitedir('/home/users/grosa/.local/lib/python3.11/site-packages')

sys.path.insert(0, os.path.dirname(__file__))

from wsgiref.handlers import CGIHandler
try:
    from app import app
except Exception as e:
    print("Content-type: text/html\n\n")
    print(f"<h1>Error Crítico</h1><p>{e}</p>")
    sys.exit()

class ProxyFix(object):
   def __init__(self, app):
       self.app = app
   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)