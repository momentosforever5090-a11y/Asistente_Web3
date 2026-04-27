Mira esto: # auth.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-muy-segura-cambiar-en-produccion'

# Configurar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# Modelo de usuario simple
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Base de datos de usuarios (solo para pruebas)
# En producción usar una base de datos real
users_db = {
    'admin': {'password': 'admin123'},
    'user': {'password': 'pass'}
}

@login_manager.user_loader
def load_user(user_id):
    # El user_id guardado en sesión es el nombre de usuario en este ejemplo
    if user_id in users_db:
        return User(user_id, user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if username in users_db and users_db[username]['password'] == password:
            user = User(username, username)
            login_user(user, remember=form.remember.data)
            flash('¡Sesión iniciada correctamente!', 'success')
            
            # Redirigir a la página que el usuario intentaba ver (next parameter)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
