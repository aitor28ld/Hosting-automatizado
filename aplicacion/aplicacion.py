#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, app, route, run, request, template, default_app, static_file, get, post, response, redirect
import commands
import json
import getpass
from ldap3 import Server, Connection, ALL
from beaker.middleware import SessionMiddleware
from github import Github

# Sesiones de usuarios con tiempo de 5 min guardados en memoria
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

# Definimos el usuario y su contraseña para iniciar una conexión con el servicio LDAP
usuario = "cn=admin,dc=spotype,dc=com"
# Cambiar contraseña para no tener que ponerla transparente
password = 'root'

server = Server("192.168.1.110", get_info=ALL)
conn = Connection(server, usuario, password, auto_bind=True)

# Inicio de la aplicación
@route('/')
def raiz():
	s = request.environ.get('beaker.session')
	#Si existe una sesión, se entra en ella, sino entra cómo anonimo
	if s.has_key('sesion'):
		return template('index-sesion.tpl',usuario=s["sesion"][1])
	else:
		return template('index.tpl')

# Creación de usuarios
# Este route contiene la plantilla dónde el usuario introducirá sus datos
@route('/registro')
def registro():
	return template('registro.tpl')

# Cogemos los datos desde la plantilla y los guardamos en variables para despues, con REDIRECT,
# enviarlo y así crearle el usuario
@post('/sesion')
def sesion():
	usuario = request.forms.get('usuario')
	password = request.forms.get('password')
	email = request.forms.get('email')
	nombre = request.forms.get('nombre')
	apeuno = request.forms.get('apeuno')
	apedos = request.forms.get('apedos')
	ssh = request.forms.get('ssh')
	usuariogit = request.forms.get('usuariogit')
	con = request.forms.get('contra')
	# Guardamos la clave ssh en la sesión del usuario
	s = request.environ.get('beaker.session')
	s["ssh"] = [ssh]
	# Guardamos los datos de github en la sesión del usuario
	s["repos"] = [usuariogit, con]
	s["github"] = [usuariogit, con]
	s.save()
	redirect ('http://192.168.1.110:8080/prueba/'+usuario+'/'+password+'/'+email+'/'+nombre+'/'+apeuno+'/'+apedos)
	
