#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL

usuario = "cn=admin,dc=spotype,dc=com"
#Cambiar contraseña para no tener que ponerla transparente
password = 'root'

server = Server("192.168.1.110", get_info=ALL)
conn = Connection(server, usuario, password, auto_bind=True)

#Inicio de la aplicación
@route('/')
def raiz():
	return template('index.tpl')

#Creación de usuarios
@route('/registro')
def registro():
	return template('registro.tpl')

@post('/sesion')
def sesion():
	usuario = request.forms.get('usuario')
	password = request.forms.get('password')
	email = request.forms.get('email')
	nombre = request.forms.get('nombre')
	apeuno = request.forms.get('apeuno')
	apedos = request.forms.get('apedos')
	redirect ('http://192.168.1.110:8080/prueba/'+usuario+'/'+password+'/'+email+'/'+nombre+'/'+apeuno+'/'+apedos)
	
@route('/prueba/<usuario>/<password>/<email>/<nombre>/<apeuno>/<apedos>')
def prueba(usuario,password,email,nombre,apeuno,apedos,):
	uid = "uid="+usuario+",ou=People,dc=spotype,dc=com"
	objectclass = ["inetOrgPerson","posixAccount","person","top"]
	atributos = {"cn":nombre+" "+apeuno+" "+apedos,"sn":apeuno+" "+apedos,"userPassword":password,"mail":email,"uid":usuario,"uidNumber":20000 ,"gidNumber":20000,"homeDirectory":"/home/users/"+usuario}
	conexion = conn.add(uid,objectclass,atributos)
	if conexion == True:
		return template('sesion-valida.tpl', usuario=usuario)
	else:
		return template('sesion-error.tpl', usuario=usuario)


#Logueos de usuarios
#@post('/login')
#def login():
#	usuario = request.forms.get('usuario')
#	password = request.forms.get('contraseña')
#	userldap = commands.getoutput('')
	#if usuario == :
	#else:
	#	return template ('error.tpl', usuario=usuario)

#Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='192.168.1.110', port=8080)
