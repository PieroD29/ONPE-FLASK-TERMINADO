from flask import Flask, render_template
from flask_cors import CORS
import mysql.connector

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'onpe'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)
app = Flask(__name__)
#CORS(app)

@app.route('/')
def index():
    return 'hola'

@app.route('/actas/numero/<id>')
def actas_numero(id): 
    nActas = 'queso'
    cursor.callproc('sp_getGrupoVotacion', (id,))
    for data in cursor.stored_results():
        nActas = data.fetchone()
    
    return nActas

if __name__ == '__main__':
    app.run(port=5000, debug=True)