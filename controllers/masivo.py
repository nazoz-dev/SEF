# -*- coding: utf-8 -*-
# intente algo como
def index(): 
    alumnos = db(db.alumno).select()
    for alumno in alumnos:
        #q = db.cuotas.curso = alumnos.curso
        q = db.cuota
        cuotas = db(q).select()
        for cuota in cuotas:
            q = (db.cxa.id_alumno == alumno.id) & (db.cxa.id_cuota == cuota.id)
            fila = db(q).select()
            if not fila:
                # insertar registros:
                db.cxa.insert(id_alumno=alumno.id, id_cuota=cuota.id)
            else:
                # actualizar registros
                db(q).update(estado=True)
    # borro los registros:
    db(db.cxa.id_cuota==None).delete()
    response.view = "generic.html"
    filas = db((db.cxa.id_alumno == db.alumno.id) & (db.cxa.id_cuota == db.cuota.id)).select()
    return dict(message=filas)
