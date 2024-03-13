# Librerías
from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS,cross_origin

# Inicializamos Flask con el modulo que será ejecutado
app = Flask(__name__)

# Utilizamos y creamos la variable CORS para evitar que deje de funcionar el servicio si se llama desde un puerto diferente
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Configuración con el servidor de BD MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'

# Inicializamos la BD con los parámetros anteriores
mysql = MySQL(app)

# Obtener información de un cliente
@app.route('/api/clientes/<int:id>')
@cross_origin()
def informacionCliente(id):
    cur = mysql.connection.cursor('SELECT id, Nombre, Apellido, Email, Telefono, Direccion FROM clientes WHERE id = ' + str(id))
    cur.execute()
    data = cur.fetchall()
    content = {}
    for fila in data:
        content = {
            'id':fila[0],
            'Nombre':fila[1],
            'Apellido':fila[2],
            'Email':fila[3],
            'Telefono':fila[4],
            'Direccion':fila[5]
        }
    return jsonify(content)

# Obtener información de los clientes
@app.route('/api/clientes')
@cross_origin()
def informacionClientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, Nombre, Apellido, Email, Telefono, Direccion FROM clientes')
    data = cur.fetchall()
    resultado = []
    for fila in data:
        content = {
            'id':fila[0],
            'Nombre':fila[1],
            'Apellido':fila[2],
            'Email':fila[3],
            'Telefono':fila[4],
            'Direccion':fila[5]
        }
        resultado.append(content)
    return jsonify(resultado)

# Crear un cliente o modificarlo
@app.route('/api/clientes', methods=['POST'])
@cross_origin()
def crearCliente():
    if 'id' in request.json:
        modificarCliente()
    else:
        crearCliente()
    return 'ok'

def crearCliente():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `clientes` (`id`, `Nombre`, `Apellido`, `Email`, `Telefono`, `Direccion`) VALUES (NULL, %s, %s, %s, %s, %s);",
                (request.json['Nombre'], request.json['Apellido'], request.json['Email'], request.json['Telefono'], request.json['Direccion']))
    mysql.connection.commit()
    return 'Cliente Guardado'

def modificarCliente():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `clientes` SET `Nombre` = %s, `Apellido` = %s, `Email` = %s, `Telefono` = %s, `Direccion` = %s WHERE `clientes`.`id` = %s;",
                (request.json['Nombre'], request.json['Apellido'], request.json['Email'], request.json['Telefono'], request.json['Direccion'], request.json['id']))
    mysql.connection.commit()
    return 'Modificación Exitosa'

# Eliminar un cliente
@app.route('/api/clientes/<int:id>', methods=['DELETE'])
@cross_origin()
def eliminarCliente(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `clientes` WHERE `clientes`.`id` = " + str(id))
    mysql.connection.commit()
    return 'Cliente Eliminado'

# Conexión con el FrontEnd
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

# Cargamos todos los archivos
@app.route('/<path:path>')
@cross_origin()
def publicFiles(path):
    return render_template(path)

# Inicializamos el servidor de Flask
if __name__ == '__main__':
    app.run(None,3000,True)