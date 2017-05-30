% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Actualización de repositorios</h2><br>
				</header>
				<h4>Repositorio a actualizar en el servidor</h4>
				<form action="/reposok" method='POST'>
					Repositorio: <input name="repositorio" type="text" /><br>
					
					<input type="submit" value="Actualizar repositorio" />
				</form>
			</div>
		</section>
	</div>

% include('footer.tpl')
