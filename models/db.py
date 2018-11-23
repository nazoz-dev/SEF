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

db.define_table(
    auth.settings.table_user_name,
    Field('dni', 'integer', length=8, label=T('DNI')),
    Field('first_name', length=128, label=T('Nombre')),
    Field('last_name', length=128, label=T('Apellido')),
    Field('email', length=128, default='', unique=True),
    Field('username', length=128, label=T('Nombre de Usuario')),
    Field('password', 'password', length=512,
          readable=False, label=T('Password')),
    Field('registration_key', length=512,
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,
          writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.dni.requires = [
  IS_NOT_EMPTY(error_message=auth.messages.is_empty),
  IS_NOT_IN_DB(db, custom_auth_table.dni)]
custom_auth_table.first_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.username.requires = [
  IS_NOT_EMPTY(error_message=auth.messages.is_empty),
  IS_NOT_IN_DB(db, custom_auth_table.username)]
custom_auth_table.password.requires = []
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------

mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.gmail.com:587')
mail.settings.sender = myconf.get('leandrogarrido096@gmail.com')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# define-tabla
# -------------------------------------------------------------------------

auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False

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

################################################### Tabla Curso #########################################################

db.define_table('curso',
                Field('curso', 'string',label=T('Curso')),
                Field('nivel', 'string',label=T('Nivel')),
                Field('turno', 'string',label=T('Turno')),
                Field('division', 'string', writable=False, label=T('Division')),
                Field('registro', 'datetime',writable=False, readable=False,default=request.now),
               )

db.curso.curso.requires=IS_IN_SET(['1°Año', '2°Año', '3°Año', '4°Año', '5°Año', '6°Año'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')
db.curso.nivel.requires=IS_IN_SET(['Primaria', 'Secundaria'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')
db.curso.turno.requires=IS_IN_SET(['Mañana', 'Tarde'], zero=T('Elegir una opción'), error_message='Es necesario completar este campo')

############################################# Fin de la Tabla Curso ####################################################

################################################### Tabla Cuota #########################################################
db.define_table('cuota',
                Field('importe', 'float',label=T('Importe')),
                Field('mes', 'string',label=T('Mes')),
                Field('mantenimiento', 'float',label=T('Mantenimiento')),
                Field('nivel', 'string',label=T('Nivel Escolar')),
                Field('ciclo', 'integer', label=T('Ciclo Lectivo')),
                Field('registro', 'datetime',writable=False, readable=False, default=request.now),
               )

############################################# Fin de la Tabla Cuota ####################################################

################################################# Tabla Alumnos #######################################################

db.define_table('alumno',
        Field('dni', 'integer',label=T('DNI')),
        Field('apellido', 'string',label=T('Apellido')),
        Field('nombre','string',label=T('Nombres')),
        Field('sexo', 'string',label=T('Sexo'),),
        Field('f_nacimiento', 'date', label=T('Fecha de Nacimiento'), default = request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
        Field('localidad','string',label=T('Localidad')),
        Field('domicilio', 'string',label=T('Domicilio')),
        Field('telefono', 'integer',label=T('Telefono')),
        Field('curso', db.curso ,label=T('Curso, División, Turno y Nivel')),
        Field('registro', 'datetime',writable=False, readable=False,default=request.now),)

db.alumno.dni.requires=[ IS_NOT_IN_DB(db,db.alumno.dni, error_message="El campo esta incompleto o ya esta en la base de datos."), IS_LENGTH(8,error_message="Excedio la cantidad de digitos permitidos para este campo.")]
db.alumno.apellido.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumno.nombre.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumno.sexo.requires=IS_IN_SET(["Masculino", "Femenino"], zero=T('Elegir una opción'), error_message="Es necesario completar este campo")
db.alumno.localidad.requires=IS_IN_SET(['González Catán','Virrey del Pino', 'Pontevedra', 'Gregorio de Laferrere', 'Isidro Casanova','Rafael Castillo','San Justo','Ciudad Evita','Morón','Merlo','Ramos Mejía','Otro'], zero=T('Elegir una opción'), error_message="Es necesario completar este campo")
db.alumno.domicilio.requires=[IS_LOWER(), IS_NOT_EMPTY(error_message="Es necesario completar este campo")]
db.alumno.telefono.requires=[ IS_NOT_EMPTY(error_message="Es necesario completar este campo"), IS_LENGTH(10,error_message="Excedio la cantidad de digitos permitidos para este campo.")]
db.alumno.curso.requires=IS_IN_DB(db,'curso.id', '%(curso)s - %(division)s - %(turno)s - %(nivel)s', zero=T("Elegir una opción"), error_message="Es necesario completar este campo")

########################################## Fin de la Tabla Alumnos ######################################################

############################################### Tabla Alumnos x Cuota ###################################################
db.define_table('cxa',
                Field('id_alumno', db.alumno, label=T('Alumno')),
                Field('id_cuota',db.cuota, label=T('Cuota')),
                Field('estado', 'string', label=T('Estado')), #campo de cuota abonada
                Field('registro', 'datetime',writable=False, readable=False,default=request.now),
               )
############################################# Fin de la Alumno x Cuota ##################################################
