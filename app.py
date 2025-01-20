from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Konfigurasi database
DB_CONFIG = {
    "host": "localhost",
    "database": "testdb",
    "user": "postgres",
    "password": "postgres"  # Ganti dengan password PostgreSQL kamu
}

# Fungsi untuk koneksi ke database
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Endpoint GET halaman home
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Home Page!"}), 200

# Endpoint POST login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validasi sederhana
    if email == "test@example.com" and password == "12345":
        return jsonify({"message": "Login successful!", "token": "mock-token"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint POST untuk mengisi database user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    age = data.get("age")

    if not first_name or not last_name or not age:
        return jsonify({"message": "Missing data"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s)",
        (first_name, last_name, age)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
