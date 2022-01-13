# CRUD_Casino_Ruleta

En este repositorio se desarrolló un programa para la creación de usuarios, donde además se pueden modificar, eliminar y editar los usuarios ya inscritos en la base de datos, la cual fue elaborada con MySQL.

Además, se puede jugar a la ruleta con cualquier usuario registrado en la base de datos, este juego consiste en elegir un usuario y que este pueda apostar un monto del saldo disponible, el juego devuelve aleatoriamente un color y cada color tiene una probabilidad asociada.

Para iniciar la ejecución se debe crear la base de datos de MySQL, para cual se debe instalar XAMPP con anterioridad ya que esta provee los servicios para la base de datos.

Para la creación de la base de datos se deben ingresar los siguientes comandos en el Shell o terminal de XAMPP.

#### CREATE DATABASE sistema;
#### USE sistema;
CREATE TABLE IF NOT EXISTS usuarios(
 	id BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
 	name VARCHAR(255) NOT NULL,
 	age SMALLINT NOT NULL,
  cash SMALLINT NOT NULL,
  image VARCHAR(255) NOT NULL,
 	PRIMARY KEY(id)
);

Para el despliegue de la aplicación solo basta con ejecutar el archivo app.py en cualquier terminal de un sistema operativo que tenga instalado Python, por ejemplo, un framework como anaconda o visual studio code.

La ejecución del programa se realiza con el siguiente comando "python .\app.py" en el Shell o terminal del sistema operativo o aplicación, también tiene que estar ubicado en la ruta donde están guardadas las carpetas del programa.

Cuando se haya ejecutado la aplicación con el comando anterior se debe abrir una pestaña en cualquier navegador y dirigirse a la siguiente URL “http://127.0.0.1:5000/” o “http://localhost:5000/” y listo, ya se puede ingresar, eliminar o editar usuarios o jugar a la ruleta con los usuarios ya inscritos.

