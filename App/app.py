from flask import Flask, render_template, url_for

app = Flask(__name__)

menu_items = [
    {"name": "Elegir Método de Pago", "url": "#", "disabled": False},
    {"name": "Revisar Información Empleado", "url": "#", "disabled": False},
    {"name": "Revisar Días Trabajador", "url": "#", "disabled": False},
    {"name": "Revisar Cotizaciones", "url": "#", "disabled": False},
    {"name": "Imprimir Liquidación", "url": "#", "disabled": False},
]

# Ruta principal
@app.route('/')
def layout():
    return render_template('index.html', menu_items=menu_items)

# Ruta de login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta de registro
@app.route('/register')
def register():
    return render_template('registrar.html', menu_items=menu_items)

if __name__ == '__main__':
    app.run(debug=True)
