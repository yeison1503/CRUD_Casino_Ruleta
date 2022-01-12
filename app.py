from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():

    sql = "SELECT * FROM `usuarios`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    jugadores = cursor.fetchall()
    #print(jugadores)

    conn.commit()
    return render_template('usuarios/index.html', jugadores=jugadores)

@app.route('/destroy/<int:id>')
def destroy(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=%s",(id))
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=%s",(id))
    jugadores = cursor.fetchall()
    conn.commit()

    return render_template('usuarios/edit.html', jugadores=jugadores)

@app.route('/update', methods = ['POST'])
def update():
    nombre = request.form['txtNombre']
    edad = request.form['txtEdad']
    dinero = request.form['txtDinero']
    foto = request.form['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE usuarios SET name=%s, age=%s, cash=%s, image=%s  WHERE id=%s;"
    datos = (nombre,edad, dinero,foto, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

@app.route("/create")
def create():
    return render_template('usuarios/create.html')

@app.route('/store', methods=['POST'])
def storage():
     nombre = request.form['txtNombre']
     edad = request.form['txtEdad']
     dinero = request.form['txtDinero']
     foto = request.form['txtFoto']

     now = datetime.now()
     tiempo=now.strftime("%Y%H%M%S")

     if foto.filename != '':
         nuevaFoto = tiempo+foto.filename
         foto.save("uploads/"+nuevaFoto)
    
     sql = "INSERT INTO `usuarios` (`id`, `name`, `age`, `cash`, 'image') VALUES (NULL, %s, %s, %s, %s);"
     datos = (nombre, edad, dinero, foto)
     conn = mysql.connect()
     cursor = conn.cursor()
     cursor.execute(sql,datos)
     conn.commit()
     return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
