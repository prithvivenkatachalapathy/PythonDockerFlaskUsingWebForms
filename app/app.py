from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'taxData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'things Data'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM taxables')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, things=result)


@app.route('/view/<int:thing_id>', methods=['GET'])
def record_view(thing_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM taxables WHERE id=%s', thing_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', thing=result[0])


@app.route('/edit/<int:thing_id>', methods=['GET'])
def form_edit_get(thing_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM taxables WHERE id=%s', thing_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', thing=result[0])


@app.route('/edit/<int:thing_id>', methods=['POST'])
def form_update_post(thing_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Item'), request.form.get('Cost'), request.form.get('Tax'),
                 request.form.get('Total'), thing_id)
    sql_update_query = """UPDATE taxables t SET t.Item = %s, t.Cost = %s, t.Tax = %s, t.Total = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/things/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New thing Form')


@app.route('/things/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Item'), request.form.get('Cost'), request.form.get('Tax'),
                 request.form.get('Total'))
    sql_insert_query = """INSERT INTO taxables (Item,Cost,Tax,Total) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:thing_id>', methods=['POST'])
def form_delete_post(thing_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM taxables WHERE id = %s """
    cursor.execute(sql_delete_query, thing_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/things', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM taxables')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/things/<int:thing_id>', methods=['GET'])
def api_retrieve(thing_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM taxables WHERE id=%s', thing_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/things/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Item'], content['Cost'], content['Tax'],
                 content['Total'])
    sql_insert_query = """INSERT INTO taxables (Item,Cost,Tax,Total) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/things/<int:thing_id>', methods=['PUT'])
def api_edit(thing_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Item'], content['Cost'], content['Tax'],
                 content['Total'], thing_id)
    sql_update_query = """UPDATE taxables t SET t.Item = %s, t.Cost = %s, t.Tax = %s, t.Total = 
        %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()

    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/things/<int:thing_id>', methods=['DELETE'])
def api_delete(thing_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM taxables WHERE id = %s """
    cursor.execute(sql_delete_query, thing_id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)