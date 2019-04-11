from flask import Flask, send_from_directory, jsonify, redirect, request
from database_connections import mdb_connectie, connect_sql
from generate_id_list import homepage, personal, collaborative, shoppingcart, loadselected, selectedsimilar, search_on_name
from lift_calculation import lift
from algorithms import calculate_timespan

app = Flask(__name__)


@app.route('/')
def home():
    return redirect("/index.html", code=302)


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)


@app.route('/popularproducts', methods=['POST'])
def popularproducts():
    sessiondata = request.json
    return jsonify(homepage(sql_db, mongo_db, sessiondata, timespan))


@app.route('/personalproducts', methods=['POST'])
def personalproducts():
    sessiondata = request.json
    return jsonify(personal(sql_db, mongo_db, sessiondata))


@app.route('/collaborativefiltering', methods=['POST'])
def collaborativeproducts():
    sessiondata = request.json
    return jsonify(collaborative(sql_db, mongo_db, sessiondata))


@app.route('/shoppingcart', methods=['POST'])
def cart():
    sessiondata = request.json
    return jsonify(shoppingcart(sql_db, mongo_db, sessiondata))


@app.route('/selected', methods=['POST'])
def getselected():
    sessiondata = request.json
    return jsonify(loadselected(sql_db, mongo_db, sessiondata))


@app.route('/selectedsimilar', methods=['POST'])
def getsimilar():
    sessiondata = request.json
    return jsonify(selectedsimilar(sql_db, mongo_db, sessiondata))

@app.route('/searchedproduct', methods=['POST'])
def searchproducts():
    sessiondata = request.json
    return jsonify(search_on_name(sql_db, mongo_db, sessiondata))


if __name__ == '__main__':
    mongo_db = mdb_connectie("voordeelshop")  # ophalen connectie MongoDB
    sql_db = connect_sql('voordeelshop_complete', 'postgres', 'Welkom01!')  # ophalen connectie SQL
    timespan = calculate_timespan(sql_db, 20)
    #lift(sql_db) # berekenen en invoeren lift
    app.run()  # starten applicatie