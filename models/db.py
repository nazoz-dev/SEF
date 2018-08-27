# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

########################################################
########## Creacion de la Base de Datos   ##############
########################################################

################################################# Tabla Alumnos #######################################################

db.define_table('alumnos',
        Field('dni', 'integer',label=T('DNI')),
        Field('apellido', 'string',label=T('Apellido')),
        Field('nombre','string',label=T('Nombres')),
        Field('sexo', 'list:string',label=T('Sexo'),),
        Field('f_nacimiento', 'date', label=T('Fecha de Nacimiento')),
        Field('localidad','list:string',label=T('Localidad')),
        Field('domicilio', 'string',label=T('Domicilio')),
        Field('telefono', 'integer',label=T('Telefono')),
        Field('curso','list:string',label=T('Curso')),
        Field('turno','list:string',label=T('Turno')),

        Field('registro', 'datetime',writable=False, readable=False,default=request.now),)

db.alumnos.dni.requires=[ IS_NOT_IN_DB(db,db.alumnos.dni, error_message="El campo esta incompleto o ya esta en la base de datos."), IS_LENGTH(8,error_message="Excedio la cantidad de digitos permitidos para este campo.")]
db.alumnos.apellido.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumnos.nombre.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumnos.sexo.requires=IS_IN_SET(["Masculino", "Femenino"], zero=T('Elegir una opción'), error_message="Es necesario completar este campo")
db.alumnos.localidad.requires=IS_IN_SET(['González Catán','Virrey del Pino', 'Pontevedra', 'Gregorio de Laferrere', 'Isidro Casanova','Rafael Castillo','San Justo','Ciudad Evita','Morón','Merlo','Ramos Mejía','Otro'], zero=T('Elegir una opción'), error_message="Es necesario completar este campo")
db.alumnos.domicilio.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumnos.telefono.requires=[ IS_NOT_IN_DB(db,db.alumnos.telefono, error_message="Es necesario completar este campo."), IS_LENGTH(10,error_message="Excedio la cantidad de digitos permitidos para este campo.")]
db.alumnos.curso.requires=IS_IN_DB(db,db.curso.curso, '%(nombre)s', zero=T('Elegir una opción'), error_message='Es necesario completar este campo')
db.alumnos.turno.requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo'),

########################################## Fin de la Tabla Alumnos ######################################################

################################################### Tabla Curso #########################################################

db.define_table('curso',
                Field('curso', 'list:integer',label=T('Curso')),
                Field('turno', 'list:string',label=T('Turno')),
                Field('nivel', 'list:string',label=T('Nivel')),
                Field('registro', 'datetime',writable=False, readable=False,default=request.now),
               )

db.curso.curso.requires=IS_IN_SET([1, 2, 3, 4, 5, 6], zero=T('Elegir una opción'), error_message="Es necesario completar este campo")
db.curso.turno.requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')
db.curso.nivel.requires=IS_IN_SET(['Básico', 'Superior'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo'),

############################################# Fin de la Tabla Curso ####################################################
