#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL

#Raíz de la aplicación
@route('/')
def raiz():
	return template('index.tpl')

#Creación de usuarios
@post('/registro')
def registro():
	
	regusuario = request.forms.get('usuario')
	regpassword = request.forms.get('contraseña')
	regemail = request.forms.get('email')
	
#Logueos de usuarios
@post('/login')
def login():
	usuario = request.forms.get('usuario')
	password = request.forms.get('contraseña')
	userldap = commands.getoutput('')
	if usuario == :
	else:
		return template ('error.tpl', usuario=usuario)

#Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='192.168.1.110', port=8080)
