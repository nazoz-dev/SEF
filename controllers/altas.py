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
    formulario=SQLFORM(db.cuota).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def cxa():
    formulario=SQLFORM(db.cxa).process()
    if formulario.accepts(request.vars, session):
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario)

def bucar_mes():
    return dict()

def mantenimiento():
    return dict()
