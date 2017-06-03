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

server = Server("{{ ansible_eth0.ipv4.address}}", get_info=ALL)
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
	redirect ('/prueba/'+usuario+'/'+password+'/'+email+'/'+nombre+'/'+apeuno+'/'+apedos)
	
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
				commands.getoutput('sudo mkdir -p /home/users/'+usuario)
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
	# Búsqueda de repositorio
	x = g.get_user().get_repos()
	# Filtrado de repositorios existentes
	p = [l.name for l in x if l.name == s["github"][2] ]
	if s["github"][2] in p:
		return template('error-git.tpl', creacion = s["github"][2])		
	else:
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
	x = g.get_user().get_repos()
	p = [l.name for l in x if l.name == s["github"][2] ]
	if s["github"][2] in p:
                return template('error-git.tpl', creacion = s["github"][2])
        else:
                # Creamos el repositorio en Github
                g.get_user().create_repo(s["github"][2])
                redirect ('/git')

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
		commands.getoutput('sudo echo "'+s["sesion"][1]+' IN    CNAME   debian" >> /var/cache/bind/db.spotype')
		commands.getoutput('sudo rndc flush && sudo /etc/init.d/bind9 restart')
		return template('git.tpl', repo = s["github"][2], usuario = s["github"][0])
	else:
		commands.getoutput('sudo rndc flush && sudo /etc/init.d/bind9 restart')
		return template('git.tpl', repo = s["github"][2], usuario = s["github"][0])

# Actualizar repositorios e ir directamente a la web del usuario
@get('/webs')
def webs():
	s = request.environ.get('beaker.session')
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
		return template ('err-repo.tpl')

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
		return template('err-key.tpl')

# Ir a la web directamente
@get('/page')
def page():
	s = request.environ.get('beaker.session')
	redirect('http://'+s["sesion"][1]+'.spotype.com')

# Crear BD
@get('/mysql')
def crearmysql():
	return template ('crear-mysql.tpl')

@post('/crearmysql')
def mysql():
	usuario = request.forms.get('user')
	contras = request.forms.get('contras')
	nombrebd = request.forms.get('bd')
	# Creamos el fichero que después será inyectado a mysql
	commands.getoutput('echo \#\!/bin/bash > /home/usuario/bd.sh && sudo chmod u+x /home/usuario/bd.sh')
	commands.getoutput("""echo "create user """+usuario+"""@localhost identified by '"""+contras+"""';" >> /home/usuario/bd.sh""")
	commands.getoutput('''echo "create database '''+nombrebd+''';" >> /home/usuario/bd.sh ''')
	commands.getoutput("""echo "grant all privileges on """+nombrebd+""".* to """+usuario+"""@localhost identified by '"""+contras+"""' with grant option;" >> /home/usuario/bd.sh""")
	commands.getoutput('mysql -u root -proot < /home/usuario/bd.sh')
	return template('mysql.tpl', nombrebd = nombrebd, usuario = usuario)

# Administrar BD con phpmyadmin
@get('/phpmyadmin')
def phpmyadmin():
	redirect ('http://phpmyadmin.spotype.com')

# Eliminación de repositorios
@get('/delweb')
def delweb():
	return template('delweb.tpl')

@post('/delgit')
def delgit():
	s = request.environ.get('beaker.session')
	rep = request.forms.get('repo')
	# Dependiendo de la sesión iniciada por el usuario, devolverá una u otra con sus datos, sino,
	# dará error
	if s.has_key('github'):
		g = Github(s['github'][0],s['github'][1])
		g.get_user().get_repo(s['github'][2]).delete()
		return template ('delgit.tpl')
	elif s.has_key('repos'):
		g = Github(s['repos'][0],s['repos'][1])
		g.get_user().get_repo(s['repos'][2]).delete()
		return template ('delgit.tpl')
	else:
		return template ('no-sesion.tpl')

# Eliminación de BD
@get('/delbd')
def defbd():
	return template('delbd.tpl')

@post('/deletebd')
def deletebd():
	# Guardamos el usuario y el nombre de la BD para luego, mediante un fichero, inyectarlo a
	# mysql y así permitir la eliminación del usuario y BD
	usuario = request.forms.get('user')
	nombrebd = request.forms.get('bd')
	commands.getoutput('echo \#\!/bin/bash > /home/usuario/delbd.sh && sudo chmod u+x /home/usuario/delbd.sh')
	commands.getoutput("""echo "drop user """+usuario+"""@localhost;" >> /home/usuario/delbd.sh""")
	commands.getoutput("""echo "drop database """+nombrebd+""";" >> /home/usuario/delbd.sh""")
	commands.getoutput('mysql -u root -proot < /home/usuario/delbd.sh')
	
	return template ('deletebd.tpl', usuario = usuario, bd = nombrebd)

# Eliminación de usuarios
@get('/delaccount')
def delaccount():
	s = request.environ.get('beaker.session')
	usuario = s['sesion'][1]
	conn.delete("uid="+s["sesion"][1]+",ou=People,dc=spotype,dc=com")
	commands.getoutput("sudo sed '/"+s["sesion"][1]+"/d' /var/cache/bind/db.spotype -i")
	commands.getoutput("cd /etc/apache2/sites-available && sudo a2dissite "+s["sesion"][1]+".conf")
	commands.getoutput("sudo /etc/init.d/apache2 reload")
	# Eliminamos la sesión que el usuario tiene abierta
	s.delete()
	return template ('delacc.tpl', usuario = usuario)
	

# Ficheros estáticos
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(app=app,host="{{ ansible_eth0.ipv4.address }}", port=8080)
