# -*- coding: utf-8 -*-

#######################################################################################################################################################################################################

def buscar_dni():
    formulario= SQLFORM.factory(
        Field('dni', 'integer', label=T('DNI'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_LENGTH(8,error_message="Excedio la cantidad de digitos permitidos para este campo."), IS_IN_DB(db,db.alumno.dni, error_message="El DNI ingresado no esta en la base de datos.")]))
    if formulario.accepts(request.vars, session):
        dni = formulario.vars.dni
        redirect(URL('alumnos',args=(),vars=dict(dni=dni)))
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def alumnos():
    dni = request.vars.dni
    reg = db(dni == db.alumno.dni).select(db.alumno.ALL).first() #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    form = SQLFORM(db.alumno,reg, submit_button='Guardar Cambios')
    if form.accepts(request.vars, session):
        redirect(URL('buscar_dni',args=(),vars=dict()))
        response.flash='Se guardaron los cambios correctamente.'
    elif form.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(form=form)

####################################################################################################################################################################################################

def buscar_nivel_turno():
    formulario= SQLFORM.factory(
        Field('nivel', 'string',label=T('Nivel Escolar'),requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('turno', 'string',label=T('Turno'),requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo'))
    )
    if formulario.accepts(request.vars, session):
        nivel = formulario.vars.nivel
        turno = formulario.vars.turno
        consulta = (db.curso.nivel==nivel) & (db.curso.turno==turno)
        fila = db(consulta).select()
        if fila:
            response.flash='Formulario aceptado'
            redirect(URL('lista_cursos',args=(),vars=dict(nivel=nivel, turno=turno)))
        else:
            formulario.errors.nivel = 'El ciclo y nivel ingresado no existe'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def lista_cursos():
    nivel = request.vars.nivel
    turno = request.vars.turno
    cursos = db((nivel == db.curso.nivel) & (db.curso.turno==turno)).select()
    return dict(cursos=cursos)

def cursos():
    reg = db.curso(request.args[0]) # Cumple la funcion de un SELECT
    form = SQLFORM(db.curso,reg, submit_button='Guardar Cambios')
    if form.accepts(request.vars, session):
        curso = form.vars.curso
        nivel = form.vars.nivel
        turno = form.vars.turno
        division= form.vars.division
        registro= request.now
        id_curso= form.vars.id
        consulta = (db.curso.curso==curso) & (db.curso.nivel==nivel) & (db.curso.turno==turno) & (db.curso.division==division)
        fila = db(consulta).select()
        if fila=='':
            form.errors.turno= 'Ya existe un curso con los valores ingresados' #= response.flash='Hay uno o más errores en el formulario'
        else:
            response.flash='Se guardaron los cambios correctamente.'
            redirect(URL('buscar_nivel_turno',args=(),vars=dict()))
    elif form.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(form=form)

##############################################################################################################################################################################################

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
    reg = db((ciclo == db.cuota.ciclo) & (db.cuota.nivel==nivel)).select(db.cuota.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    return dict(reg=reg, ciclo=ciclo, nivel=nivel)

def cuotas():
    inscripcion='Inscripción'
    mes=['Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre','Diciembre',]
    no_mantenimiento=0
    registro= request.now
    formulario= SQLFORM.factory(
        Field('importe_inscripcion', 'float',label=T('Importe Inscripción'),requires=IS_NOT_EMPTY(error_message="Es necesario completar este campo")),
        Field('importe_mensual', 'float',label=T('Importe Mensual'),requires=IS_NOT_EMPTY(error_message="Es necesario completar este campo")),
        Field('importe_mantenimiento', 'float',label=T('Importe Mantenimiento'),requires=IS_NOT_EMPTY(error_message="Es necesario completar este campo")),
        Field('mantenimiento_mes_a', 'string',label=T('1° Mes de Mantenimiento'),requires=IS_IN_SET(['Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre','Diciembre',], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('mantenimiento_mes_b', 'string',label=T('2° Mes de Mantenimiento'),requires=IS_IN_SET(['Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre','Diciembre',], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')))
    if formulario.accepts(request.vars, session):
        if formulario.vars.mantenimiento_mes_a == formulario.vars.mantenimiento_mes_b:
            formulario.errors.mantenimiento_mes_a = 'El mes para la cuota de mantenimiento ya fue seleccionado'
            formulario.errors.mantenimiento_mes_b = 'El mes para la cuota de mantenimiento ya fue seleccionado'
        else:
            importe_inscripcion= formulario.vars.importe_inscripcion
            importe_mensual= formulario.vars.importe_mensual
            importe_mantenimiento= formulario.vars.importe_mantenimiento
            mantenimiento_mes_a= formulario.vars.mantenimiento_mes_a
            mantenimiento_mes_b= formulario.vars.mantenimiento_mes_b
            ciclo = request.args[0]
            nivel= request.args[1]
            # INGRESANDO REGISTRO DE INSCRIPCION
            consulta_inscripcion = (db.cuota.mes == inscripcion) & (db.cuota.nivel == nivel) & (db.cuota.ciclo == ciclo)
            fila_inscripcion = db(consulta_inscripcion).select()
            if fila_inscripcion:
                # insertar registros:
                db(consulta_inscripcion).update(importe=importe_inscripcion, mes=inscripcion, mantenimiento=no_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro)
            # FIN DEL INGRESO DE REGISTRO DE INSCRIPCION
            for x in mes:
                # INGRESANDO REGISTRO DE CUOTA MENSUAL
                consulta_mensual = (db.cuota.mes == x) & (db.cuota.nivel == nivel) & (db.cuota.ciclo == ciclo)
                fila_mensual = db(consulta_mensual).select()
                if fila_mensual:
                    # insertar registros:
                    if mantenimiento_mes_a==x or mantenimiento_mes_b==x:
                        db(consulta_mensual).update(importe=importe_mensual, mes=x, mantenimiento=importe_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro) # ingresa registro con mantenimiento
                    else:
                        db(consulta_mensual).update(importe=importe_mensual, mes=x, mantenimiento=no_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro) # ingresa registro sin mantenimiento
                # FIN DEL INGRESO DE REGISTRO DE cuota mensual
            redirect(URL('buscar_ciclo',args=(),vars=dict()))
            response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

##################################################################################################################################################################################################
