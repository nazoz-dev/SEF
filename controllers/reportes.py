# -*- coding: utf-8 -*-

def buscar_ciclo():
    formulario= SQLFORM.factory(
        Field('ciclo', 'integer', label=T('Ciclo Electivo'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_LENGTH(4,error_message="Excedio la cantidad de digitos permitidos para este campo.")]),
        Field('nivel', 'string',label=T('Nivel Escolar'),requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo'))
    )
    if formulario.accepts(request.vars, session):
        ciclo = formulario.vars.ciclo
        nivel = formulario.vars.nivel
        consulta = (db.cuota.ciclo==ciclo) & (db.cuota.nivel==nivel)
        fila = db(consulta).select()
        if fila:
            response.flash='Formulario aceptado'
            redirect(URL('lista_cuotas',args=(),vars=dict(ciclo=ciclo, nivel=nivel)))
        else:
            formulario.errors.nivel = 'El ciclo y nivel ingresado no existe'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def lista_cuotas():
    ciclo = request.vars.ciclo
    nivel = request.vars.nivel
    reg = db((db.cuota.ciclo==ciclo) & (db.cuota.nivel==nivel)).select() #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    return dict(reg=reg, ciclo=ciclo)

#######################################################################################################################################################################################################################

def buscar_curso():
    reg=db(db.curso).select()
    return dict(reg=reg)

def lista_morosos():
    nombre_curso=''
    id_curso=request.args[0]
    curso= db(db.curso.id==id_curso).select()
    for x in curso:
        nombre_curso=x.curso +' '+ x.division +' '+ x.turno + ' - ' + x.nivel
    consulta=(db.alumno.id==db.cxa.id_alumno) & (db.cuota.id==db.cxa.id_cuota) & (db.alumno.curso==id_curso) & (db.cxa.estado=="Pendiente")
    reg=db(consulta).select()
    return dict(reg=reg, nombre_curso=nombre_curso)

def lisos():
    nombre_curso=''
    id_curso=request.args[0]
    curso= db(db.curso.id==id_curso).select()
    for x in curso:
        nombre_curso=x.curso +' '+ x.division +' '+ x.turno + ' - ' + x.nivel
    q=db(db.alumno.curso==id_curso).select()
    for alumno in q:
        y=db(db.cuota).select()
        for cuota in y:
            consulta=(alumno.id==db.cxa.id_alumno) & (cuota.id==db.cxa.id_cuota) & (db.cxa.estado=="Pendiente")
            reg=db(consulta).select()
    return dict(reg=reg, nombre_curso=nombre_curso)
