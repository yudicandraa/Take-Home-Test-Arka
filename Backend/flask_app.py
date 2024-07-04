from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

# Function to establish database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="yudicandra.mysql.pythonanywhere-services.com",
            user="yudicandra",
            password="Defeatmyenemy17#",
            database="yudicandra$default"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to execute select queries
def execute_query(query, params=None):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    else:
        return []

# Function to execute insert, update, delete queries
def execute_non_select_query(query, params=None):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor.lastrowid
    else:
        return None

# Function to check database connection
def db_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return True
    else:
        return False

# Function to get all products from the database
def get_all_products():
    query = 'SELECT * FROM Products'
    return execute_query(query)

# Function to get product by id
def get_product_by_id(product_id):
    query = 'SELECT * FROM Products WHERE product_id = %s'
    return execute_query(query, (product_id,))

# Define routes
@app.route('/')
def index():
    is_connected = db_check()
    if is_connected:
        return "<h2>Success</h2>"
    else:
        return "<h2>Failed</h2>"

@app.route('/products', methods=['GET'])
def list_products():
    products = get_all_products()
    products_list = [
        {"product_id": row[0], "product_name": row[1], "description": row[2], "price": row[3]}
        for row in products
    ]
    return jsonify(products_list)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        abort(404)
    row = product[0]
    product_data = {"product_id": row[0], "product_name": row[1], "description": row[2], "price": row[3]}
    return jsonify(product_data)

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'product_name' in request.json:
        abort(400)
    product = {
        "product_name": request.json['product_name'],
        "description": request.json.get('description', ""),
        "price": request.json.get('price', 0)
    }
    query = 'INSERT INTO Products (product_name, description, price) VALUES (%s, %s, %s)'
    product_id = execute_non_select_query(query, (product['product_name'], product['description'], product['price']))
    product['product_id'] = product_id
    return jsonify(product), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if not request.json:
        abort(400)
    product = get_product_by_id(product_id)
    if not product:
        abort(404)
    update_data = {
        "product_name": request.json.get('product_name', product[0][1]),
        "description": request.json.get('description', product[0][2]),
        "price": request.json.get('price', product[0][3])
    }
    query = 'UPDATE Products SET product_name = %s, description = %s, price = %s WHERE product_id = %s'
    execute_non_select_query(query, (update_data['product_name'], update_data['description'], update_data['price'], product_id))
    return jsonify(update_data)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        abort(404)
    query = 'DELETE FROM Products WHERE product_id = %s'
    execute_non_select_query(query, (product_id,))
    return '', 204

@app.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    users_list = [
        {"user_id": row[0], "name": row[1], "email": row[2], "password": row[3]}
        for row in users
    ]
    return jsonify(users_list)

@app.route('/clients', methods=['GET'])
def list_clients():
    clients = get_all_clients()
    clients_list = [
        {"service_id": row[0], "user_id": row[1], "start_date": row[2], "contract_value": row[3]}
        for row in clients
    ]
    return jsonify(clients_list)

if __name__ == '__main__':
    app.run(debug=True)
