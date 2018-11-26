# -*- coding: utf-8 -*-

def buscar_dni():
    response.flash = T("¡Bienvenido!")
    nombre_rol='sin rol'
    if auth.user_id:#auth.user_id tiene el id del user logeado
        reg_id_group_logeado=db(auth.user.id==db.auth_membership.user_id).select(db.auth_membership.group_id)
        id_group_logeado=reg_id_group_logeado[0].group_id #filtro de datos 
        reg_nombre_rol=db(id_group_logeado==db.auth_group.id).select(db.auth_group.role)
        nombre_rol=reg_nombre_rol[0].role
    formulario= SQLFORM.factory(
        Field('dni', 'integer', label=T('DNI'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_IN_DB(db,db.alumno.dni, error_message="El DNI ingresado no esta en la base de datos."), IS_LENGTH(8,error_message="Excedio la cantidad de digitos permitidos para este campo.")]))
    if formulario.accepts(request.vars, session):
        dni = formulario.vars.dni
        redirect(URL('generar_boleta',args=(),vars=dict(dni=dni)))
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario, nombre_rol=nombre_rol)

def generar_boleta():
    dni_seleccionado=''
    curso_seleccionado=''
    cuota_seleccionado=''
    cuotaid=''
    descripcion=""
    dni = request.vars.dni
    dni_seleccionado = db(dni == db.alumno.dni).select(db.alumno.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    for x in dni_seleccionado:
        curso=x.curso #guarda el id del curso seleccionao en una variable
        curso_seleccionado= db(curso == db.curso.id).select(db.curso.ALL)
        id_alumno_seleccionado= x.id
        q=(db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==db.cuota.id)
        cuotas_seleccionado= db(q).select()
        validador=(db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==db.cuota.id) & (db.cxa.estado=="Pendiente")
        #db.cuotas_seleccionado.cxa.estado=="Pendiente"
        cuota_pendiente=db(validador).select()
        for w in cuota_pendiente:
            ciclo=w.cuota.ciclo
            mes=w.cuota.mes
            importe=w.cuota.importe
            mantenimiento=w.cuota.mantenimiento
            total_importe=importe+mantenimiento
            break
        descripcion+="Cuota "+ mes + " " + str(ciclo)
        #cuotas= db(db.cxa.id_alumno==id_alumno_seleccionado).select(db.cxa.ALL)
        #for y in cuotas:
         #   estado=y.estado
            #if estado=='False':
               #cuotaid=y.id_cuota
            #else:
             #   break
        #cuota_seleccionado=db((db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==cuotaid)).select()
    return dict(dni_seleccionado=dni_seleccionado, curso_seleccionado=curso_seleccionado, cuotas_seleccionado=cuotas_seleccionado, mantenimiento=mantenimiento, importe=importe, mes=mes, total_importe=total_importe, descripcion=descripcion)
#lista alumnos por un lado y cuotas por otro, de ahi realiza una consulta para que el id del dni que se ingreso sea igual al del alumno y con el id del alumno y las cuotas realizar un for con consulta para saber cual esta en True 

def auxiliar_buscar_dni():
    response.flash = T("¡Bienvenido!")
    nombre_rol='sin rol'
    if auth.user_id:#auth.user_id tiene el id del user logeado
        reg_id_group_logeado=db(auth.user.id==db.auth_membership.user_id).select(db.auth_membership.group_id)
        id_group_logeado=reg_id_group_logeado[0].group_id #filtro de datos 
        reg_nombre_rol=db(id_group_logeado==db.auth_group.id).select(db.auth_group.role)
        nombre_rol=reg_nombre_rol[0].role
    formulario= SQLFORM.factory(
        Field('dni', 'integer', label=T('DNI'), requires=[IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_IN_DB(db,db.alumno.dni, error_message="El DNI ingresado no esta en la base de datos."), IS_LENGTH(8,error_message="Excedio la cantidad de digitos permitidos para este campo.")]))
    if formulario.accepts(request.vars, session):
        dni = formulario.vars.dni
        redirect(URL('generar_boleta',args=(),vars=dict(dni=dni)))
        response.flash='Formulario aceptado'
    elif formulario.errors:
        response.flash='Hay uno o más errores en el formulario'
    return dict(formulario=formulario, nombre_rol=nombre_rol)

def auxiliar_generar_boleta():
    dni_seleccionado=''
    curso_seleccionado=''
    cuota_seleccionado=''
    cuotaid=''
    descripcion=""
    dni = request.vars.dni
    dni_seleccionado = db(dni == db.alumno.dni).select(db.alumno.ALL) #mediante una consulta a la db obtiene un reg con los datos del usuario seleccionado
    for x in dni_seleccionado:
        curso=x.curso #guarda el id del curso seleccionao en una variable
        curso_seleccionado= db(curso == db.curso.id).select(db.curso.ALL)
        id_alumno_seleccionado= x.id
        q=(db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==db.cuota.id)
        cuotas_seleccionado= db(q).select()
        validador=(db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==db.cuota.id) & (db.cxa.estado=="Pendiente")
        #db.cuotas_seleccionado.cxa.estado=="Pendiente"
        cuota_pendiente=db(validador).select()
        for w in cuota_pendiente:
            ciclo=w.cuota.ciclo
            mes=w.cuota.mes
            importe=w.cuota.importe
            mantenimiento=w.cuota.mantenimiento
            total_importe=importe+mantenimiento
            break
        descripcion+="Cuota "+ mes + " " + str(ciclo)
        #cuotas= db(db.cxa.id_alumno==id_alumno_seleccionado).select(db.cxa.ALL)
        #for y in cuotas:
         #   estado=y.estado
            #if estado=='False':
               #cuotaid=y.id_cuota
            #else:
             #   break
        #cuota_seleccionado=db((db.cxa.id_alumno==id_alumno_seleccionado) & (db.cxa.id_cuota==cuotaid)).select()
    return dict(dni_seleccionado=dni_seleccionado, curso_seleccionado=curso_seleccionado, cuotas_seleccionado=cuotas_seleccionado, mantenimiento=mantenimiento, importe=importe, mes=mes, total_importe=total_importe, descripcion=descripcion)
#lista alumnos por un lado y cuotas por otro, de ahi realiza una consulta para que el id del dni que se ingreso sea igual al del alumno y con el id del alumno y las cuotas realizar un for con consulta para saber cual esta en True
