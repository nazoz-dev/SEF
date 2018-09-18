# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from alumnos.py")

def altas():
    formulario=SQLFORM(db.alumno).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)



def bajas():
    return dict()

def modificaciones():
    return dict()
