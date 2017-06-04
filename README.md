# Documentación sobre el contenido del repositorio y cómo funciona
***
*Autor:* Aitor León

*Creado:* 04/06/2017

*Contacto:*

- Twitter: @2ait8r
- E-mail: ldaitor28@gmail.com
***
# Hosting automatizado con autenticación en LDAP
***
## Indice
1. Introducción
  1. Descripción del proyecto
  2. Objetivos a alcanzar
2. Software a utilizar
	1. Ansible
		1. ¿Qué es Ansible?
		2. ¿Por qué utilizar Ansible?
	2. Bottle
		1. ¿Qué es Bottle?
		2. ¿Por qué Bottle y no Django?
	3. LDAP
		1. ¿Qué es LDAP?
3. Instalación del software necesario con Ansible y control de versiones
	1. Instalación y configuración del DNS con Ansible
	2. Instalación y configuración del Servidor Web con Ansible
	3. Instalación y configuración de la base de datos con Ansible
	4. Instalación y configuración del servicio Ldap con Ansible
	5. Pruebas de funcionamiento
		1. Servicio DNS (Bind9)
		2. Servidor Web (Apache2)
		3. Base de datos (MySQL)
		4. Servicio Ldap
4. Creación de la aplicación en Bottle
	1. Instalación de los paquetes y aplicaciones necesarias
	2. Beaker y PyGithub
		1. ¿Qué es Beaker?
		2. ¿Qué es PyGithub?
	3. Creación de la aplicación de Bottle paso a paso
		1. Creación de usuarios en LDAP y verificación de dichos usuarios
		2. Inicio de sesión de usuarios ya registrados
		3.  Perfiles de usuarios
		4.  Creación de repositorios con subida de ficheros iniciales
		5.  Actualización de repositorios o directos a la web del usuario
		6.  Creación de bases de datos en mysql
		7.  Administración por phpmyadmin de las bases de datos
		8.  Eliminación de repositorios creados
		9.  Eliminación de base de datos
		10.  Eliminación de usuarios
5. Despliegue de la aplicación de Bottle con Ansible
6. Referencias

***
# Introducción

Para la realización de este proyecto utilizaremos, en mayor medida, Ansible y Bottle. A continuación realizaremos unas pequeñas introducciones para Ansible y Bottle.

## Descripción del proyecto
La descripción del proyecto es ofrecer servicios de Hosting a clientes, los cuales podrán crearse una cuenta a través de la interfaz que se ubicarán en usuarios del servicio LDAP. 

Una vez iniciada sesión, el usuario podrá realizar acciones cómo:
- Darse de baja
- Administrar su base de datos.
- Crear repositorios
- Subir ficheros
- etc.

Las acciones que podrá realizar serán lanzadas por Playbooks de Ansible.

## Objetivos a alcanzar

El objetivo del proyecto consiste en, a través de la interfaz web con una aplicación en Bottle o Django, lanzamos las instrucciones disponibles en la interfaz mediante Playbooks de Ansible.
El usuario, el cual estará creado en nuestro servicio LDAP y autenticado con la librería de Python, podrá subir sus ficheros a través de una cuenta Github clonada a su directorio Home especificada en su cuenta de LDAP.

Si se dispone de tiempo, se puede realizar una ampliación añadiendo Balanceadores de carga a los servidores para ofrecer una buena disponibilidad de los servicios ofrecidos a los usuarios.

# Software a utilizar

## Ansible

### ¿Qué es Ansible?

Ansible es una herramienta de configuración informática que puede configurar sistemas, desplegar software y orquestar más tareas avanzadas así cómo despliegue continuo o actualizaciones sucesivas.

###¿Por qué utilizar Ansible?
Diseñado para despliegue a diferentes niveles desde el principio, Ansible modela tu infraestructura informática describiendo como interactúan todos tus sistemas, en lugar de sólo administrar un sistema a la vez.

Algunos motivos por lo que vamos a utilizar Ansible:

__Arquitectura eficiente__

Ansible trabaja conectándose a tus nodos y lanzando pequeños programas llamados “módulos”. Esos programas están escritos para ser modelos de recursos del estado del sistema. Ansible los ejecuta sobre SSH por defecto, y borra cuando han finalizado.

Tus librerías de módulos pueden residir en cualquier máquina y sin requerir de servidores, demonios, o bases de datos.

__Administra tu inventario en simples ficheros de texto__

Por defecto, Ansible representa qué máquinas son administradas usando un simple fichero INI que pone todas tus máquinas administradas en grupos, a tu propia elección.

Una vez que la lista de máquinas está definida, podemos asignarles variables en simples ficheros de textos.

__Playbooks: un lenguaje simple y potente de automatización__

Playbooks pueden orquestar finamente múltiples partes de la topologia de tu infraestructura, con detallado control sobre cuantas máquinas podemos abordar al mismo tiempo. Aquí es dónde Ansible comienza a ser más interesante.

## Bottle
### ¿Qué es Bottle?

Bottle es un rápido, simple y ligero micro-framework WSGI para Python. Distribuido cómo un único modulo y sin otras dependencias que la de la estándar de Python.

Bottle tiene las siguientes funcionalidades, y son muy simples de aprender:

- Routing: peticiones de mapeo a funciones con soporte para URLs limpias y dinámicas.
- Templates: plantillas rápidas y creadas para Python, construidas y soportadas para Mako, Jinja2 y Cheetah
- Utilidades: acceso conveniente a datos de formularios, subida de ficheros, cookies, encabezados y otros metadatos relacionados con el protocolo HHTP.
- Servidor: desarrollado en HTTP y soporte para Paste, Fapws3, Bjoern, Gae, Cherrypy o cualquier otro servidor HTTP capaz de soportar WSGI.

### ¿Por qué Bottle y no Django?
La respuesta en simple, en mi caso usaría Django para la realización de este proyecto . Pero, viendo el tiempo de aprendizaje mínimo que se le debe dar a Django comparado con el tiempo que se le debe dar a Bottle y teniendo en cuenta que con Django debería de empezar de cero, es decir, no tengo una mínima base sobre cómo funciona la estructura de Django, debo de elegir Bottle con el cual ya tengo una base e idea de cómo funciona su estructura.

## LDAP

### ¿Qué es LDAP?
LDAP son las siglas de Ligthweight Directory Access Protocol o en español Protocolo Ligero de Acceso a Directorios y que, a nivel de aplicación, nos permitirá el acceso al servicio de directorio ordenado y distribuido para buscar diversa información en nuestro entorno de red.

Su implementación en este proyecto servirá para que los usuarios tengan acceso a su directorio, asignado en local y sincronizado con los repositorios de su cuenta en Github.


# Instalación del software necesario con Ansible y control de versiones
Antes de proceder a crear los playbooks de ansible con la instalación del software necesario, deberemos instalar Ansible, para ello ejecutamos:

    apt update && apt upgrade -y
    apt install ansible


Procedemos a crear los ficheros de configuración de ansible, para ello creamos un directorio y sus respectivos ficheros con su contenido:

    mkdir ansible
    nano ansible.cfg
    [defaults]
    hostfile = ansible_hosts
    remote_user = usuario
    
    nano ansible_hosts
    [proyecto]
    debian ansible_ssh_host=192.168.1.106
    

Antes de probar cualquier conexión, nos aseguramos que el host objetivo tiene instalado openssh-server con:

    aptitude search openssh-server

Al probar la conectividad, nos dará fallo ya que no utilizaremos clave publica, así que deberemos de indicarle que nos pregunte la contraseña del usuario con el parámetro –ask-pass tal y cómo vemos en el siguiente ejemplo:

    usuario@debian:~/git/Proyecto/ansible$ ansible proyecto -m ping –ask-pass
    SSH password: 
    debian | success >> {
    "changed": false, 
    "ping": "pong"
    }


También deberemos de meter el usuario a utilizar en el sudo. Para ello instalamos sudo y añadimos la siguiente linea:

	apt install sudo
	nano /etc/sudoers
	usuario ALL=(ALL:ALL) NOPASSWD: ALL

Ahora que tenemos conexión, procedemos a crear un playbook con roles. Los roles de un playbook de Ansible funcionan de la manera expuesta a continuación.

Definimos los roles en el playbook:
<pre>
--
- hosts: proyecto
  roles:
    - actualizacion
