# -*- coding: utf-8 -*-

def alumnos():
    formulario=SQLFORM(db.alumno).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def cursos():
    formulario=SQLFORM(db.curso).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def cuotas():
    formulario=SQLFORM(db.cuota).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def axc():
    return dict()
