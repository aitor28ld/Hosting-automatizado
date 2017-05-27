% include('header.tpl')
<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Crear Base de datos</h2>
				</header>
				<form action="crearmysql" method="post">
					Usuario : <input name="user" type="text" /><br>
					Contraseña : <input name="contras" type="password" /><br>
					Nombre de la base de datos : <input name="bd" type="text" /><br>
					<input value="Crear Base de Datos" type="submit" />
				</form>
			</div>
		</section>
	</div>

% include('header.tpl')