</pre>

Hasta ahora sólo hemos definido un rol. En la ubicación dónde está el fichero .yml, creamos un directorio llamado roles y dentro de el ,los directorios de los roles que llamaremos desde el playbook los cuales contienen o podrían contener los siguientes directorios:

- tasks
- Handlers
- vars
- defaults
- meta
- etc

Un ejemplo de ello, con sólo tareas a realizar:

	usuario@debian:~/git/Proyecto/ansible/roles$ tree
	.
	└── actualizacion
	    └── tasks
        	└── main.yml

El fichero main es el que contiene las ordenes a ejecutar, en mi caso son las siguientes ordenes sencillas:

	usuario@debian:~/git/Proyecto/ansible/roles$ cat actualizacion/tasks/main.yml
 
	- name: actualización del sistema
	  apt: upgrade=yes update_cache=yes

Probamos que funciona correctamente:
	usuario@debian:~/git/Proyecto/ansible$ ansible-playbook principal.yml –ask-pass
	SSH password: 

	PLAY [proyecto] *************************************************************** 

	GATHERING FACTS *************************************************************** 
	ok: [debian]

	TASK: [actualizacion | actualización del sistema] ***************************** 
	changed: [debian]

	PLAY RECAP ******************************************************************** 
	debian                     : ok=2    changed=1    unreachable=0    failed=0 


# Instalación y configuración del DNS con Ansible

Procedemos a realizar la instalación y configuración del servidor DNS con bind9 mediante ansible creando la siguiente estructura:

	usuario@debian:~/git/Proyecto/ansible$ tree roles/dns/
	roles/dns/
	├── handlers
	│ └── main.yml
	├── tasks
	│ └── main.yml
	└── templates
	    ├── db.192.168.1
	    ├── db.spotype
	    ├── named.conf.local
	    └── resolv.conf

Dónde templates contiene los ficheros, de la configuración principal, que serán copiados a sus correspondientes rutas en la máquina destino, handlers contiene la notificación y tarea de reiniciar el servicio una vez esté configurado y task las tareas a realizar con el rol DNS

Y con el siguiente contenido en los mains:

__tasks/main.yml__

	# Instalamos Bind9
	- name: instalación del servicio de DNS
  	apt:
	    name: bind9
	    state: present
	
	# Copiamos los ficheros principales de configuración ubicados en ../templates/ para tener configurado Bind9

	- name: Copiando configuración local
  	  template: > 
	    src=named.conf.local 
	    dest=/etc/bind/named.conf.local
	    owner=root
	    group=root
	    mode=0644

    - name: Copiando resolución directa
      template: >
        src=db.spotype 
    	dest=/var/cache/bind/db.spotype
    	owner=root
    	group=root
    	mode=0644
    
    - name: Copiando resolución inversa
      template: >
    	src=db.192.168.1 
    	dest=/var/cache/bind/db.192.168.1
    	owner=root
    	group=root
    	mode=0644
    
    - name: Copiando resolv.conf
      template: > 
    	src=resolv.conf
    	dest=/etc/resolv.conf
    	owner=root
    	group=root
    	mode=0644
    
    # Damos los correspondientes permisos a los ficheros copiados y notificamos al handler el reinicio del servicio
    
    - name: Reiniciando DNS con handler
      command: /bin/true
      notify: Reinicio del servicio DNS (bind9)
    
__handlers/main.yml__

    - name: Reinicio del servicio DNS (bind9)
      service:
        name: bind9
      	state: restarted
  
A continuación veremos el contenido de los ficheros de Templates, dichos ficheros contienen variables del host objetivo dónde se instalarán y copiaran los ficheros. Si queremos ver las variables que el host objetivo tiene, ejecutamos el siguiente comando desde la posición de los ficheros ansible_hosts y ansible.cfg:

	ansible <host> -m setup
	
	debian | success >> {
	    "ansible_facts": {
        	"ansible_all_ipv4_addresses": [
	            "192.168.1.128"
        	], 
        	"ansible_all_ipv6_addresses": [
	            "fe80::a00:27ff:fe0c:1dfe"
        	], 
        	"ansible_architecture": "x86_64", 
        	"ansible_bios_date": "12/01/2006", 
        	"ansible_bios_version": "VirtualBox", 
        	"ansible_cmdline": {
            "BOOT_IMAGE": "/boot/vmlinuz-3.16.0-4-amd64", 
            	"quiet": true, 
            	"ro": true, 
            	"root": "UUID=7853e319-d806-4d2e-b970-f5af5038abe9"
        	}, 
	… (demasiadas variables)

Cómo podemos ver, se trata de un diccionario y podemos tratarlo cómo hacemos con python.

Contenido de las plantillas ubicadas en Templates:

__db.spotype:__

	$TTL    86400
	@       IN      SOA     {{ ansible_hostname }}.spotype.com. mail.spotype.com. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                          86400 )       ; Negative Cache TTL

	spotype.com.      IN      NS      {{ ansible_hostname }}.spotype.com.
	spotype.com.      IN      MX      10 correo.spotype.com.

	$ORIGIN spotype.com.
	{{ ansible_hostname }}		IN      A       {{ ansible_eth0.ipv4.address }}
	www         IN  CNAME   {{ ansible_hostname }}
	ldap		IN	CNAME	{{ ansible_hostname }}
	phpmyadmin	IN	CNAME	{{ ansible_hostname }}

__db.192.168.1:__

	$TTL    86400
	@       IN      SOA     {{ ansible_hostname }}.spotype.com. mail.spotype.com. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                          86400 )       ; Negative Cache TTL

	spotype.com.      IN      NS      {{ ansible_hostname }}.spotype.com.

	$ORIGIN 1.168.192.in-addr.arpa.
	{{ ansible_eth0["ipv4"]["address"].split(".")[3] }}       IN      PTR     {{ ansible_hostname }}.spotype.com.

__Resolv.conf:__

	nameserver {{ ansible_eth0.ipv4.address }}


## Instalación y configuración del Servidor Web con Ansible

Una vez tenemos instalado y configurado el servicio DNS con Bind9, procedemos a instalar y configurar el servidor web con Apache2, creando la siguiente estructura:

	Serweb/
	├── files
	│ ├── apache2.conf
	│ ├── phpmyadmin.conf
	│ └── spotype.conf
	├── handlers
	│ └── main.yml
	└── tasks
	    └── main.yml

Dónde files contiene la configuración del virtualhost principal, de phpmyadmin y de la configuración de apache2., handlers contiene la notificación y la tarea del reinicio del servicio y task las tareas a realizar cuando ejecutemos el playbook con ansible.
 
Contenido de los mains:

__task/main.yml__

	- name: instalación de apache, php5 y curl
  	  apt: name={{item}} state=installed
  	  with_items:
     	   - apache2
       	   - php5
       	   - php5-curl
	
	- copy:
	    src: spotype.conf
	    dest: /etc/apache2/sites-available/spotype.conf
	    owner: root
	    group: root
	    mode: 644

	- copy:
	    src: phpmyadmin.conf
    	dest: /etc/apache2/sites-available/phpmyadmin.conf
	    owner: root
	    group: root
	    mode: 644

	- copy:
    	src: apache2.conf
    	dest: /etc/apache2/apache2.conf
    	owner: root
    	group: root
    	mode: 0644

	- name: Deshabilitando el sitio por defecto
  	  shell: sudo a2dissite 000-default.conf

	- name: Habilitando el sitio de Spotype.com
  	  shell: sudo a2ensite spotype.conf
	
	- name: Habilitando el sitio de phpmyadmin
  	  shell: sudo a2ensite phpmyadmin.conf

	- name: Haibilitando modulos de apache2
  	  action: command a2enmod rewrite
  	  notify: reinicio del servicio de Apache

__handlers/main.yml__

	- name: reinicio del servicio de Apache
   	  service:
    	name: apache2
    	state: restarted

## Instalación y configuración de la base de datos con Ansible

Comienza la instalación y configuración un poco complicada. Nuestra base de datos que los usuarios utilizaran para subir sus CMS será MySQL. Su estructura de directorios es la siguiente:
	Bd/
	├── handlers
	│ └── main.yml
	├── tasks
	│ └── main.yml
	└── vars
    	└── main.yml

