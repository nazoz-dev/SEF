# -*- coding: utf-8 -*-

def buscar_dni():
    return dict()

def generar_boleta():
    dni_seleccionado=''
    curso_seleccionado=''
    dni = request.vars.dni
    dni_seleccionado = db(dni == db.alumno.dni).select(db.alumno.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    for x in dni_seleccionado:
        curso=x.curso #guarda el id del curso seleccionao en una variable
        curso_seleccionado= db(curso == db.curso.id).select(db.curso.ALL)
    return dict(dni_seleccionado=dni_seleccionado, curso_seleccionado=curso_seleccionado)

def generar_recibo():
    return dict()
