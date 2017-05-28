% include('header.tpl')
<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Eliminar Base de datos</h2>
				</header>
				<form action="/deletebd" method="post">
					Usuario : <input name="user" type="text" /><br>
					Nombre de la base de datos : <input name="bd" type="text" /><br>
					<input value="Borrar Base de Datos" type="submit" />
				</form>
			</div>
		</section>
	</div>

% include('header.tpl')
