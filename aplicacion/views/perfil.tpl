% include('header.tpl')
	<!-- One -->
		<section id="one">
			<div class="container">
				<header class="major">
					<h2>Perfil de {{usuario}}</h2><br>
				</header>
				<h4>Acciones para hacer</h4>
				<ul>
					<li><form action="/web">
							<input type="submit" value="Crear repositorio" />
						</form>
					</li>
					<li><form action="/webs">
							<input type="submit" value="Actualizar repositorio" />
						</form>
					</li>
					<li><form action="/page">
							<input type="submit" value="Ir a tu página web" />
						</form>
					</li>
					<li><form action="/phpmyadmin">
							<input type="submit" value="Administrar Base de Datos" />
						</form>
					</li>
					<li><form action="/delweb">
							<input type="submit" value="Eliminar web/CMS" />
						</form>
					</li>
					<li><form action="/delaccount">
							<input type="submit" value="Eliminar cuenta" />
						</form>
					</li>
				<ul>
			</div>
		</section>
	</div>

% include('footer.tpl')