Dónde handlers contiene las notificaciones y la tarea de reiniciar el servicio de MySQL, tasks contiene las tareas a realizar y vars las variables que necesitará MySQL para su instalación y configuración.

El contenido de los mains es el siguiente:

__handlers/main.yml__

	- name: reinicio de MySQL
  	  service:
	    name: mysql
	    state: restarted

__tasks/main.yml__

	- name: Definiendo contraseña antes de instalar
  	  debconf: name='mysql-server' question='mysql-server/root_password' value='{{mysql_root_password | quote}}' vtype='password'

	- name: Confirmación de la contraseña de root
  	  debconf: name='mysql-server' question='mysql-server/root_password_again' value='{{mysql_root_password | quote}}' vtype='password'

	- name: Instalando MySQL Server/Client
  	  apt: name={{item}} state=installed 
  	  with_items:
           - mysql-server
       	   - mysql-client
       	   - python-mysqldb   
  	  notify: reinicio de MySQL

__vars/main.yml__

	mysql_root_password: "root"

## Instalación y configuración del servicio Ldap con Ansible

Sin duda esta es la parte más complicada, aunque cómo todo, debes de saber qué tocar.

Comenzamos creando la estructura del servicio LDAP:
	
	Ldap/
	├── defaults
	│ └── main.yml
	├── files
	│ ├── inicial.ldif
	│ ├── openssh-lpk.ldif
	│ └── openssh-lpk.schema
	├── handlers
	│ └── main.yml
	├── tasks
	│ └── main.yml
	├── templates
	│ ├── DB_CONFIG.j2
	│ ├── ldap.conf.j2
	│ ├── slapd.conf.j2
	│ └── slapd_defaults.j2
	└── vars
	    └── main.yml
	└── vars
	    └── main.yml

Dónde *defaults* contiene la configuración por defecto del servicio Ldap tanto para servidor cómo para cliente, *files* contiene la base de la base de datos de nuestro servicio Ldap, *handlers* contiene las notificaciones y la tarea de reinicio del servicio, *tasks* contiene todas las tareas a realizar en el servicio Ldap, *templates* contiene las plantillas de la base de datos, de la configuración del cliente ldap y del servidor y *vars* contiene las variables necesarias para el servicio.

Contenido de los mains es el siguiente:

__defaults/main.yml__

    #Configuración de las variables
    openldap_domain: spotype.com
    openldap_organization: spotype
    openldap_admin_password: root
    
    openldap_default_services: ldap:/// ldapi:///
    openldap_default_options: ""
    
    #Configuración del servidor
    openldap_server_schemas:
      - core
      - cosine
      - inetorgperson
      - openssh-lpk
      - nis
      - openssh-lpk
    openldap_server_loglevel: none
    openldap_server_modules:
      - back_hdb
    - syncprov
    openldap_server_database: hdb				#tipo de base de datos de Ldap
    openldap_server_suffix: dc=spotype,dc=com		#sufijo del servidor
    openldap_server_rootdn: cn=admin,dc=spotype,dc=com	#dn del servidor
    openldap_server_rootpw: root	#Contraseña del servidor, se encripta en el fichero resultante
    openldap_server_indexes:
      - objectClass,cn eq
      - entryCSN,entryUUID eq
    openldap_server_acls:
      - to attrs=userPassword by anonymous auth by self write by * none
      - to * by self write by * none
    openldap_server_password_hash: "{SSHA}"		#Tipo de cifrado de la contraseña
    
    openldap_dbconfig_set_cachesize: 2097152
    openldap_dbconfig_set_lk_max_objects: 1500
    openldap_dbconfig_set_lk_max_locks: 1500
    openldap_dbconfig_set_lk_max_lockers: 1500
    
    #Configuración del fichero /etc/ldap/ldap.conf
    openldap_client_uri: ldap://localhost				#URI del cliente en el servidor
    openldap_client_base: dc=spotype,dc=com			#Base del cliente
    openldap_client_binddn: cn=spotype,dc=spotype,dc=com	#Binddn del cliente en el servidor
    openldap_client_sizelimit: 0
    openldap_client_timelimit: 0
    
    openldap_sync_syncprov_checkpoint: 50 10
    openldap_sync_syncprov_sessionlog: 100
    
    openldap_sync_consumer: False
    openldap_sync_syncrepl_rid: 001
    openldap_sync_syncrepl_provider: ldap://ldap.example.com
    openldap_sync_syncrepl_type: refreshAndPersist
    openldap_sync_syncrepl_interval: 00:00:05:00
    openldap_sync_syncrepl_searchbase: "{{ openldap_server_suffix}}"
    openldap_sync_syncrepl_binddn: cn=admin,dc=spotype,dc=com
    openldap_sync_syncrepl_credentials: secret
    openldap_sync_syncrepl_starttls: "no"
    openldap_sync_syncrepl_retry: 60 +
    openldap_sync_syncrepl_bindmethod: simple
    openldap_sync_syncrepl_timeout: 0
    openldap_sync_syncrepl_network_timeout: 0
    openldap_sync_syncrepl_keepalive: 0:0:0
    openldap_sync_syncrepl_filter: (objectclass=*)
    openldap_sync_syncrepl_scope: sub
    openldap_sync_syncrepl_schemachecking: off

__handlers/main.yml__

	- name: reiniciando LDAP
  	  service: name=slapd state=restarted
  	  tags: openldap

__tasks/main.yml__

	- name: No autoconfigurar LDAP
  	  debconf: >
	    name=slapd
	    question='slapd/no_configuration'
	    value=true
	    vtype=boolean
  	  tags: openldap

	- name: Instalación de los paquetes necesarios LDAP
  	  apt: name={{ item }} state=present update_cache=yes
  	  with_items: openldap_packages
  	  environment: env
  	  tags: openldap
	
	- copy:
	    src: openssh-lpk.ldif
	    dest: /etc/ldap/schema/openssh-lpk.ldif
	    owner: root
	    group: root
	    mode: 0644
	
	- copy:
	    src: openssh-lpk.schema
	    dest: /etc/ldap/schema/openssh-lpk.schema
	    owner: root
	    group: root
	    mode: 0644
	
	- name: Creando configuración por defecto LDAP
  	  template: >
	    src=slapd_defaults.j2
    	dest={{ openldap_defaults_file }}
    	owner=root
    	group=root
    	mode=0644
  	  notify: reiniciando LDAP
  	  tags: openldap
	
	- name: Hasheando contraseña LDAP
  	  command: slappasswd -h {{ openldap_server_password_hash }} -s {{ openldap_server_rootpw }}
  	  register: rootpw
  	  tags: openldap

	- name: Creando configuración del servidor LDAP
  	  template: >
	    src=slapd.conf.j2
	    dest={{ openldap_server_configuration }}
	    owner=root
	    group=root
	    mode=0644
  	  notify: reiniciando LDAP
  	  tags: openldap

	- name: Creando configuración BD de LDAP
  	  template: >
	    src=DB_CONFIG.j2
	    dest={{ openldap_server_directory }}/DB_CONFIG
	    owner=openldap
	    group=openldap
	    mode=0600
  	  notify: reiniciando LDAP
  	  tags: openldap
	
	- name: Creando configuración del cliente LDAP
  	  template: >
	    src=ldap.conf.j2
	    dest={{ openldap_client_configuration }}
	    owner=root
	    group=root
	    mode=0644
	  	tags: openldap

	- name: Asegurando la activación del servicio LDAP al inicio
	  service: name=slapd state=started enabled=yes
  	  tags: openldap

	- copy:
	    src: inicial.ldif
    	dest: /etc/ldap/inicial.ldif
    	owner: root
    	group: root
    	mode: 0644
	
	- name: Creando esquema Openssh-lpk
  	  command: /bin/true
  	  notify: reiniciando LDAP
	
	- name: Creando una base para Openldap
  	  shell: ldapadd -x -D 'cn=admin,dc=spotype,dc=com' -w root -f /etc/ldap/inicial.ldif