# Con rutas dinámicas, guardamos los datos y procedemos a realizar la petición al servicio LDAP 
# para crear el usuario
@route('/prueba/<usuario>/<password>/<email>/<nombre>/<apeuno>/<apedos>')
def prueba(usuario,password,email,nombre,apeuno,apedos):
	s = request.environ.get('beaker.session')
	numuid = []
	numuid.append(commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uidNumber=*)" | grep uidNumber | grep -v "# filter"'))
	if numuid[0] != "":
		for i in numuid:
			num2 = i.split("\n")
			num3 = int(max(num2).split(": ")[1])+1
			uid = "uid="+usuario+",ou=People,dc=spotype,dc=com"
			objectclass = ["inetOrgPerson","posixAccount","person","top","ldapPublicKey"]
			atributos = {"cn":nombre+" "+apeuno+" "+apedos,"sn":apeuno+" "+apedos,"userPassword":password,"mail":email,"uid":usuario,"uidNumber":num3 ,"gidNumber":num3 ,"homeDirectory":"/home/users/"+usuario,"sshPublicKey": s["ssh"]}
			conexion = conn.add(uid,objectclass,atributos)
	
			# Si la conexión se ha establecido y ha creado al usuario, le creamos su directorio y le damos sus 
			# correspondientes permisos, sino se le envía una alerta de error
			if conexion == True:
				commands.getoutput('sudo mkdir /home/users/'+usuario)
				uid = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" uidNumber |grep uid | tail -1 |cut -d: -f2')
				uid = uid.split(" ")[1]
				commands.getoutput('sudo chown '+uid+' /home/users/'+usuario)
				commands.getoutput('sudo mkdir /home/users/'+usuario+'/.ssh/')
				commands.getoutput('sudo chgrp -R usuario /home/users/'+usuario+'/')
				commands.getoutput('sudo chmod -R 770 /home/users/'+usuario)
				commands.getoutput('echo "'+s["ssh"][0]+'" > /home/users/'+usuario+'/.ssh/id_rsa.pub')
				commands.getoutput('sudo chmod 700 /home/users/'+usuario+'/.ssh/id_rsa.pub')
				return template('sesion-valida.tpl', usuario=usuario)
				#break
			else:
				return template('sesion-error.tpl', usuario=usuario)
				#break
	else:
		uid = "uid="+usuario+",ou=People,dc=spotype,dc=com"
		objectclass = ["inetOrgPerson","posixAccount","person","top","ldapPublicKey"]
		atributos = {"cn":nombre+" "+apeuno+" "+apedos,"sn":apeuno+" "+apedos,"userPassword":password,"mail":email,"uid":usuario,"uidNumber":20000 ,"gidNumber":20000,"homeDirectory":"/home/users/"+usuario,"sshPublicKey": s["ssh"]}
		conexion = conn.add(uid,objectclass,atributos)
	
		# Si la conexión se ha establecido y ha creado al usuario, le creamos su directorio y le damos sus 
		# correspondientes permisos, sino se le envía una alerta de error
		if conexion == True:
			commands.getoutput('sudo mkdir /home/users/'+usuario)
			uid = commands.getoutput('ldapsearch -x -w root -D "cn=admin,dc=spotype,dc=com" "(uid='+usuario+')" uidNumber |grep uid | tail -1 |cut -d: -f2')
			uid = uid.split(" ")[1]
			commands.getoutput('sudo chown '+uid+' /home/users/'+usuario)
			commands.getoutput('sudo mkdir /home/users/'+usuario+'/.ssh/')
			commands.getoutput('sudo chgrp -R usuario /home/users/'+usuario+'/')
			commands.getoutput('sudo chmod -R 770 /home/users/'+usuario)
			commands.getoutput('echo "'+s["ssh"][0]+'" > /home/users/'+usuario+'/.ssh/id_rsa.pub')
			commands.getoutput('sudo chmod 700 /home/users/'+usuario+'/.ssh/id_rsa.pub')
			return template('sesion-valida.tpl', usuario=usuario)
		else:
			return template('sesion-error.tpl', usuario=usuario)

# Logueos de usuarios
@route('/inicio')
def inicio():
	return template('inicio.tpl')

@post('/login')
def login():
	# Abrimos la sesión del usuario
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
			# Añadimos la plantilla y el usuario a la sesión para después devolverla y enviarle el usuario
			s['sesion'] = ['login-ok.tpl',usuario]
			s.save()
			return template(s['sesion'][0], usuario=s['sesion'][1])
		else:
			return template ('login-error.tpl')
	else:
		return template ('login-error.tpl')

# Perfil de usuarios
@get('/perfil')
def perfil():
	s = request.environ.get('beaker.session')
	return template('perfil.tpl', usuario=s['sesion'][1])
	
# Subir CMS con repositorio
@get('/web')
def web():
	s = request.environ.get('beaker.session')
	if s.has_key('github'):
		return template('web-git.tpl')
	else:
		return template('web.tpl')
	
@post('/githubok')
def github():
	repo = request.forms.get('repo')
	s = request.environ.get('beaker.session')
	s["github"].append(repo)
	s.save()
	# Logueo en Github
	g = Github(s["github"][0],s["github"][1])
	# Creamos el repositorio en Github
	g.get_user().create_repo(s["github"][2])
	redirect ('/git')

@post('/github')
def github():
	usuario = request.forms.get('usuario')
	passw = request.forms.get('password')
	repo = request.forms.get('repo')
	s = request.environ.get('beaker.session')
	s["github"] = [usuario,passw,repo]
	s.save()
	# Logueo en Github
	g = Github(usuario,passw)
	# Creamos el repositorio en Github
	g.get_user().create_repo(repo)
	redirect ('http://192.168.1.110:8080/git')

