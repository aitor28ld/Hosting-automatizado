% include('header.tpl')
<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Registro</h2>
					<p>Introduce los siguientes datos</p>
				</header>
				<form action="sesion" method="post">
					Nombre: <input name="nombre" type="text" /><br>
					Primer apellido: <input name="apeuno" type="text" /><br>
					Segundo apellido: <input name="apedos" type="text" /><br>
					Usuario: <input name="usuario" type="text" /><br>
					Contraseña : <input name="password" type="password" /><br>
					Email : <input name="email" type="text" /><br>
				<input value="Registrarse" type="submit" />
			</form>
			</div>
		</section>
	</div>

% include('header.tpl')
