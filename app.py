from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
from config import DB_CONFIG 

app = Flask(__name__)
CORS(app) 

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )


@app.route('/')
def home():
    return render_template('index.html')

# Create Employee (POST)
@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        data = request.json
        required_fields = ["name", "interview_time", "details", "notes"]
        
        # Check for missing fields
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = "INSERT INTO employees (name, interview_time, details, notes) VALUES (%s, %s, %s, %s)"
                values = (data['name'], data['interview_time'], data['details'], data['notes'])
                cursor.execute(sql, values)
                db.commit()
        
        return jsonify({"message": "Employee added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get All Employees (GET)
@app.route('/get_employees', methods=['GET'])
def get_employees():
    try:
        with get_db_connection() as db:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()

        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)})

# Search Employee by Name (GET)
@app.route('/search_employee', methods=['GET'])
def search_employee():
    try:
        name = request.args.get('name')
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employees WHERE name LIKE %s", ('%' + name + '%',))
        employees = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify([{"id": emp[0], "name": emp[1], "interview_time": emp[2], "details": emp[3], "notes": emp[4]} for emp in employees])
    except Exception as e:
        return jsonify({"error": str(e)})


# Update Employee (PUT)
@app.route('/update_employee/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        data = request.json
        required_fields = ["name", "interview_time", "details", "notes"]
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = "UPDATE employees SET name=%s, interview_time=%s, details=%s, notes=%s WHERE id=%s"
                values = (data['name'], data['interview_time'], data['details'], data['notes'], id)
                cursor.execute(sql, values)
                db.commit()

        return jsonify({"message": "Employee updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Delete Employee (DELETE)
@app.route('/delete_employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
                db.commit()

        return jsonify({"message": "Employee deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