__vars/main.yml__

	Env:
  	RUNLEVEL: 1
	
	openldap_packages:
  	- slapd
  	- ldap-utils
	
	openldap_defaults_file: /etc/default/slapd
	
	openldap_default_user: openldap
	openldap_default_group: openldap
	openldap_default_sentinel_file: /etc/ldap/noslapd
	
	openldap_server_pidfile: /var/run/slapd/slapd.pid
	openldap_server_argsfile: /var/run/slapd/slapd.args
	openldap_server_modulepath: /usr/lib/ldap
	openldap_server_directory: /var/lib/ldap
	openldap_server_configuration: /etc/ldap/slapd.conf
	openldap_client_configuration: /etc/ldap/ldap.conf
	
	openldap_schema_directory: /etc/ldap/schema
	
Ahora procedemos a mostrar el contenido de los ficheros restantes:

__files/inicial.ldif__

	dn: dc=spotype,dc=com
	objectClass: top
	objectClass: dcObject
	objectClass: organization
	dc: spotype
	o: Spotype S.L

	dn: ou=People,dc=spotype,dc=com
	ou: People
	objectClass: top
	objectClass: organizationalUnit

__files/openssh-lpk.ldif__

	dn: cn=openssh-lpk,cn=schema,cn=config
	objectClass: olcSchemaConfig
	cn: openssh-lpk
	olcAttributeTypes: ( 1.3.6.1.4.1.24552.500.1.1.1.13 NAME 'sshPublicKey'
  	DESC 'MANDATORY: OpenSSH Public key'
  	EQUALITY octetStringMatch
  	SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
	olcObjectClasses: ( 1.3.6.1.4.1.24552.500.1.1.2.0 NAME 'ldapPublicKey' SUP top $
  	DESC 'MANDATORY: OpenSSH LPK objectclass'
  	MAY ( sshPublicKey $ uid )
  	)

__files/openssh-lpk.schema__

	#
	# LDAP Public Key Patch schema for use with openssh-ldappubkey
	#                              useful with PKA-LDAP also
	#
	# Author: Eric AUGE <eau@phear.org>
	#
	# Based on the proposal of : Mark Ruijter
	#
	# octetString SYNTAX
	attributetype ( 1.3.6.1.4.1.24552.500.1.1.1.13 NAME 'sshPublicKey'
    	    DESC 'MANDATORY: OpenSSH Public key'
        	EQUALITY octetStringMatch
        	SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )

	# printableString SYNTAX yes|no
	objectclass ( 1.3.6.1.4.1.24552.500.1.1.2.0 NAME 'ldapPublicKey' SUP top AUXILIARY
        DESC 'MANDATORY: OpenSSH LPK objectclass'
        MUST ( sshPublicKey $ uid )
        )

**templates/DB_CONFIG.j2**

	set_cachesize 0 {{ openldap_dbconfig_set_cachesize }} 0
	set_lk_max_objects {{ openldap_dbconfig_set_lk_max_objects }}
	set_lk_max_locks {{ openldap_dbconfig_set_lk_max_locks }}
	set_lk_max_lockers {{ openldap_dbconfig_set_lk_max_lockers }}

__templates/ldap.conf.j2__

	# {{ ansible_managed }}

	URI {{ openldap_client_uri }}
	BASE {{ openldap_client_base }}

	SIZELIMIT {{ openldap_client_sizelimit }}
	TIMELIMIT {{ openldap_client_timelimit }}

	TLS_CACERT	/etc/ssl/certs/ca-certificates.crt

__templates/slapd.conf.j2__

	# {{ ansible_managed }}
	
	# Basics

	{% for schema in openldap_server_schemas %}
	include /etc/ldap/schema/{{ schema }}.schema
	{% endfor %}

	pidfile {{ openldap_server_pidfile }}
	argsfile {{ openldap_server_argsfile }}
	loglevel {{ openldap_server_loglevel }}

	password-hash {{ openldap_server_password_hash }}

	modulepath {{ openldap_server_modulepath }}
	{% for module in openldap_server_modules %}
	moduleload {{ module }}
	{% endfor %}

	# Database configuration

	database {{ openldap_server_database }}
	suffix "{{ openldap_server_suffix }}"
	rootdn "{{ openldap_server_rootdn }}"
	rootpw {{ rootpw.stdout }}
	directory {{ openldap_server_directory }}
	{% for index in openldap_server_indexes %}
	index {{ index }}
	{% endfor %}

	overlay syncprov
	syncprov-checkpoint {{ openldap_sync_syncprov_checkpoint }}
	syncprov-sessionlog {{ openldap_sync_syncprov_sessionlog }}

	{% if openldap_sync_consumer %}
	syncrepl rid={{ openldap_sync_syncrepl_rid }}
  	provider={{ openldap_sync_syncrepl_provider }}
  	bindmethod={{ openldap_sync_syncrepl_bindmethod }}
  	timeout={{ openldap_sync_syncrepl_timeout }}
	network-timeout={{ openldap_sync_syncrepl_network_timeout }}
  	binddn="{{ openldap_sync_syncrepl_binddn }}"
  	credentials="{{ openldap_sync_syncrepl_credentials }}"
  	keepalive={{ openldap_sync_syncrepl_keepalive }}
  	starttls={{ openldap_sync_syncrepl_starttls }}
  	filter="{{ openldap_sync_syncrepl_filter }}"
  	searchbase="{{ openldap_sync_syncrepl_searchbase }}"
  	scope={{ openldap_sync_syncrepl_scope }}
  	schemachecking={{ openldap_sync_syncrepl_schemachecking }}
  	type={{ openldap_sync_syncrepl_type }}
  	interval={{ openldap_sync_syncrepl_interval }}
  	retry="{{ openldap_sync_syncrepl_retry }}"
	{% endif %}

	# ACLs
	{% for acl in openldap_server_acls %}
	access {{ acl }}
	{% endfor %}


**templates/slapd_defaults.j2**

    # {{ ansible_managed }}
    
    # Default location of the slapd.conf file or slapd.d cn=config directory. If
    # empty, use the compiled-in default (/etc/ldap/slapd.d with a fallback to
    # /etc/ldap/slapd.conf).
    SLAPD_CONF=
    
    # System account to run the slapd server under. If empty the server
    # will run as root.
    SLAPD_USER="{{ openldap_default_user }}"
    
    # System group to run the slapd server under. If empty the server will
    # run in the primary group of its user.
    SLAPD_GROUP="{{ openldap_default_group }}"
    
    # Path to the pid file of the slapd server. If not set the init.d script
    # will try to figure it out from $SLAPD_CONF (/etc/ldap/slapd.d by
    # default)
    SLAPD_PIDFILE=
    
    # slapd normally serves ldap only on all TCP-ports 389. slapd can also
    # service requests on TCP-port 636 (ldaps) and requests via unix
    # sockets.
    # Example usage:
    # SLAPD_SERVICES="ldap://127.0.0.1:389/ ldaps:/// ldapi:///"
    SLAPD_SERVICES="{{ openldap_default_services }}"
    
    # If SLAPD_NO_START is set, the init script will not start or restart
    # slapd (but stop will still work).  Uncomment this if you are
    # starting slapd via some other means or if you don't want slapd normally
    # started at boot.
    #SLAPD_NO_START=1
    
    # If SLAPD_SENTINEL_FILE is set to path to a file and that file exists,
    # the init script will not start or restart slapd (but stop will still
    # work).  Use this for temporarily disabling startup of slapd (when doing
    # maintenance, for example, or through a configuration management system)
    # when you don't want to edit a configuration file.
    SLAPD_SENTINEL_FILE={{ openldap_default_sentinel_file }}
    
    # For Kerberos authentication (via SASL), slapd by default uses the system
    # keytab file (/etc/krb5.keytab).  To use a different keytab file,
    # uncomment this line and change the path.
    #export KRB5_KTNAME=/etc/krb5.keytab
    
    # Additional options to pass to slapd
    SLAPD_OPTIONS="{{ openldap_default_options }}"

## Pruebas de funcionamiento
Lanzamos el playbook y verificamos que no da errores:

    usuario@debian:~/git/Proyecto/ansible$ ansible-playbook principal.yml --ask-pass
    SSH password: 
    
    PLAY [proyecto] *************************************************************** 
    
    GATHERING FACTS *************************************************************** 
    ok: [debian]
    
    TASK: [actualizaciones | actualización del sistema] *************************** 
    changed: [debian]
    
    TASK: [serweb | instalación de apache, php5 y curl] *************************** 
    changed: [debian]
    
    TASK: [serweb | copy ] ******************************************************** 
    changed: [debian]
    
    TASK: [serweb | copy ] ******************************************************** 
    changed: [debian]
    
    TASK: [serweb | copy ] ******************************************************** 
    changed: [debian]
    
    TASK: [serweb | Deshabilitando el sitio por defecto] ************************** 
    changed: [debian]
    
    TASK: [serweb | Habilitando el sitio de Spotype.com] ************************** 
    changed: [debian]
    
    TASK: [serweb | Habilitando el sitio de phpmyadmin] *************************** 
    changed: [debian]
    
    TASK: [serweb | Haibilitando modulos de apache2] ****************************** 
    changed: [debian]
    
    TASK: [bd | Definiendo contraseña antes de instalar] ************************** 
    changed: [debian]
    
    TASK: [bd | Confirmación de la contraseña de root] **************************** 
    changed: [debian]
    
    TASK: [bd | Instalando MySQL Server/Client] *********************************** 
    changed: [debian]
    
    TASK: [ldap | No autoconfigurar LDAP] ***************************************** 
    changed: [debian]
    
    TASK: [ldap | Instalación de los paquetes necesarios LDAP] ******************** 
    changed: [debian] => (item=slapd,ldap-utils)
    
    TASK: [ldap | copy ] ********************************************************** 
    changed: [debian]
    
    TASK: [ldap | copy ] ********************************************************** 
    changed: [debian]
    
    TASK: [ldap | Creando configuración por defecto LDAP] ************************* 
    changed: [debian]
    
    TASK: [ldap | Hasheando contraseña LDAP] ************************************** 
    changed: [debian]
    
    TASK: [ldap | Creando configuración del servidor LDAP] ************************ 
    changed: [debian]
    
    TASK: [ldap | Creando configuración BD de LDAP] ******************************* 
    changed: [debian]
    
    TASK: [ldap | Creando configuración del cliente LDAP] ************************* 
    changed: [debian]
    
    TASK: [ldap | Asegurando la activación del servicio LDAP al inicio] *********** 
    changed: [debian]
    
    TASK: [ldap | copy ] ********************************************************** 
    changed: [debian]
    
    TASK: [ldap | Creando esquema Openssh-lpk] ************************************ 
    changed: [debian]
    
    TASK: [ldap | Creando una base para Openldap] ********************************* 
    changed: [debian]
    
    TASK: [dns | instalación del servicio de DNS] ********************************* 
    changed: [debian]
    
    TASK: [dns | Copiando configuración local] ************************************ 
    changed: [debian]
    
    TASK: [dns | Copiando resolución directa] ************************************* 
    changed: [debian]
    
    TASK: [dns | Copiando resolución inversa] ************************************* 
    changed: [debian]
    
    TASK: [dns | Copiando resolv.conf] ******************************************** 
    changed: [debian]
    
    TASK: [dns | Configurando permisos del servicio DNS] ************************** 
    changed: [debian]
    
    NOTIFIED: [serweb | reinicio del servicio de Apache] ************************** 
    changed: [debian]
    
    NOTIFIED: [bd | reinicio de MySQL] ******************************************** 
    changed: [debian]
    
    NOTIFIED: [ldap | reiniciando LDAP] ******************************************* 
    changed: [debian]
    
    NOTIFIED: [dns | Reinicio del servicio DNS (bind9)] *************************** 
    changed: [debian]
    
    PLAY RECAP ******************************************************************** 
    debian : ok=54   changed=50   unreachable=0failed=0 

Ahora procedemos a verificar las instalaciones y configuraciones realizadas.

### Servicio DNS (Bind9)

    usuario@debian:~/git/Proyecto/ansible$ dig @192.168.1.110 -t ns spotype.com
    
    ; <<>> DiG 9.9.5-9+deb8u8-Debian <<>> @192.168.1.110 -t ns spotype.com
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 3617
    ;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 2
    
    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 4096
    ;; QUESTION SECTION:
    ;spotype.com.			IN	NS
    
    ;; ANSWER SECTION:
    spotype.com.		86400	IN	NS	ansible.spotype.com.
    
    ;; ADDITIONAL SECTION:
    ansible.spotype.com.	86400	IN	A	192.168.1.110
    
    ;; Query time: 1 msec
    ;; SERVER: 192.168.1.110#53(192.168.1.110)
    ;; WHEN: Mon May 01 13:06:18 CEST 2017
    ;; MSG SIZE  rcvd: 78


### Servidor Web (Apache2)

![Servidor Web](http://imgur.com/aBsXvcS "Funcionamiento")

### Base de datos (MySQL)

    usuario@ansible:/etc/ldap# mysql -u root -p
    Enter password: 
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 37
    Server version: 5.5.55-0+deb8u1 (Debian)
    
    Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.
    
    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql> 

### Servicio Ldap

    usuario@ansible:~$ sudo slapcat
    dn: dc=spotype,dc=com
    objectClass: top
    objectClass: dcObject
    objectClass: organization
    dc: spotype
    o: Spotype S.L
    structuralObjectClass: organization
    entryUUID: 6db6b4de-c2a9-1036-9757-137ad14b1adb
    creatorsName: cn=admin,dc=spotype,dc=com
    createTimestamp: 20170501110236Z
    entryCSN: 20170501110236.332733Z#000000#000#000000
    modifiersName: cn=admin,dc=spotype,dc=com
    modifyTimestamp: 20170501110236Z
    contextCSN: 20170501110236.372020Z#000000#000#000000
    
    dn: ou=People,dc=spotype,dc=com
    ou: People
    objectClass: top
    objectClass: organizationalUnit
    structuralObjectClass: organizationalUnit
    entryUUID: 6dbcb37a-c2a9-1036-9758-137ad14b1adb
    creatorsName: cn=admin,dc=spotype,dc=com
    createTimestamp: 20170501110236Z
    entryCSN: 20170501110236.372020Z#000000#000#000000
    modifiersName: cn=admin,dc=spotype,dc=com
    modifyTimestamp: 20170501110236Z

#Creación de la aplicación en Bottle

## Instalación de los paquetes y aplicaciones necesarias

Para poder crear la aplicación de bottle con python, necesitaremos un editor de texto, en mi caso usaré Geany.
Para instalar Geany tenemos que actualizar la lista de repositorios:

	apt update && apt upgrade -y

Instalamos Geany:

	apt install geany -y

Lo siguiente será instalar bottle, un framework de python:

	apt install python-bottle -y

Para que las librerías importadas de ldap3 funcionen correctamente, instalaremos el paquete setuptools:

	apt install python-setuptools
 
Cómo en la aplicación realizaremos búsquedas y peticiones al servicio de LDAP, deberemos instalar su librería desde este repositorio de [github](https://github.com/cannatag/ldap3):

	su
	unzip ldap3-master.zip
	cd ldap3-master
	python setup.py install

Necesitaremos de la aplicación git para poder realizar clonaciones de repositorios:

	apt install git

Para las sesiones de usuarios, nos ayudaremos de Beaker:

	apt install python-beaker

Necesitaremos instalar PyGithub para poder loguearnos, clonar y pushear los repositorios, nos la descargamos desde su [repositorio oficial](https://github.com/PyGithub/PyGithub) y la instalamos:

	unzip PyGithub-master.zip
	cd  PyGithub-master
	python setup.py install

Ahora procederé a explicar qué son Beaker y PyGithub.

NOTA: la instalación y descompresión de los paquetes se hará automáticamente por ansible en la tarea que luego definiremos.

## Beaker y PyGithub

### ¿Qué es Beaker?

Beaker es una librería para guardar en caché y para usar sesiones en una aplicación web y scripts de Python. Por defecto, viene con WSGI Middleware para un fácil uso con aplicaciones basadas en WSGI (en nuestro caso Bottle) para aplicaciones basadas en Python.

En nuestro caso usaremos Beaker para guardar las sesiones que los usuarios abriran. Dichas sesiones tienen diferentes opciones de uso, las cuales puedes encontrar sus definición de uso en [este enlace](https://beaker.readthedocs.io/en/latest/configuration.html#options-for-sessions-and-caching)

En mi caso usaré la opción para sesiones y caché llamada Type. Este tipo de opción nos permite almacenar las sesiones o los objetos de caché.

Los diferentes modos que soporta son:

- file
- dbm
- memory
- ext:memcached
- ext:database
- ext:google

Nosotros usaremos la siguiente configuración en nuestra aplicación:

	session_opts = {
	    'session.type': 'memory',
	    'session.cookie_expires': 300,
	    'session.auto': True
	}

Dichas opciones son para:

- session.type: memory → guardamos las sesiones que los usuarios inician en la memoria del servidor dónde la aplicación se está ejecutando.
- Session.cookie_expires: 300 → expiración de la sesión. Medida en segundos.
- session.auto: true → la sesión iniciada por el usuario se guardará cada vez que se acceda por peticiones a la aplicación.

Por último, decir de las sesiones de Beaker guardadas en memoria que estas se guardan en diccionarios, así que su manejo nos resultará muy cómodo.

### ¿Qué es PyGithub?

PyGithub es una librería (de otras muchas) de python. Gracías a esta librería podemos administrar los recursos, que Github nos ofrece, a través de scripts de Python.

Desafortunadamente, PyGithub no dispone de mucha [documentación](http://pygithub.readthedocs.io/en/latest/introduction.html#very-short-tutorial) en su web, tan sólo una pequeña introducción que nos permite listar los repositorios que tenemos creados en nuestro perfil de Github.

De todas formas, su uso es intuitivo y fácil para aquel que haya trabajado minimamente con alguna librería anteriormente. Si tenemos el paquete Ipython instalado en nuestro sistema, podremos acceder a todos los métodos que nos ofrece PyGithub una vez nos hemos “logueado” con dicha librería.

Un ejemplo sencillo de uso sería el siguiente. Primero nos metemos a ipython (si no lo tenemos instalado, lo instalamos con apt install ipython):

	ipython

Cargamos la librería de PyGithub:

	from github import Github 

A continuación, nos logueamos (está en claro, por seguridad no pondré mis datos):

	g = Github("<usuario>","<contraseña>")

La mayoría de métodos interesantes a utilizar están dentro de g.get_user(), podemos mostrarlos metiendo dicho método en una variable:

	l = g.get_user()

De este modo, al escribir l. y pulsar TAB, nos mostrará todos los métodos que podemos utilizar. 
Si queremos sacar nuestros seguidores, con la variable anteriormente definida, escribimos:

	for x in l.get_followers():
   	  ...:     print x.name
   	  ...:     
	Álvaro Rodríguez Márquez
	Carlos Gómez Díaz
	Carlos Jesús Sánchez Ortega
	Juan Manuel Díaz Galán
	Alejandro Palomino García
	Alvaro Sola Olivero
	Manuel Alcocer Jiménez
	Alberto Andrades

En la aplicación utilizaré el método para saber si hay un repositorio que ya existe (get_repo()), crear un repositorio (create_repo(‘<nombre>’)) y borrarlo (get_repo(‘<nombre’).delete())

## Creación de la aplicación de Bottle paso a paso

Una vez tenemos instalado el software requerido y tenemos un mínimo conocimiento sobre ellos, comenzamos a crear nuestra aplicación. 

El fichero dónde la aplicación será ejecutada deberá tener las librerías que importaremos y éstas son:

	from bottle import Bottle, app, route, run, request, template, default_app, static_file, get, post, response, redirect
	import commands
	import json
	import getpass
	from ldap3 import Server, Connection, ALL
	from beaker.middleware import SessionMiddleware
	from github import Github

Ahora procedemos a añadirle las sesiones que los usuarios usarán para poder mantenerse conectados (opciones usadas anteriormente explicadas en el apartado [¿Qué es Beaker?]()):

	# Sesiones de usuarios con tiempo de 5 min guardados en memoria
	session_opts = {
	    'session.type': 'memory',
	    'session.cookie_expires': 300,
	    'session.auto': True
	}
	app = SessionMiddleware(app(), session_opts)

La aplicación también deberá poder conectarse con nuestro servicio de LDAP, así que establecemos la conexión con:

	# Definimos el usuario y su contraseña para iniciar una conexión con el servicio LDAP
	usuario = "cn=admin,dc=spotype,dc=com"
	# Cambiar contraseña para no tener que ponerla transparente
	password = 'root'

	server = Server("{{ ansible_eth0.ipv4.address}}", get_info=ALL)
	conn = Connection(server, usuario, password, auto_bind=True)

Y al final del fichero, añadimos la ruta de los ficheros estáticos así cómo la ejecución de la aplicación:

	# Ficheros estáticos
	@route('/static/<filepath:path>')
	def server_static(filepath):
	    return static_file(filepath, root='static')

	run(app=app,host="{{ ansible_eth0.ipv4.address }}", port=8080)

Para añadir la página de inicio deberemos de segmentar el index de una plantilla cualquiera. En mi caso elegí la plantilla [Read Only](https://html5up.net/read-only), para así dejar fijo el header y footer e ir jugando con el body.

Quedaría así:

__Header.tpl__

    <!DOCTYPE HTML>
    …
    (Hasta la parte en la que el contenido empieza)
    
Templates de contenido variante (ejemplo):

    % include('header.tpl')  <!-- Aquí se incluye el fichero con el header de nuestro index -->
    					<!-- One -->
    							<section id="one">
    								<div class="container">
    									<header class="major">
    										<h2>Bienvenido</h2>
    										
    									</header>
    									<p>Bienvenido a Spotype.</p>
    								</div>
    							</section>
    					</div>
    
    % include('footer.tpl')	  <!-- Aquí se incluye el fichero con el footer de nuestro index -- >

__Footer.tpl__

    <!-- Footer -->
    …
    </body>
    </html>

Bien, ya “construida” nuestra web, vamos con la aplicación que interactuará con dichas plantillas.

**Repositorio de Github**

A partir de ahora se procederá a explicar las secciones de la aplicación con enlaces a las lineas del fichero alojado en el repositorio de [Github](https://github.com/aitor28ld/Proyecto).

### Creación de usuarios en LDAP y verificación de dichos usuarios

Para aquellos nuevos usuarios que quieran usar nuestro hosting, deberemos de crearles su usuario para que así pueda disponer de todas las funciones que ofrecemos a través de la aplicación. 
Desde la [linea 27](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L27) hasta la linea [linea 117](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L117) podemos ver lo siguiente:

-En [este route](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L28) podemos ver la página principal de la aplicación, el cual, si el usuario es nuevo se le devuelve una página y si ya es un usuario registrado, se le devuelve otra. Todo gracias a las sesiones de usuarios. El contenido de [index-sesion.tpl](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/index-sesion.tpl) y de [index.tpl](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/index.tpl) es prácticamente casí el mismo, a diferencia del botón para dirigirse al perfil del usuario.

-En el [route de la linea 39](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L39) se define la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/registro.tpl) que contiene los datos para que el usuario se registre en el hosting.

-Posteriormente, los datos introducidos por el usuario se reciben en [este post](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L45). Dichos datos se almacenan en variables y en la sesión propia del usuario, para luego ser enviados a [este route](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L67) y proceda a [crearle el perfil en el servicio LDAP](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L79), su [directorio personal](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L84) y se le asignen sus [permisos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L90) correspondientes. Si todo fue bien, se le devuelve la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/sesion-valida.tpl) con el mensaje de que se ha registrado con éxito, sino, se le devuelve otra [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/sesion-error.tpl) con el mensaje de error

### Inicio de sesión de usuarios ya registrados

A aquellos usuarios que ya estén registrados, deberemos de crearles un inicio de sesión. 

Desde la [linea 123](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L123) hasta la [linea 144](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L144) podemos ver:

-Vemos el primer [route](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#119) de la sección, el cual lleva a la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/inicio.tpl) con los datos que el usuario deberá introducir para poder iniciar sesión correctamente en el hosting.

-[Recibimos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L123) los datos introducidos por el usuario y [abrimos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L126) la sesión. Si la contraseña [no](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L132) está vacía y el usuario es [correcto](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L135), añadimos la [sesión](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L1137) y devolvemos la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/login-ok.tpl) de inicio de sesión correcto, sino devolvemos la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/login-error.tpl) con el error.

### Perfiles de usuarios

Cada usuario registrado tendrá su perfil. Este perfil es general, es decir, no tendrá botones o acciones especiales para cada usuario.

Desde la [linea 145](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L145) hasta la [linea 149](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L149) podemos ver un método GET para devolver una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/perfil.tpl) con las acciones que el usuario podrá realizar.

### Creación de repositorios con subida de ficheros iniciales

Cada usuario deberá subir sus ficheros a través de repositorios de Github.

Desde la [linea 151](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L151) hasta la [linea 233](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L233) podemos ver, en orden:

-En este [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L152), [si existe una sesión](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L155) con los datos de Github (usuario y contraseña), devolvemos una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/web-git.tpl), sino devolvemos [otra](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/web.tpl). Esto es necesario ya que debemos guardar dicha información para poder conectarnos a nuestro perfil de Github.

-Este [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L160) es el correspondiente a si existe una sesión de Github. Recibimos el nombre del repositorio a crear, lo [metemos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L164) en la sesión de github ya existente y, si ese [repositorio existe](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L172) no se crea y [devolvemos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/error-git.tpl) el error, en [caso contrario](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L174) se creará con el nombre dado por el usuario.

-En [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L179) corresponde a si no existe una sesión de Github anteriormente. Recibimos los datos de conexión así cómo el nombre del repositorio, los [guardamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L186) en la sesión y realizamos la misma acción que en el anterior POST.

-Los dos métodos POST anteriores nos redirigen a este [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L198). Aquí comenzamos a [crear el repositorio](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L202) en local con un fichero README.md, lo [inicializamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L206) y hacemos un [push](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L208) al repositorio. También le [creamos el virtualhost](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L210) al usuario, [buscamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L225) si existe en el registro DNS, si [no existe](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L226), lo [añadimos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L227) y reiniciamos el servicio así cómo limpiamos su caché, [sino](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L230) sólo limpiamos caché y reiniciamos el servicio.

### Actualización de repositorios o directos a la web del usuario
Necesitaremos hacer un pull, con git, para que cuando el usuario acceda a su página web por medio de la aplicación le aparezca actualizada, o si lo prefiere, acceder directamente a su web:

__Actualizar repositorio__

Desde la [linea 235](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L235) hasta la [linea 273](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L273) vemos en orden:

-En este [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L235), [si existe](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L238) la sesión de github se le devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/webs-git.tpl), [sino](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L240) se le devuelve [otra](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/webs.tpl).

-En este [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L243), si el repositorio introducido para actualizar es [igual](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L247) que al de la sesión, se redirecciona, sino se le devuelve el error en la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/err-repo.tpl).

-En este [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L252), [recibimos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L255) los datos introducidos y [redireccionamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L261) otro método.

-En este [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L263), si la sesión se llama [github](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L266) se [actualiza](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L267) en local con sus datos y se [redirecciona](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L268) a su web, si es [repos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L269), se actualiza con los suyos y se redirecciona a su web, sino se devuelve un error especifico a la [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/err-key.tpl).

__Ir a la web directamente__

Desde la [linea 276](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L276) hasta la [linea 279](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L279) vemos la [redirección](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L279) a la web del usuario.

### Creación de bases de datos en mysql

Los usuarios que suban CMS, tales cómo wordpress, joomla, magento, etc. necesitarán de base de datos para alojar sus datos en ellas. Por ello, deberemos hacer que dichos usuarios puedan crearlas a partir de la aplicación (Y para los usuarios más expertos, a partir de Phpmyadmin)

Desde la [linea 282](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L282) hasta la [linea 297](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L297) vemos, en orden:

-Un [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L282) que devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/crear-mysql.tpl) dónde el usuario introducirá los datos para crear su base de datos.

