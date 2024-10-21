from flask import Flask, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from config import config
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models.ModelUser import ModelUser
from models.ModelCotizaciones import ModelCotizaciones
from models.entities.User import User


app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


menu_items = [
    {"name": "Elegir Método de Pago", "url": "metodoPago", "disabled": False},
    {"name": "Revisar Información Empleado", "url": "#", "disabled": False},
    {"name": "Revisar Días Trabajador", "url": "dias", "disabled": False},
    {"name": "Revisar Cotizaciones", "url": "cotizacion", "disabled": False},
    {"name": "Imprimir Liquidación", "url": "#", "disabled": False},
]

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Ruta principal
@app.route('/')
def layout():
    return render_template('index.html', menu_items=menu_items)

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = []
    if request.method == 'POST':
        user = User(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('layout'))
            else:
                messages.append("Invalid password...")
                return render_template('login.html', messages=messages)
        else:
            messages.append("User not found...")
            return render_template('login.html', messages=messages)
    else:
        return render_template('login.html')

@app.route('/dias')
@login_required
def dias():
    return render_template('dias.html', menu_items=menu_items)

@app.route('/cotizacion')
@login_required
def cotizacion():
    cotizaciones = ModelCotizaciones.traerCotizacion(db, current_user.id)
    return render_template('cotizacion.html', menu_items=menu_items, cotizaciones=cotizaciones)

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('name')
        rut = request.form.get('rut')
        profesion = request.form.get('profesion')
        cargo = request.form.get('cargo')
        jornada = request.form.get('jornada')
        sueldo = float(request.form.get('sueldo'))
        fecha_nacimiento = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        email = request.form.get('email')
        descuentos = request.form.get('descuentos')

        # Validaciones aquí
        if not nombre or not rut or not profesion or not cargo or not jornada or not sueldo or not fecha_nacimiento or not email or not descuentos:
            flash('Por favor complete todos los campos.', 'danger')
            return redirect(url_for('register'))

        try:
            # Conexión a la base de datos y cursor
            cursor = db.connection.cursor()

            # SQL para insertar el nuevo registro
            sql = """
            INSERT INTO user (fullname, rut, profesion, cargo, jornada, sueldo, fechaNacimiento, username, descuentos, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'admin')
            """
            values = (nombre, rut, profesion, cargo, jornada, sueldo, fecha_nacimiento, email, descuentos)

            # Ejecutar la consulta
            cursor.execute(sql, values)
            db.connection.commit()  # Guardar los cambios en la base de datos

            flash('Cuenta creada exitosamente!', 'success')

            user = User(0, email, 'admin')
            logged_user = ModelUser.login(db, user)
            login_user(logged_user)
            return redirect(url_for('layout'))

        except Exception as e:
            db.connection.rollback()  # Revertir cambios en caso de error
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
            print(f"No se puede crear por: {e}")
            return redirect(url_for('register'))

        finally:
            cursor.close() 

    # Si es un GET, simplemente muestra el formulario
    return render_template('registrar.html', menu_items=menu_items)

@app.route('/metodoPago')
@login_required
def metodoPago():
    return render_template('metodoPago.html', menu_items=menu_items)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    # Consulta SQL para traer el perfil del usuario logueado
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE id = %s", (current_user.id,))
    user_data = cursor.fetchone()
    cursor.close()

    print(user_data)
    if user_data:
        # Crear el objeto `User` con los datos traídos desde la base de datos
        user = User(
            user_data[0],               # id
            user_data[1],               # fullname
            user_data[2],               # username (email)
            user_data[3],              # password
            user_data[4],               # rut
            user_data[5],               # profesion
            user_data[6],               # cargo
            user_data[7],               # jornada
            float(user_data[8]),               # sueldo
            user_data[9],               # fechaNacimiento
            user_data[10]                # descuentos
        )

        # Renderiza la plantilla `profile.html` con la información del usuario
        return render_template('profile.html', menu_items=menu_items, user=user)
    else:
        flash("No se pudo cargar el perfil", "danger")
        return redirect(url_for('layout'))
    
def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)
