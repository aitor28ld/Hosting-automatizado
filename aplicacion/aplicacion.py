#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, app, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

usuario = "cn=admin,dc=spotype,dc=com"
#Cambiar contraseña para no tener que ponerla transparente
password = 'root'

server = Server("192.168.1.110", get_info=ALL)
conn = Connection(server, usuario, password, auto_bind=True)

#Inicio de la aplicación
@route('/')
def raiz():
	s = request.environ.get('beaker.session')
	s.save()
	if s.has_key('test'):
		return template('index-sesion.tpl',usuario=s["test"][1])
	else:
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
		commands.getoutput('sudo mkdir /home/users/'+usuario)
		uid = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" uidNumber |grep uid | tail -1 |cut -d: -f2')
		uid = uid.split(" ")[1]
		commands.getoutput('sudo chown '+uid+' /home/users/'+usuario)
		commands.getoutput('sudo chmod 700 /home/users/'+usuario)
		return template('sesion-valida.tpl', usuario=usuario)
	else:
		return template('sesion-error.tpl', usuario=usuario)

#Logueos de usuarios
@route('/inicio')
def inicio():
	return template('inicio.tpl')

@post('/login')
def login():
	s = request.environ.get('beaker.session')
	usuario = request.forms.get('usuario')
	password = request.forms.get('contraseña')
	userldap = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" uid |grep uid | tail -1 |cut -d: -f2')
	userldap = userldap.split(" ")[1]
	passldap = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" userPassword | grep userPassword | tail -1 | cut -d: -f3')
	passldap = passldap.split(" ")[1]
	passldap = commands.getoutput('echo -n '+passldap+' | base64 -d')
	if usuario == userldap and password == passldap:
		s['test'] = ['login-ok.tpl',usuario]
		s.save()
		return template(s['test'][0], usuario=s['test'][1])
	else:
		return template ('login-error.tpl')

#Perfil de usuarios
@get('/perfil')
def perfil():
	s = request.environ.get('beaker.session')
	s.save()
	return template('perfil.tpl', usuario=s['test'][1])

#Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(app=app,host='192.168.1.110', port=8080)