-Un [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L287), [recibe](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L288) los datos introducidos por el usuario guardándolos en variables, [introduciendo](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L292) datos (usuario, contraseña y nombre de la BD) en un fichero e [inyectando](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L296) ese fichero en mysql con credenciales de root. Devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/mysql.tpl) notificando de la creación exitosa de la base de datos.

### Administración por phpmyadmin de las bases de datos

Los usuarios con un mejor conocimiento en administración de base de datos podrán administrar las suyas mediante phpmyadmin, el cual deberemos instalarlo mediante la importación de Ansible y definir una ruta en la aplicación.

__Sección en la aplicación__

En la aplicación deberemos definir un [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L300) para que los usuarios que pulsen en el botón sean [redirigidos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L302) a la web de phpmyadmin del hosting.

__Instalación de phpmyadmin con ansible__

Necesitaremos instalar phpmyadmin mediante playbooks de Ansible para que la automatización del hosting sea completa.

Editamos el fichero correspondiente a db.spotype (en el rol dns/templates/), añadiendo la siguiente linea al final del fichero:

	phpmyadmin      IN      CNAME   {{ ansible_hostname }}

Guardamos y procedemos a crear un fichero en el rol serweb/files, dicho fichero lo llamaré phpmyadmin.conf con el siguiente contenido:

    <VirtualHost *:80>
    ServerName phpmyadmin.spotype.com
    
    ServerAdmin webmaster@localhost
    DocumentRoot /usr/share/phpmyadmin #Apuntando al directorio principal de phpmyadmin
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    </VirtualHost>

