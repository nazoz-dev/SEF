# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from facturacion.py")

def formulario():
    #importamos libreria para el formato de la fecha
    import time
    #genera la fecha actual
    #fecha_hoy= time.strftime("%x")
    # definir los campos a obtener desde la base de datos:
    campos=0 #= db.cliente.id_cliente, db.cliente.nombre_de_fantasia, db.cliente.razon_social
    # definir la condición que deben cumplir los registros:
    criterio=1 #= db.cliente.id_cliente>0
    # ejecutar la consulta:
    lista_clientes=2 #= db(criterio).select(*campos)
    # revisar si la consulta devolvio registros:
    if not lista_clientes:
        mensaje = "No ha cargado clientes"
    else:
        mensaje = "Seleccione un cliente"
    #redirije los valores al HTML
    return dict()#message=mensaje, lista_clientes=lista_clientes, hoy=fecha_hoy,)

def cuota():
    return dict()

def confirmar():
    return dict()

def vista_previa():
    return dict ()

def vista_previa_factura():
    return dict()
