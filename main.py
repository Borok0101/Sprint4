from flask import Flask, request, redirect, url_for, session
from formulario import formularioRegistro
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash

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
        contrasena = generate_password_hash(form.contrasena.data)
        
        #Conexion DataBase

        with sqlite3.connect("dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute("insert into usuario(idUsu,tipoDocUsu,passwordUsu,nombreUsu,apellidoUsu,celularUsu,fechaNacUsu,sexoUsu,correoUsu,paisUsu) values(?,?,?,?,?,?,?,?,?,?)",
                        (nro_documento,tipo_documento,contrasena,nombre,apellido,telefono,fecha_nacimiento,genero,email,pais))
            conn.commit()
            return "Se ha registrado satisfactoriamente"
            
    return "Error al guardar los datos"


    

## Hecho por Jorge

app.secret_key = "sdkajsgf4b45"

@app.route('/login', methods =["GET","POST"])
def home():
    return render_template('Login.html')


@app.route('/logueo', methods =["GET","POST"])
def login():

    #clave = "Hola" #Base de datos
    #rol = 1 #"traer rol de base de datos"
    #correo = "hola@ashdka" #base de datos
    if request.method == "POST":

        email = request.form['email']
        
        #Conexion DataBase

        with sqlite3.connect("dataBase.db") as conn:

            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * from usuario where correoUsu = ?", (email,))
            row = cur.fetchone()
            correo = row["correoUsu"]
            clave = row["passwordUsu"]
            rol = row["rolUsu"]

            print(row,clave,rol)
            
        password = check_password_hash(clave,request.form['password'])

        if password and email == correo  :
            
            session['user']=email
            session['rol']=rol
            return redirect(url_for('control'))
        else: return "errorrr"
    else:
        return "bad request"  


@app.route('/control')
def control():
    if 'user' in session and session['rol'] == 3:
        return redirect(url_for('panel'))
    elif  'user' in session and session['rol'] == 2:
        return redirect(url_for('vistaPiloto'))
    elif  'user' in session and session['rol'] == 1:
        return redirect(url_for('vistaClient'))
    else: return "Error"

@app.route('/panel')
def panel():
    if 'user' in session and session['rol'] == 3:
        return render_template('Panel.html')
    else:
        return render_template('login.html')

@app.route('/vistaClient')
def vistaClient():
    if 'user' in session and session['rol'] == 1:
         return "vistaClient"
    else:
        return render_template('login.html')

@app.route('/vistaPiloto')
def vistaPiloto():
    if 'user' in session and session['rol'] == 2:
        return  "vistaPiloto"
    else:
        return render_template('login.html')

@app.route('/Infor')
def infor():
    if 'user' in session and session['rol'] == 3:
        return render_template('Infor.html')
    else:
        return render_template('login.html')
    

@app.route('/logout') #Metodo para salir
def logout():
    return redirect(url_for('login'))


if (__name__ == 'main'):
    app.run(debug=True)