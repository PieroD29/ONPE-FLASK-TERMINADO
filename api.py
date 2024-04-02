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

#ACTAS POR NUMERO --------------------------------------------------------------------
@app.route('/actas_numero/<numero_mesa>')
def pst_numero(numero_mesa):
    
    if numero_mesa:
        
        cursor.callproc('sp_getGrupoVotacion',(numero_mesa,))
        for numero in cursor.stored_results():
            data = numero.fetchone()
        
    else :
        data = 'INGRESE UN NUMERO DE ACTA'
    
    return data

#PARTICIPACION -----------------------------------------------------------------------------
@app.route('/participacion')
def participacion():
    cursor.execute('select * from vTotalVotos')
    votos = cursor.fetchone()

    return votos

#PARTICIPACION TOTAL -------------------------------------------------------------------------
@app.route('/participacion_total/<id>') 
def participacion_total(id):
    id_ini =  1 if id == 'Nacional' else 26 if id == 'Extranjero' else 0
    id_fin = 25 if id== 'Nacional' else 30 if id == 'Extranjero' else 0
    
    cursor.callproc('sp_getVotos', (id_ini, id_fin))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    
    return votos_p

#DEPA ----
@app.route('/participacion_total/<id>/<depa>')
def participacion_depa(id, depa):
    cursor.callproc('sp_getVotosDepartamento', (depa,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    
    return votos_p

#PROVINCIA ----
@app.route('/participacion_total/<id>/<depa>/<prov>')
def participacion_prov(id, depa, prov):
    cursor.callproc('sp_getVotosProvincia', (prov,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    return votos_p 

#DISTRITO ----
@app.route('/participacion_total/<id>/<depa>/<prov>/<dist>')
def participacion_dist(id, depa, prov, dist):
    cursor.callproc('sp_getVotosProvincia', (prov,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    return votos_p

#ACTAS_UBIGEO ---------------------------------------------------------------

#DEPARTAMENTOS ----------
@app.route('/actas_ubigeo/<ambito>')
def Departamentos(ambito):
    id_ini =  1 if ambito == 'Peru' else 26 if ambito == 'Extranjero' else 0
    id_fin = 25 if ambito == 'Peru' else 30 if ambito == 'Extranjero' else 0
    
    cursor.callproc('sp_getDepartamentos', (id_ini, id_fin))
    for data in cursor.stored_results():
        departamentos = data.fetchall()
    return departamentos

#PROVINCIAS ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>')
def Provincia(ambito, departamento):
    cursor.callproc('sp_getProvinciasByDepartamento', (departamento,))
    for data in cursor.stored_results():
        provincias = data.fetchall()
    return provincias

#DISTRITOS -----------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>')
def Distritos(ambito, departamento, provincia):
    cursor.callproc('sp_getDistritosByProvincia',(provincia,))
    for data in cursor.stored_results():
        distrito = data.fetchall()
    return distrito

#LOCALES -----------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>')
def Locales(ambito, departamento, provincia, distrito):
    cursor.callproc('sp_getLocalesVotacionByDistrito', (provincia, distrito))
    for data in cursor.stored_results():
        locales = data.fetchall()
    return locales

#LISTADO DE MESAS ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>/<locales>')
def NroMesas(ambito, departamento, provincia, distrito, locales):
    cursor.callproc('sp_getGruposVotacionByProvinciaDistritoLocal', (provincia, distrito, locales))
    for data in cursor.stored_results():
        nroMesas = data.fetchall()
    return nroMesas

#DETALLE DE MESA ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>/<locales>/<Nmesa>')
def DetalleMesa(ambito, departamento, provincia, distrito, locales, Nmesa):
    cursor.callproc('sp_getGrupoVotacionByProvinciaDistritoLocalGrupo',(departamento, provincia, distrito, locales, Nmesa))
    for data in cursor.stored_results():
        nromesa = data.fetchone()
    return nromesa

if __name__ == '__main__':
    app.run(port=5000, debug=True)