from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace these with your actual database credentials
db_config = {
    'user': 'root',
    'password': 'luke@0078',
    'host': 'localhost',
    'database': 'student_db',
}

valid_username = "admin"
valid_password = "password123"


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == valid_username and password == valid_password:
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get form data
        name = request.form["student_name"]
        dob = request.form["date_of_birth"]
        usn = request.form["usn"]

        # Insert data into the database
        insert_query = "INSERT INTO students (name, dob, usn) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, dob, usn))
        conn.commit()
        # Fetch data from the database including the ID field
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        conn.close()

    # Fetch data from the database to display on the dashboard
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Replace 'your_table_name' with the name of your table in the database
        query = "SELECT * FROM students"
        cursor.execute(query)

        # Fetch data from the database
        data = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        # Handle any errors that may occur during database connection
        print("Error: ", err)
        data = None

    return render_template("dashboard.html", data=data)


@app.route("/logout")
def logout():
    # Redirect to the login page after logging out
    return redirect(url_for("login"))


@app.route("/add_student", methods=["POST"])
def add_student():
    if request.method == "POST":
        name = request.form["student_name"]
        dob = request.form["date_of_birth"]
        usn = request.form["usn"].upper()  # Convert to uppercase

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the 'students' table, excluding the ID field
        insert_query = "INSERT INTO students (name, dob, usn) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, dob, usn))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Redirect back to the dashboard
        return redirect(url_for("dashboard"))


@app.route("/delete_student", methods=["POST"])
def delete_student():
    if request.method == "POST":
        student_name = request.form["student_name"]

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Delete the student from the database
        delete_query = "DELETE FROM students WHERE usn = %s"
        cursor.execute(delete_query, (student_name,))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Redirect back to the dashboard
        return redirect(url_for("dashboard"))


@app.route("/update_student", methods=["POST"])
def update_student():
    if request.method == "POST":
        student_name = request.form["student_name"]
        new_name = request.form["new_name"]
        new_date_of_birth = request.form["new_date_of_birth"]
        new_usn = request.form["new_usn"]

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the student in the database
        update_query = "UPDATE students SET name = %s, dob = %s, usn = %s WHERE name = %s"
        cursor.execute(
            update_query, (new_name, new_date_of_birth, new_usn, student_name))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Redirect back to the dashboard
        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
