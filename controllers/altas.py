# -*- coding: utf-8 -*-

def alumnos():
    formulario=SQLFORM(db.alumno).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def cursos():
    curso=['1°Año', '2°Año', '3°Año', '4°Año', '5°Año', '6°Año']
    division='A'
    registro= request.now
    formulario= SQLFORM.factory(
        Field('nivel', 'string',label=T('Nivel Escolar'),requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('turno', 'string',label=T('Turno'),requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')))
    if formulario.accepts(request.vars, session):
        nivel= formulario.vars.nivel
        turno= formulario.vars.turno
        # INGRESANDO REGISTRO DE INSCRIPCION
        for x in curso:
            consulta = (db.curso.curso == x) & (db.curso.nivel == nivel) & (db.curso.turno == turno) & (db.curso.division == division)
            fila = db(consulta).select()
            if not fila:
                # insertar registros:
                db.curso.insert(curso=x, nivel=nivel, turno=turno, division=division, registro=registro)
            # FIN DEL INGRESO DE REGISTRO DE INSCRIPCION
            #redirect(URL('buscar_ciclo',args=(),vars=dict(ciclo=ciclo)))
                response.flash='Formulario aceptado'
            else:
                formulario.errors.nivel = 'Ya existe uno o mas cursos con el nivel seleccionado'
                formulario.errors.turno = 'Ya existe uno o mas cursos con el turno seleccionado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)


def mas_cursos():
    i=0
    division=['B','C','D','E']
    registro= request.now
    formulario= SQLFORM.factory(
        Field('curso', 'string',label=T('Curso'),requires=IS_IN_SET(['1°Año', '2°Año', '3°Año', '4°Año', '5°Año', '6°Año'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('nivel', 'string',label=T('Nivel Escolar'),requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('turno', 'string',label=T('Turno'),requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo'))
    )
    if formulario.accepts(request.vars, session):
        curso= formulario.vars.curso
        nivel= formulario.vars.nivel
        turno= formulario.vars.turno
        # INGRESANDO REGISTRO DE INSCRIPCION
        while True:
            if i==4:
                formulario.errors.curso = 'Ya existe uno o mas cursos con el curso seleccionado'
                formulario.errors.nivel = 'Ya existe uno o mas cursos con el nivel seleccionado'
                formulario.errors.turno = 'Ya existe uno o mas cursos con el turno seleccionado'
                break
            else:
                consulta = (db.curso.curso == curso) & (db.curso.nivel == nivel) & (db.curso.turno == turno) & (db.curso.division == division[i])
                fila = db(consulta).select()
                if not fila:
                    # insertar registros:
                    db.curso.insert(curso=curso, nivel=nivel, turno=turno, division=division[i], registro=registro)
                # FIN DEL INGRESO DE REGISTRO DE INSCRIPCION
                #redirect(URL('buscar_ciclo',args=(),vars=dict(ciclo=ciclo)))
                    response.flash='Formulario aceptado'
                    break
                else:
                    i+=1
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)


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
        Field('mantenimiento_mes_b', 'string',label=T('2° Mes de Mantenimiento'),requires=IS_IN_SET(['Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre','Diciembre',], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('nivel', 'string',label=T('Nivel Escolar'),requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')),
        Field('ciclo', 'integer', label=T('Ciclo Electivo'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_LENGTH(4,error_message="Excedio la cantidad de digitos permitidos para este campo.")]))
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
            nivel=formulario.vars.nivel
            ciclo = formulario.vars.ciclo
            # INGRESANDO REGISTRO DE INSCRIPCION
            consulta_inscripcion = (db.cuota.mes == inscripcion) & (db.cuota.nivel == nivel) & (db.cuota.ciclo == ciclo)
            fila_inscripcion = db(consulta_inscripcion).select()
            if not fila_inscripcion: #no estas vacia
                # insertar registros:
                db.cuota.insert(importe=importe_inscripcion, mes=inscripcion, mantenimiento=no_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro)
            # FIN DEL INGRESO DE REGISTRO DE INSCRIPCION
            for x in mes:
                # INGRESANDO REGISTRO DE CUOTA MENSUAL
                consulta_mensual = (db.cuota.mes == x) & (db.cuota.nivel == nivel) & (db.cuota.ciclo == ciclo)
                fila_mensual = db(consulta_mensual).select()
                if not fila_mensual:
                    # insertar registros:
                    if mantenimiento_mes_a==x or mantenimiento_mes_b==x:
                        db.cuota.insert(importe=importe_mensual, mes=x, mantenimiento=importe_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro) # ingresa registro con mantenimiento
                    else:
                        db.cuota.insert(importe=importe_mensual, mes=x, mantenimiento=no_mantenimiento, nivel=nivel, ciclo=ciclo, registro=registro) # ingresa registro sin mantenimiento
                # FIN DEL INGRESO DE REGISTRO DE cuota mensual
            redirect(URL('lista_cuotas',args=(),vars=dict(ciclo=ciclo, nivel=nivel)))
            response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def lista_cuotas():
    ciclo = request.vars.ciclo
    nivel= request.vars.nivel
    reg = db((ciclo == db.cuota.ciclo) & (db.cuota.nivel==nivel)).select(db.cuota.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    return dict(reg=reg, nivel=nivel)


def cxa():
    curso_alumno=''
    ciclo=request.now.year
    estado='Pendiente'
    registro= request.now
    reg_alumnos = db(db.alumno).select()
    for alumno in reg_alumnos:
        filtro_nivel = alumno.curso==db.curso.id
        consulta = db(filtro_nivel).select()
        for x in consulta:
            curso_alumno=x.nivel
            if curso_alumno=='Primaria':
                #pasa algo
                q=(db.cuota.nivel=='Primaria') & (db.cuota.ciclo==ciclo)
                reg_cuotas=db(q).select()
                for cuota in reg_cuotas:
                    q = (db.cxa.id_alumno == alumno.id) & (db.cxa.id_cuota == cuota.id)
                    fila = db(q).select()
                    if not fila:
                        # insertar registros:
                        db.cxa.insert(id_alumno=alumno.id, id_cuota=cuota.id, estado=estado, registro=registro)
            else:
                #pasa otra cosa
                q=(db.cuota.nivel=='Secundaria') & (db.cuota.ciclo==ciclo)
                reg_cuotas=db(q).select()
                for cuota in reg_cuotas:
                    q = (db.cxa.id_alumno == alumno.id) & (db.cxa.id_cuota == cuota.id)
                    fila = db(q).select()
                    if not fila:
                        # insertar registros:
                        db.cxa.insert(id_alumno=alumno.id, id_cuota=cuota.id, estado=estado, registro=registro)
    filas = db((db.cxa.id_alumno == db.alumno.id) & (db.cxa.id_cuota == db.cuota.id)).select()
    return dict(formulario=filas)
