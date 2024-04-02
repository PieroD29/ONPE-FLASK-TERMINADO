from flask import Flask, render_template, request
import mysql.connector

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'onpe'
}

#PSDT: Parece que en la base de datos del host remoto no se encuentra creado la vista de vTotalVotos, por lo que 
#      puede que ocurra algun error al momento de ejecutar participacion. Segun el script sql que se encuentra en anuncion
#      si existe la vista de vTotalVotos, es el script Onpe.sql en la linea 62, por lo que recimiendo usar la base de datos local
configRemote = {
    'host': 'srv1101.hstgr.io',
    'user': 'u584908256_onpe',
    'password': 'Senati2023@',
    'database': 'u584908256_onpe'
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)
app = Flask(__name__)

#INDEX ----------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/actas_numero')
def actas_Numero(): 
    return render_template('actas_numero.html')

@app.route('/participacion')
def participacion():
    
    cursor.execute('select * from vTotalVotos')
    votos = cursor.fetchone()
    
    print(votos)
    
    return render_template('participacion.html', votos=votos)
#INDEX ----------------------------------------------------------------------

#PARTICIPACION --------------------------------------------------------------
count_p = None
#AMBITO ----
@app.route('/participacion_total/<id>') 
def participacion_total(id):
    count_p = 1
    id_ini =  1 if id == 'Nacional' else 26 if id == 'Extranjero' else 0
    id_fin = 25 if id== 'Nacional' else 30 if id == 'Extranjero' else 0
    
    cursor.callproc('sp_getVotos', (id_ini, id_fin))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    
    print(votos_p)
    
    return render_template('participacion_total.html', votos_p = votos_p, id = id, count_p = count_p)

#DEPA ----
@app.route('/participacion_total/<id>/<depa>')
def participacion_depa(id, depa):
    count_p = 2
    cursor.callproc('sp_getVotosDepartamento', (depa,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    
    return render_template('participacion_total.html', votos_p = votos_p, id = id, depa = depa, count_p = count_p)

#PROVINCIA ----
@app.route('/participacion_total/<id>/<depa>/<prov>')
def participacion_prov(id, depa, prov):
    count_p = 3
    cursor.callproc('sp_getVotosProvincia', (prov,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    return render_template('participacion_total.html', votos_p = votos_p, id = id, depa = depa, prov = prov, count_p = count_p)

#DISTRITO ----
@app.route('/participacion_total/<id>/<depa>/<prov>/<dist>')
def participacion_dist(id, depa, prov, dist):
    count_p = 4
    cursor.callproc('sp_getVotosProvincia', (prov,))
    for data in cursor.stored_results():
        votos_p = data.fetchall()
    return render_template('participacion_total.html', votos_p = votos_p, id = id, depa = depa, prov = prov, dist = dist, count_p = count_p)
#PARTICIPACION --------------------------------------------------------------

#POST ACTAS NUMERO-----------------------------------------------------------------------
@app.route('/actas_numero', methods=["POST"])
def pst_numero():
    numero_mesa = request.form['nroMesa']
    data = None
    proceso = None
    msg = None
    
    if numero_mesa:
        
        if len(numero_mesa) < 6 or len(numero_mesa) > 6:
            msg = 'INCORRECTO'
        
        elif numero_mesa == '000000' or numero_mesa == '999999':
            msg = 'NO EXISTE'
            
        else:
            proceso = 1
            print(numero_mesa)
            
            cursor.callproc('sp_getGrupoVotacion',(numero_mesa,))
            for numero in cursor.stored_results():
                data = numero.fetchone()
            print(data)
        
    else :
        msg = 'INGRESE UN NUMERO DE ACTA'
    
    return render_template('actas_numero.html', proceso=proceso, data=data, msg = msg)
#POST ----------------------------------------------------------------

#ACTAS UBIGEO --------------------------------------------------------
@app.route('/actas_ubigeo')
#INDEX -------
def actas_Ubigeo():
    return render_template('actas_ubigeo.html')

#DEPARTAMENTOS ----------
@app.route('/actas_ubigeo/<ambito>', methods=['POST'])
def Departamentos(ambito):
    print("Ambito:", ambito)
    id_ini =  1 if ambito == 'Peru' else 26 if ambito == 'Extranjero' else 0
    id_fin = 25 if ambito == 'Peru' else 30 if ambito == 'Extranjero' else 0
    
    cursor.callproc('sp_getDepartamentos', (id_ini, id_fin))
    for data in cursor.stored_results():
        departamentos = data.fetchall()
    print(departamentos)
    print(cursor)
    return departamentos

#PROVINCIAS ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>', methods=['POST'])
def Provincia(ambito, departamento):
    print("Ambito: ", ambito, "\nDepartamento:", departamento)
    
    cursor.callproc('sp_getProvinciasByDepartamento', (departamento,))
    for data in cursor.stored_results():
        provincias = data.fetchall()

    print(provincias)
    return provincias

#DISTRITOS -----------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>', methods=['POST'])
def Distritos(ambito, departamento, provincia):
    print("Ambito: ", ambito, "\nDepartamento:", departamento, "\nProvincia:", provincia)
    
    cursor.callproc('sp_getDistritosByProvincia',(provincia,))
    for data in cursor.stored_results():
        distrito = data.fetchall()
        print(cursor.rowcount)
    print(distrito)
    return distrito

#LOCALES -----------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>', methods=['POST'])
def Locales(ambito, departamento, provincia, distrito):
    print("Ambito: ", ambito, "\nDepartamento:", departamento, "\nProvincia:", provincia, "\nDistrito:", distrito)
    
    cursor.callproc('sp_getLocalesVotacionByDistrito', (provincia, distrito))
    for data in cursor.stored_results():
        locales = data.fetchall()

    print(locales)
    return locales

#LISTADO DE MESAS ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>/<locales>', methods=['POST'])
def NroMesas(ambito, departamento, provincia, distrito, locales):
    print("Ambito: ", ambito, "\nDepartamento:", departamento, "\nProvincia:", provincia, "\nDistrito:", distrito, "\nLocales:", locales)
    
    cursor.callproc('sp_getGruposVotacionByProvinciaDistritoLocal', (provincia, distrito, locales))
    for data in cursor.stored_results():
        nroMesas = data.fetchall()

    return nroMesas

#DETALLE DE MESA ------------
@app.route('/actas_ubigeo/<ambito>/<departamento>/<provincia>/<distrito>/<locales>/<Nmesa>', methods=['POST'])
def DetalleMesa(ambito, departamento, provincia, distrito, locales, Nmesa):
    print("Ambito: ", ambito, "\nDepartamento:", departamento, "\nProvincia:", provincia, "\nDistrito:", distrito, "\nLocales:", locales, "\nMesa:", Nmesa)
    
    cursor.callproc('sp_getGrupoVotacionByProvinciaDistritoLocalGrupo',(departamento, provincia, distrito, locales, Nmesa))
    for data in cursor.stored_results():
        nromesa = data.fetchone()
    print(nromesa)
    return nromesa

#ACTAS UBIGEO --------------------------------------------------------

if __name__ == '__main__':
    app.run(port=5000, debug=True)