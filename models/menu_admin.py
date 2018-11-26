# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('SEF'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu_admin = [
    (T('Home'), False, URL('default', 'index'), [])]

response.menu_admin +=[
    (T('Usuarios'), False, None, [
            (T('Altas'), False, URL('altas','listar_usuarios')),
            (T('Bajas'), False, URL('bajas','listar_usuarios')),
        ]),
    (T('Cursos'), False, None, [
            (T('Altas'), False, URL('altas','cursos')),
            (T('Bajas'), False, URL('bajas','buscar_nivel_turno')),
            (T('Agregar Division'),False, URL('altas','mas_cursos')),
        ]),
    (T('Cuotas'), False, None, [
            (T('Altas'), False, URL('altas', 'cuotas'),[]),
            (T('Bajas'),False, URL('bajas','buscar_ciclo')),
            (T('Modificaciones'),False, URL('modificaciones','buscar_ciclo')),
        ]),
    (T('Cuota por Alumno'), False, URL('altas','cxa'),[]),
    (T('Reportes'), False, None, [
            (T('Listar Cuotas'), False, URL('reportes','buscar_ciclo')),
            (T('B'), False, ''),
            (T('C'), False, ''),
        ])
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources

    # ------------------------------------------------------------------------------------------------------------------


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
