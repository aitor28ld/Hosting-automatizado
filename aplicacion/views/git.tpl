% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Correcto!</h2>
				</header>
				<p>Repositorio {{repo}} creado con exito! <br>
				Ya puedes subir tus archivos a tu repositorio en <a href="https://github.com/{{usuario}}">Github</a></p>
				<form action="/perfil">
					<input type="submit" value="Ir a tu perfil" />
				</form>
			</div>
		</section>
	</div>

% include('footer.tpl')
