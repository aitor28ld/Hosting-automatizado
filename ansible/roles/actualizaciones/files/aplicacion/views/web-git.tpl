% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Logueate en Github</h2><br>
				</header>
				<h4>Inicio de sesión y nuevo repositorio</h4>
				<form action="/githubok" method='POST'>
					Nombre del repositorio a crear: <input name="repo" type="text" /><br>
					
					<input type="submit" value="Loguearse y crear" />
				</form>
			</div>
		</section>
	</div>

% include('footer.tpl')
