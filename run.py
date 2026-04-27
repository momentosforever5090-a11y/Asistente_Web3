# run.py
from auth import app, login_required
from dashboard import dash_app

# Proteger la ruta del dashboard a nivel de Flask
@app.route('/dashboard/')
@login_required
def dashboard():
    # Dash manejará el contenido, pero Flask exige autenticación
    return dash_app.index()

if __name__ == '__main__':
    app.run(debug=True)