Ahora editaremos las tareas del mismo rol (tasks/main.yml) añadiendo lo siguiente:

    - name: instalación de apache, php5 y curl
      apt: name={{item}} state=installed
      with_items:
       - apache2
       - php5
       - php5-curl
    
    - copy:
      src: spotype.conf
      dest: /etc/apache2/sites-available/spotype.conf
	  owner: root
      group: root
      mode: 644*
    
    - copy:  #Este copy entero
      src: phpmyadmin.conf
      dest: /etc/apache2/sites-available/phpmyadmin.conf
      owner: root
      group: root
      mode: 644
    
    - name: Habilitando el sitio de Spotype.com y phpmyadmin
      shell: sudo a2ensite spotype.conf
      shell: sudo a2ensite phpmyadmin.conf #Esta
    
    - name: Haibilitando modulos de apache2
      action: command a2enmod rewrite
      notify: reinicio del servicio de Apache

Ahora creamos el rol de phpmyadmin con la siguiente estructura de directorio:

	Phpmyadmin/
	├── defaults
	│ └── main.yml
	├── tasks
	│ ├── main.yml
	│ └── setup-Debian.yml
	└── vars
	    └── main.yml

Dónde:

- Defaults: contiene la configuración de la instalación necesaria para phpmyadmin
- tasks: contiene las tareas principales de instalación y configuración de phpmyadmin para Debian
- vars: contiene las variables necesarias para la instalación y configuración de phpmyadmin.