@get('/git')
def git():
	s = request.environ.get('beaker.session')
	# Clonamos el repositorio anteriormente creado
	commands.getoutput('cd /home/users/'+s["sesion"][1]+' && git clone https://github.com/'+s["github"][0]+'/'+s["github"][2]+'.git')
	# Creamos un fichero README.md en el repositorio
	commands.getoutput('sudo echo "#Repositorio creado con la aplicación de Aitor28ld" > /home/users/'+s["sesion"][1]+'/'+s["github"][2]+'/README.md')
	# Inicializamos el repositorio, añadimos el fichero y lo comentamos
	commands.getoutput('cd /home/users/'+s["sesion"][1]+'/'+s["github"][2]+' && git init && git add README.md && git commit -m "Repositorio creado satisfactoriamente" && git branch --unset-upstream')
	# Establecemos las credenciales de usuario y subimos los cambios del repositorio
	commands.getoutput('cd /home/users/'+s["sesion"][1]+'/'+s["github"][2]+' && git remote set-url origin https://'+s["github"][0]+':'+s["github"][1]+'@github.com/'+s["github"][0]+'/'+s["github"][2]+'.git && git push -u origin master')
	commands.getoutput('sudo chown usuario /etc/apache2/sites-* && sudo chmod -R o+rwx /home/users')
	commands.getoutput('touch /etc/apache2/sites-available/'+s["sesion"][1]+'.conf')
	commands.getoutput("""
	sudo echo '<VirtualHost *:80>
        ServerName """+s["sesion"][1]+""".spotype.com

        ServerAdmin webmaster@localhost
        DocumentRoot /home/users/"""+s["sesion"][1]+"""

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

	</VirtualHost>' > /etc/apache2/sites-available/"""+s["sesion"][1]+'.conf')
	commands.getoutput('cd /etc/apache2/sites-available && sudo a2ensite '+s["sesion"][1]+'.conf')
	commands.getoutput('sudo /etc/init.d/apache2 reload')
	commands.getoutput('sudo chown usuario /var/cache/bind/db.spotype')
	DNS = commands.getoutput('cat /var/cache/bind/db.spotype | grep '+s["sesion"][1])
	if DNS == "":
		commands.getoutput('sudo echo "'+s["sesion"][1]+' IN    CNAME    ansible" >> /var/cache/bind/db.spotype')
		return template('git.tpl', repo = s["github"][2], usuario = s["github"][0])
	else:
		return template('git.tpl', repo = s["github"][2], usuario = s["github"][0])

# Actualizar repositorios e ir directamente a la web del usuario
@get('/webs')
def webs():
	s = request.environ.get('beaker.session')
	# Si existe una sesión, se entra en ella, sino entra cómo anonimo
	if s.has_key('github'):
		return template('webs-git.tpl')
	else:
		return template('webs.tpl')
	
@post('/reposok')
def repos():
	s = request.environ.get('beaker.session')
	repositorio = request.forms.get('repositorio')
	if repositorio == s["github"][2]:
		redirect('/repositorios')
	else:
		return "Error de repositorio"

@post('/repos')
def reposok():
	s = request.environ.get('beaker.session')
	usuario = request.forms.get('usuario')
	con = request.forms.get('password')
	repositorio = request.forms.get('repositorio')
	s["repos"] = [usuario,con,repositorio]
	s.save()
	
	redirect('/repositorios')
	
@get('/repositorios')
def repositorios():
	s = request.environ.get('beaker.session')
	if s.has_key('github'):
		commands.getoutput('cd /home/users/'+s["sesion"][1]+'/'+s["github"][2]+' && git pull')
		redirect ('http://'+s["sesion"][1]+'.spotype.com')
	elif s.has_key('repos'):
		commands.getoutput('cd /home/users/'+s["sesion"][1]+'/'+s["repos"][2]+' && git pull')
		redirect ('http://'+s["sesion"][1]+'.spotype.com')
	else:
		return "Error de clave"

# Ir a la web directamente
@get('/page')
def page():
	s = request.environ.get('beaker.session')
	redirect('http://'+s["sesion"][1]+'.spotype.com')

# Eliminación de repositorios

# Eliminación de BD

# Eliminación de usuarios

# Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(app=app,host='192.168.1.110', port=8080)
