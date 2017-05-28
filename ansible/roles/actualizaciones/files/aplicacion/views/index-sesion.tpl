% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Bienvenido {{usuario}}</h2>
				</header>
				<p>Bienvenido a Spotype.</p>
				<form action="/perfil">
					<input type="submit" value="Ir a tu perfil" />
				</form>
			</div>
		</section>
	</div>

% include('footer.tpl')