Contenido de __defaults/main.yml:__

	phpmyadmin_mysql_host: localhost
	phpmyadmin_mysql_port: ""
	phpmyadmin_mysql_socket: ""
	phpmyadmin_mysql_connect_type: tcp
	phpmyadmin_mysql_user: root
	phpmyadmin_mysql_password: "{{ mysql_root_password }}"

Contenido de __tasks/main.yml:__

    - name: Variables de phpmyadmin
      include_vars: "main.yml"
     
    - name: Fichero de configuración de phpmyadmin 
      set_fact:
        phpmyadmin_config_file: "{{ __phpmyadmin_config_file }}"
      when: phpmyadmin_config_file is not defined
    
    - include: setup-Debian.yml
      when: ansible_os_family == 'Debian'
    
    - name: Añadimos usuario y contraseñas root para la conexión con mysql
      lineinfile: >
        dest={{ phpmyadmin_config_file }}
        state=present
    	regexp="^.+\['{{ item.key }}'\].+$"
    	line="$cfg['Servers'][$i]['{{ item.key }}'] = '{{ item.value }}';"
    	insertbefore="^\?>"
      with_items:
      - { key: host, value: "{{ phpmyadmin_mysql_host }}" }
      - { key: port, value: "{{ phpmyadmin_mysql_port }}" }
      - { key: socket, value: "{{ phpmyadmin_mysql_socket }}" }
      - { key: connect_type, value: "{{ phpmyadmin_mysql_connect_type }}" }
      - { key: user, value: "{{ phpmyadmin_mysql_user }}" }
      - { key: password, value: "{{ phpmyadmin_mysql_password }}"}
    
