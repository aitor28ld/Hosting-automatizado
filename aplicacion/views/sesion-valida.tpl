% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Completado!</h2>
				</header>
				<p>Usuario <b>{{usuario}}</b> registrado con exito!</p>
				<form action="/inicio">
					<input type="submit" value="Iniciar sesión" />
				</form>
			</div>
		</section>
	</div>

% include('footer.tpl')			
