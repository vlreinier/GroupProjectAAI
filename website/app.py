from flask import Flask, send_from_directory, jsonify, redirect, request
from pymongo import MongoClient
from database_connections import mdb_connectie, connect_sql
from query import popular,personal,collaborative,content
from lift import lift

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("/index.html", code=302)

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)

@app.route('/popularproducts')
def popularproducts():
    return jsonify(popular(sql_db,mongo_db))

@app.route('/personalproducts', methods=['POST'])
def personalproducts():
    sessiondata = request.json
    return jsonify(personal(sql_db,mongo_db,sessiondata))

@app.route('/collaborativefiltering', methods=['POST'])
def collaborativeproducts():
    sessiondata = request.json
    return jsonify(collaborative(sql_db,mongo_db,sessiondata))
	
@app.route('/contentfiltering', methods=['POST'])
def contentproducts():
    sessiondata = request.json
    return jsonify(content(sql_db,mongo_db,sessiondata))

if __name__ == '__main__':
    mongo_db = mdb_connectie("voordeelshop") # ophalen connectie MongoDB
    sql_db = connect_sql('voordeelshopfull_orders', 'postgres', 'Welkom01!') # ophalen connectie SQL
    #lift(sql_db) # berekenen en invoeren lift 
    app.run() # starten applicatie

