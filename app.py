# https://prueba-crud-ruleta.herokuapp.com/

import re
from sys import path
from flask import Flask
from flask import render_template,request,redirect,flash,url_for
from flask.helpers import url_for
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime
from funciones import juego_ruleta
import os


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

app.secret_key="InterTelco"

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

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
    #print(jugadores)

    return render_template('usuarios/edit.html', jugadores=jugadores)

@app.route('/update', methods = ['POST'])
def update():
    nombre = request.form['txtNombre']
    edad = request.form['txtEdad']
    dinero = request.form['txtDinero']
    #foto = request.files['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE usuarios SET name=%s, age=%s, cash=%s  WHERE id=%s;"
    datos = (nombre,edad, dinero, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    # if foto.filename != '':
    #     nuevaFoto = tiempo+foto.filename
    #     foto.save("uploads/"+nuevaFoto)
    #     cursor.execute("SELECT image FROM usuarios WHERE id=%s",id)
    #     file=cursor.fetchall()

    #     os.remove(os.path.join(app.config['CARPETA'],file[0][0]))
    #     cursor.execute("UPDATE image SET image=%s WHERE id=%s",nuevaFoto,id)
    #     conn.commit()

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
     foto = request.files['txtFoto']
     
     if nombre == '' or edad == '' or dinero == '' or foto == '':
         flash('Recuerde llenar los datos de los campos')
         return redirect(url_for('create'))

     now = datetime.now()
     tiempo=now.strftime("%Y%H%M%S")

     if foto.filename != '':
        nuevaFoto = tiempo+foto.filename
        foto.save("uploads/"+nuevaFoto)
     
     sql = "INSERT INTO `usuarios` (`id`, `name`, `age`, `cash`, `image`) VALUES  (NULL, %s, %s, %s, %s);"
     #sql = "INSERT INTO `usuarios` (`id`, `name`, `age`, `cash`) VALUES  (NULL, %s, %s, %s);"
     print(nuevaFoto)
     datos = (nombre, edad, dinero, nuevaFoto)
     #datos = (nombre, edad, dinero)
     conn = mysql.connect()
     cursor = conn.cursor()
     cursor.execute(sql,datos)
     conn.commit()
     return redirect('/')


@app.route('/ruleta', methods = ['POST', 'GET'])
def ruleta():
    
    if request.method == 'GET':
        sql = "SELECT * FROM `usuarios`;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)

        jugadores = cursor.fetchall()
        #print(jugadores)

        conn.commit()
        return render_template('usuarios/ruleta.html', jugadores=jugadores)
    else:
        apuesta = request.form['txtApuesta']
        id = request.form['txtJugador']
        color = request.form["txtTipo"]

        sql= "SELECT cash FROM usuarios WHERE id=%s;"
        datos = (id)
        
        conn = mysql.connect()
        cursor = conn.cursor()    
        cursor.execute(sql,datos)
        dinero = cursor.fetchall()
        conn.commit()
        #print(id,dinero[0][0],color,apuesta)
        saldo=int(dinero[0][0])
        #print(saldo)

        if saldo == 0:
            #print("Sin saldo para apostar")
            flash('Sin saldo para apostar','alert alert-danger')
            #error = 'Sin saldo para apostar'
        elif saldo <= 1000:
            apuesta = saldo
            saldo = juego_ruleta(saldo,color,apuesta)
        else:
            saldo = juego_ruleta(saldo,color,apuesta)


        sql = "UPDATE usuarios SET cash=%s  WHERE id=%s;"
        datos = (saldo, id)
        conn = mysql.connect()
        cursor = conn.cursor()    
        cursor.execute(sql,datos)
        conn.commit()

        return redirect(url_for('ruleta'))


if __name__=='__main__':
    app.run(debug=True)
