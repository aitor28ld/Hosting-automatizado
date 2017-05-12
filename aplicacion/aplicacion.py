#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL

usuario = "cn=admin,dc=spotype,dc=com"
#Cambiar contraseña para no tener que ponerla transparente
password = getpass.getpass('Introduce la contraseña: ')

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
	sesusuario = request.forms.get('usuario')
	sespassword = request.forms.get('password')
	sesemail = request.forms.get('email')
	sesnombre = request.forms.get('nombre')
	sesapeuno = request.forms.get('apeuno')
	sesapedos = request.forms.get('apedos')
	sesssh = request.forms.get('ssh')
	uid = "uid="+sesusuario+",ou=People,cn=admin,dc=spotype,dc=com"
	objectclass = ["inetOrgPerson","posixAccount","person","top","ldapPublicKey"]
	atributos = {"cn":sesnombre+''+sesapeuno+''+sesapedos,"sn":sesapeuno+''+sesapedos,"mail":sesemail,"uid": sesusuario,"uidNumber":20000 ,"gidNumber": 20000,"homeDirectory":"/home/users/"+sesusuario,"sshPublicKey": sesssh}
	conn.add(uid,objectclass,atributos)
	print conn
	return template('sesion.tpl', usuario=sesusuario)
	
"""Añadir la introducción de los esquemas al fichero de slapd.conf con ansible"""

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
