#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, app, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL
from beaker.middleware import SessionMiddleware
from github import Github

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
	if s.has_key('sesion'):
		return template('index-sesion.tpl',usuario=s["sesion"][1])
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
	ssh = request.forms.get('ssh')
	s = request.environ.get('beaker.session')
	s["ssh"] = [ssh]
	s.save()
	redirect ('http://192.168.1.110:8080/prueba/'+usuario+'/'+password+'/'+email+'/'+nombre+'/'+apeuno+'/'+apedos)
	
@route('/prueba/<usuario>/<password>/<email>/<nombre>/<apeuno>/<apedos>')
def prueba(usuario,password,email,nombre,apeuno,apedos):
	s = request.environ.get('beaker.session')
	uid = "uid="+usuario+",ou=People,dc=spotype,dc=com"
	objectclass = ["inetOrgPerson","posixAccount","person","top","ldapPublicKey"]
	atributos = {"cn":nombre+" "+apeuno+" "+apedos,"sn":apeuno+" "+apedos,"userPassword":password,"mail":email,"uid":usuario,"uidNumber":20000 ,"gidNumber":20000,"homeDirectory":"/home/users/"+usuario,"sshPublicKey": s["ssh"]}
	conexion = conn.add(uid,objectclass,atributos)
	if conexion == True:
		commands.getoutput('sudo mkdir /home/users/'+usuario)
		uid = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" uidNumber |grep uid | tail -1 |cut -d: -f2')
		uid = uid.split(" ")[1]
		commands.getoutput('sudo chown '+uid+' /home/users/'+usuario)
		commands.getoutput('sudo mkdir /home/users/'+usuario+'/.ssh/')
		commands.getoutput('sudo chgrp -R usuario /home/users/'+usuario+'/')
		commands.getoutput('sudo chmod -R 770 /home/users/'+usuario)
		commands.getoutput('echo "'+s["ssh"][0]+'" > /home/users/'+usuario+'/.ssh/id_rsa.pub')
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
	if passldap != "":
		passldap = passldap.split(" ")[1]
		passldap = commands.getoutput('echo -n '+passldap+' | base64 -d')
		if usuario == userldap and password == passldap:
			s['sesion'] = ['login-ok.tpl',usuario]
			s.save()
			return template(s['sesion'][0], usuario=s['sesion'][1])
		else:
			return template ('login-error.tpl')
	else:
		return template ('login-error.tpl')

#Perfil de usuarios
@get('/perfil')
def perfil():
	s = request.environ.get('beaker.session')
	s.save()
	return template('perfil.tpl', usuario=s['sesion'][1])
	
#Subir CMS con repositorio
@get('/web')
def web():
	return template('web.tpl')
	
@post('/github')
def github():
	usuario = request.forms.get('usuario')
	passw = request.forms.get('password')
	repo = request.forms.get('repo')
	s = request.environ.get('beaker.session')
	s.save()
	g = Github(usuario,passw)
	g.get_user().create_repo(repo)
	redirect ('http://192.168.1.110:8080/git/'+ usuario +'/' +repo)

@get('/git/<usuario>/<repo>')
def git(usuario,repo):
	s = request.environ.get('beaker.session')
	s.save()
	commands.getoutput('sudo cd /home/users/'+s["sesion"][1]+' && git clone git@github.com:'+usuario+'/'+repo)
	return template('git.tpl', repo = repo, usuario = usuario)

#Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(app=app,host='192.168.1.110', port=8080)
