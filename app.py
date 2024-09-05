from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema21702'

mysql.init_app(app)

@app.route("/")
def index():

    #guardar usuario en la base de datos
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'gonzalo', 'cabrerao@gmail.com', 'otrafotodemardel.jpg');";
    
    #llamo a la conection
    conn = mysql.connect()
    #llamo al cursor que es el que viaja a la base de datos
    cursor = conn.cursor()
    #que lleve el pedido sql de arriba
    cursor.execute(sql)
    conn.commit()

    return render_template("empleados/index.html")

@app.route("/create")
def create():
    return render_template("empleados/create.html")


@app.route("/store", methods = ['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);";
    
    datos=(_nombre, _correo, _foto)

    #llamo a la conection
    conn = mysql.connect()
    #llamo al cursor que es el que viaja a la base de datos
    cursor = conn.cursor()
    #que lleve el pedido sql de arriba
    cursor.execute(sql, datos)
    conn.commit()
    return render_template("empleados/index.html")


if __name__ == '__main__':
    app.run(debug=True)