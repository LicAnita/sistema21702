from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app = Flask(__name__)
app.secret_key='sistema21702'

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema21702'

mysql.init_app(app)
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route("/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


@app.route("/")
def index():

    #guardar usuario en la base de datos
    sql = "SELECT * FROM `empleados`;";
    
    #llamo a la conection
    conn = mysql.connect()
    #llamo al cursor que es el que viaja a la base de datos
    cursor = conn.cursor()
    #que lleve el pedido sql de arriba
    cursor.execute(sql)

    #para comprobar que se vea bien
    empleados=cursor.fetchall()
    print(empleados)


    conn.commit()
    #además que me devuelva a la página de origen, que me devuelva los empleados de la lista
    return render_template("empleados/index.html", empleados=empleados)

@app.route("/destroy/<int:id>")
def destroy(id):
    #borrar usuario de la base de datos, podría crear el sql 
    # sql = "DELETE FROM `empleados` WHERE `id` = %s;"
    # pero es más piola así:
    conn = mysql.connect()
    cursor = conn.cursor()

    #para que me elimine también la foto del repositorio local
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    #que me traiga todo lo que devuelve la consulta.
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM empleados WHERE id=%s ", (id))
    conn.commit()
    return redirect('/')    

@app.route("/edit/<int:id>")
def edit(id):
    #editar usuario de la base de datos
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s ", (id))
    #para traerme toda la infor de los empleados
    empleados=cursor.fetchall()
    conn.commit()
    return render_template("empleados/edit.html", empleados=empleados)

@app.route("/update", methods=['POST'])
def update():
    #actualizar usuario de la base de datos
    #recoger los datos del formulario
    _nombre =request.form['txtNombre']
    _correo =request.form['txtCorreo']
    _foto =request.files['txtFoto']
    id =request.form['txtID']

    sql = "UPDATE empleados SET nombre=%s ,correo=%s WHERE id=%s;"
    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        #si habia subido una foto, que me traiga el nombre de la foto
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)

        #me traigo toda la fila
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        # cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))



    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route("/create")
def create():
    return render_template("empleados/create.html")


@app.route("/store", methods = ['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    if _nombre=='' or _correo=='' or _foto=='':
        flash('Debe completar todos los campos')
        return redirect(url_for('create'))

    #saco fecha y hora para poder renombrar la foto y que no se pise con archivos de igual nombre
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    nuevoNombreFoto = tiempo + _foto.filename

    if _foto.filename != '':
        #hago un if para que no la guarde si no sube foto porque sino guarda un strign feo
        #ahora la guardo así
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);";
    
    datos=(_nombre, _correo, nuevoNombreFoto)

    #llamo a la conection
    conn = mysql.connect()
    #llamo al cursor que es el que viaja a la base de datos
    cursor = conn.cursor()
    #que lleve el pedido sql de arriba
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)