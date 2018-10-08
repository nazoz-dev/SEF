# -*- coding: utf-8 -*-

def buscar_ciclo():
    formulario= SQLFORM.factory(
        Field('ciclo', 'integer', label=T('Ciclo Electivo'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_LENGTH(4,error_message="Excedio la cantidad de digitos permitidos para este campo."), IS_IN_DB(db,db.cuota.ciclo, error_message="El año ingresado no esta en la base de datos.")]))
    if formulario.accepts(request.vars, session):
        ciclo = formulario.vars.ciclo
        redirect(URL('lista_cuotas',args=(),vars=dict(ciclo=ciclo)))
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def lista_cuotas():
    ciclo = request.vars.ciclo
    nivel = request.vars.nivel
    reg = db((db.cuota.ciclo==ciclo) & (db.cuota.nivel==nivel)).select() #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    return dict(reg=reg, ciclo=ciclo)
