# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    response.flash = T("¡Bienvenido!")
    nombre_rol='sin rol'
    if auth.user_id:#auth.user_id tiene el id del user logeado
        reg_id_group_logeado=db(auth.user.id==db.auth_membership.user_id).select(db.auth_membership.group_id)
        id_group_logeado=reg_id_group_logeado[0].group_id #filtro de datos 
        reg_nombre_rol=db(id_group_logeado==db.auth_group.id).select(db.auth_group.role)
        nombre_rol=reg_nombre_rol[0].role
        if nombre_rol == 'Administrador':
            redirect(URL('principal_admin'))
        elif nombre_rol=='Auxiliar Administrativo':
            redirect(URL('principal_auxiliar'))
    return dict(message=T("¡Bienvenido a SEF!"))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_membership(role='Auxiliar Administrativo')
def principal_auxiliar():
    return dict ()

@auth.requires_membership(role='Administrador')
def principal_admin():
    return dict ()
