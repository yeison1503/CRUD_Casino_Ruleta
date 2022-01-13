import numpy as np
import random
from flask import flash

def juego_ruleta(saldo,color,apuesta):
    probV=0.02
    probR=0.49
    probN=0.49
    cant= 100
    verde="verde"
    negro="negro"
    rojo="rojo"
    COLOR = np.random.choice([rojo, negro, verde], size = 100, p=[0.49,0.49,0.02])

    color_aleatorio = COLOR[random.randint(0, 100)]
    #print("\nColor obtenido: " + color_aleatorio)
    flash("Color obtenido: " + color_aleatorio ,'alert alert-info')
    if color == color_aleatorio:
        # Si el usuario Acierta o no
        if color == "verde":
            #print("la apuesta se multiplica por 15")
            flash('Sin saldo para apostar','alert alert-success')
            saldo += int(apuesta) * 15
        else:
            flash('La apuesta se multiplica por 2','alert alert-success')
            #print("La apuesta se multiplica por 2")
            saldo += int(apuesta) * 2
    else:
        #print("Pierde lo apostado")
        flash('Pierde lo apostado','alert alert-danger')
        saldo -= int(apuesta)
    
    return saldo

#Comandos para crear la base de datos en MySQL

# CREATE DATABASE sistema;
# USE sistema;
# CREATE TABLE IF NOT EXISTS usuarios(
# 	id BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
# 	name VARCHAR(255) NOT NULL,
# 	age SMALLINT NOT NULL,
#   cash SMALLINT NOT NULL,
#   image VARCHAR(255) NOT NULL,
# 	PRIMARY KEY(id)
# );