# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from facturacion.py")

def formulario():
    return dict()#message=mensaje, lista_clientes=lista_clientes, hoy=fecha_hoy,)

def cuota():
    return dict()

def confirmar():
    return dict()

def vista_previa():
    dni_seleccionado=''
    curso_seleccionado=''
    dni = request.vars.dni
    dni_seleccionado = db(dni == db.alumno.dni).select(db.alumno.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    for x in dni_seleccionado:
        curso=x.curso #guarda el id del curso seleccionao en una variable
        curso_seleccionado= db(curso == db.curso.id).select(db.curso.ALL)
    return dict(dni_seleccionado=dni_seleccionado, curso_seleccionado=curso_seleccionado)


def vista_previa_factura():
    return dict ()
