from flask import Flask, request, redirect, url_for, session
from formulario import formularioRegistro
from flask.templating import render_template
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route("/registrarse", methods=["GET","POST"])
def registro():
    form = formularioRegistro()
    return render_template('registro.html', form=form)


@app.route("/guardar_registro", methods=["GET","POST"])
def guardar_registro():
    form = formularioRegistro()
    if request.method == "POST":
        pais = form.pais.data
        tipo_documento = form.tipo_documento.data
        nro_documento = form.nro_documento.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        fecha_nacimiento = form.fecha_nacimiento.data
        genero = form.genero.data
        telefono = form.telefono.data
        email = form.email.data
        contrasena = form.contrasena.data
        with sqlite3.connect("dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute("insert into usuario(idUsu,passwordUsu,nombreUsu,apellidoUsu,celularUsu,fechaNacUsu,sexoUsu,correoUsu) values(?,?,?,?,?,?,?,?)",
                        (nro_documento,contrasena,nombre,apellido,telefono,fecha_nacimiento,genero,email))
            conn.commit()
            return "Se ha registrado satisfactoriamente"
            
    return "Error al guardar los datos"


    

## Hecho por Jorge

app.secret_key = "sdkajsgf4b45"

@app.route('/login', methods =["GET","POST"])
def home():
    return render_template('login.html')

@app.route('/logueo', methods =["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        session['user']=email
        return redirect(url_for('panel'))
        
    else:
        return "bad request"     

    

@app.route('/panel')
def panel():
    if 'user' in session:
        return render_template('Panel.html')
    else:
        return render_template('login.html')

@app.route('/Infor')
def infor():
    if 'user' in session:
        return render_template('Infor.html')
    else:
        return render_template('login.html')
    

@app.route('/logout') #Metodo para salir
def logout():
    return redirect(url_for('login'))




if (__name__ == 'main'):
    app.run(debug=True)