Contenido de __tasks/setup-Debian.yml:__

    - name: Asegurarse de que phpmyadmin está instalado
      apt: name=phpmyadmin state=installed
      notify: restart apache
    
    - name: Asegurarse de la configuración de phpmyadmin en apache2
      lineinfile:
    	dest: /etc/apache2/apache2.conf
    	state: present
    	regexp: "^Include.+phpmyadmin.+$"
    	line: "Include /etc/phpmyadmin/apache.conf"
    	insertafter: "EOF"
      notify: reinicio del servicio de Apache

Contenido de __vars/main.yml:__

	__phpmyadmin_config_file: /etc/phpmyadmin/config.inc.php

Por último, agregamos el rol al playbook de Ansible que utilizamos cómo principal:

    —
    - hosts: proyecto
      user: usuario
      sudo: True
      roles:
    	- actualizaciones
    	- dns
    	- serweb
    	- bd
    	- phpmyadmin
    	- { role: ldap }

### Eliminación de repositorios creados

Todo usuario debería poder eliminar sus repositorios cuando ellos lo vean necesario.

Desde la [linea 305](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L305) hasta la [linea 324](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L324) vemos, en orden:

- Un [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L305) el cual devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/delweb.tpl) con los datos que deberá introducir el usuario para, después, proceder a la eliminación del repositorio definido.

- Un [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L309) que recibe los datos introducidos por el usuario y, si el usuario tiene una sesión llamada [github](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L315), se obtienen sus [datos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L316) y se [elimina](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L317) el repositorio devolviendo una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/delgit.tpl), al igual que si la tiene con [repos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L319), sino se devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/no-sesion.tpl) notificando el error.

## Eliminación de base de datos

Al igual que con la creación de base de datos, el usuario podrá eliminar las bases de datos que él quiera mediante la aplicación (para principiantes) o mediante la administración por phpmyadmin (para usuarios con algo de conocimientos).

Si la hacemos mediante la aplicación, podemos ver desde la [linea 327](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L327) hasta la [linea 342](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L342):

- Un [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L327), el cual devuelve una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/delbd.tpl) con los datos que deberá introducir el usuario sobre la base de datos a eliminar.

- Un [método POST](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L331), dónde recibimos los datos y los [guardamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L335) en variables, creando un [fichero](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L337) con  dichos datos e [inyectandolo](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L340) a mysql para el borrado de la base de datos y devolviendo una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/deletebd.tpl) con la notificación de que se eliminó.

## Eliminación de usuarios

Por último, y no menos importante, el usuario podrá “darse de baja” en nuestro hosting si él lo quiere así.

Desde la [linea 344](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L344) hasta la [linea 355](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L355) podemos ver, en orden:

- Un [método GET](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L345), dónde [guardamos el usuario](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L348) de la sesión en una variable, lo [borramos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L349) del servicio LDAP, del [registro](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L350) del servicio DNS y [deshabilitamos](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/templates/aplicacion.py#L351) su web, devolviendo una [plantilla](https://github.com/aitor28ld/Proyecto/blob/master/ansible/roles/aplicacion/files/aplicacion/views/delacc.tpl) con la notificación de eliminación exitosa.

# Despliegue de la aplicación de Bottle con Ansible
Para que la aplicación y el automatizado del hosting sea completo, deberemos de crear las tareas perteneciente a ello.

Creamos una nueva tarea llamada aplicación cuyas subdirectorios serán files, templates y tasks .
El subdirectorio files contendrá:

	Files/
	├── aplicación
	├── ldap3-master.zip
	└── PyGithub-master.zip

Dónde:

- aplicación: contendrá todos los ficheros necesarios para la ejecución optima de la aplicación exceptuando el fichero de ejecución del servidor, el cual estará alojado en Templates ya que necesita variables.
- ldap3-master.zip y PyGithub-master.zip: paquetes necesarios para la ejecución optima de la aplicación.
    
    	Templates
    	└── aplicacion.py


Dónde:

- aplicación.py: el fichero que ejecuta la aplicación. Contiene variables de ansible cómo por ejemplo:

<pre>
run(app=app,host="{{ ansible_eth0.ipv4.address }}", port=8080)
</pre>

Estructura de __tasks__

    Tasks/
    └── main.yml


Contenido de __main.yml__:

    - name: Instalación de los paquetes necesarios de la aplicación de Hosting
      shell: apt install geany python-bottle python-setuptools git python-beaker -y
    
    - copy:
        src: ldap3-master.zip
        dest: /home/usuario/Plantillas/ldap3-master.zip
    
    - copy:
    	src: PyGithub-master.zip 
    	dest: /home/usuario/Plantillas/PyGithub-master.zip
    
    - name: Descomprimiendo LDAP3
      shell: cd /home/usuario/Plantillas/ && sudo unzip ldap3-master.zip
    
    - name: Descomprimiendo PyGithub
      shell: cd /home/usuario/Plantillas/ && sudo unzip PyGithub-master.zip
     
    - name: Instalación de LDAP3
      shell: cd /home/usuario/Plantillas/ldap3-master && sudo python setup.py install
    
    - name: Instalando PyGithub
      shell: cd /home/usuario/Plantillas/PyGithub-master && sudo python setup.py install
    
    - copy:
    	src: aplicacion
    	dest: /home/usuario/
    	directory_mode: yes
    
    - name: Copiando fichero aplicacion.py
      template: >
    	src=aplicacion.py
    	dest=/home/usuario/aplicacion/aplicacion.py
    
    - name: Cambiando permisos a static
      shell: sudo chgrp -R www-data /home/usuario/aplicacion/static
    
    - name: Cambiando permisos a views
      shell: sudo chgrp -R www-data /home/usuario/aplicacion/views
      shell: sudo chmod -R 755 /home/usuario/aplicacion
    
    - name: Haciendo la aplicación ejecutable por el usuario
      shell: sudo chown -R usuario:usuario /home/usuario/aplicacion
    
    - name: Tareas de mantenimiento
      shell: sudo mkdir /home/users

El fichero principal.yml quedaría de la siguiente forma, siendo esto su contenido final:

<pre>
—
- hosts: proyecto
  user: usuario
  sudo: True
  roles:
    - actualizaciones
    - serweb
    - aplicacion
    - bd
    - phpmyadmin
    - ldap
    - dns
</pre>

Una vez la aplicación haya sido desplegada con Ansible, la ejecutaremos con:

	python aplicación.py

	usuario@debian:~/aplicacion$ python aplicacion.py 
	Bottle v0.12.7 server starting up (using WSGIRefServer())...
	Listening on http://192.168.1.129:8080/
	Hit Ctrl-C to quit.

Los clientes que vayan a acceder y estén en el rango local o el servidor esté accesible desde internet, deberán introducir en la URL de su navegador:
	www.spotype.com:8080

El hosting **no** dispone de redirección de puertos.

# Referencias
[Página oficial de ansible](https://www.ansible.com/it-automation)

[Tutorial de Ansible - Playbooks](http://docs.ansible.com/ansible/playbooks_intro.html)

[Tutorial de Ansible – Roles](http://docs.ansible.com/ansible/playbooks_roles.html)

[Tutorial de Ansible – Copias](http://docs.ansible.com/ansible/copy_module.html)

[Tutorial de Ansible – Variables](http://docs.ansible.com/ansible/playbooks_variables.html#variables-defined-in-inventory)

[Tutorial de Ansible - Módulo apt](http://docs.ansible.com/ansible/apt_module.html)

[Tutorial de Ansible – Templates](http://docs.ansible.com/ansible/template_module.html#status)

[Tutorial de Ansible - File](http://docs.ansible.com/ansible/file_module.html)

[Repositorio de OpenLDAP automatizado con Ansible](https://github.com/kbrebanov/ansible-openldap)

[Error de mal configuración de OpenLDAP con Ansible](https://serverfault.com/questions/540721/when-tried-to-do-ldapadd-got-this-error-ldap-add-no-such-object-32)

[Instalación de MySQL con Ansible](http://techwatch.keeward.com/geeks-and-nerds/properly-install-mysql-on-production-server-using-ansible/)

[Página oficial de Bottle](https://bottlepy.org/docs/dev/)

[Ejemplo de Sesiones con Beaker](https://gist.github.com/alexcabrera/4662006)

[Tutorial de Beaker](http://beaker.readthedocs.io/en/latest/configuration.html)

[Tutorial de PyGithub](http://pygithub.github.io/PyGithub/v2/user_guide.html)
