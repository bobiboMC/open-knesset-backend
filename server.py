from flask import Flask,request, url_for
from flask_cors import CORS
import api.db as DB
import api.queries as QUERY
import json
app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
app.secret_key = 'oknesset#@@#'
app.config['ENV'] = "development"
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return {'success': True, 'data' : []}, 200
    
@app.route('/db')
def db_tables():
    return {'success': True, 'data' : DB.get_data("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")}, 200

@app.route('/<table_name>/list')
def get_table_list(table_name):
    if len(table_name.split(' ')) != 1: #one word only,that is table's name
        data=ValueError("You must give table's name!")
        status_code=400
    else:
        status_code = 200
        query = "SELECT * FROM %s"
        data = DB.get_data_list(query,table_name)
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code
    return {'success': True, 'data' :data }, status_code 
    

@app.route('/discribe')
def get_discribe():
    return {'success': True, 'data' : DB.get_discribe('members_presence')}, 200
    

@app.route('/member_kns_by_individual/<int:id>')
@app.route('/member_kns_by_personal/<int:id>')
def get_member_kns(id):
    status_code=200
    id_field = (
        "mk_individual_id"
        if request.path == f"/member_kns_by_individual/{str(id)}"
        else "PersonID"
    )
    query = QUERY.get_member_kns_query(id_field)
    data = DB.get_fully_today_kns_member(query, (id,))
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code 

    return {'success': True, 'data' :data }, status_code 

@app.route('/minister_by_individual/<int:id>')
@app.route('/minister_by_personal/<int:id>')
def get_minister(id):
    status_code=200
    id_field = (
        "mk_individual_id"
        if request.path == f"/minister_by_individual/{str(id)}"
        else "PersonID"
    )
    query = QUERY.get_minister_query(id_field)
    data = DB.get_fully_today_kns_member(query, (id,))
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code 

    return {'success': True, 'data' :data }, status_code         

# favicon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='/images/hasadna-logo.ico')
    

if __name__ == "__main__":
    app.run(debug=True)
