from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.105.168.32'
mysql.init_app(app)

def insert(cursor, name, email):
    string = f"INSERT INTO students(studentName,email) VALUES('{name}','{email}')"

    try:
        cursor.execute(string)
        mysql.connection.commit()
        print("YUPPPP")
        return "<h1>Success adding user to database</h1>"
    except Exception as e:
        print("NOOOOO")
        print(e)
        return "<h1>Failed to add user to database.</h1>"



def read(cursor):
    cursor.execute('''SELECT * FROM students''')  # execute an SQL statment
    rv = cursor.fetchall()  # Retreive all rows returend by the SQL statment
    Results = []
    html = ""
    for row in rv:  # Format the Output Results and add to return string
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        html = html + (f"<tr style='border: 1px solid blue'><th  style='border: 1px solid blue'>{Result['Name']}</th> <th style='border: 1px solid blue'>{Result['Email']}</th></tr> <br>")

    html = f"<table style='border: 1px solid blue'><tr style='border: 1px solid red'><th  style='border: 1px solid black'>Name</th><th style='border: 1px solid red'>Email</th></tr>{html}</table>"
    # response = {'Results': Results, 'count': len(Results)}
    # ret = app.response_class(
    #     response=json.dumps(response),
    #     status=200,
    #     mimetype='application/json'
    # )
    # return ret  # Return the data in a string format
    return html

def update(cursor,id,email):
    try:
        cursor.execute(f"UPDATE students set email = '{email}' where studentID = '{id}'")
        mysql.connection.commit()
        return "<h1>Success updating user in database</h1>"
    except:
        return "<h1>Unable to upadte user.,/h1>"


def delete(cursor,name):
    try:
        str = f"DELETE from students where studentName = '{name}'"
        print(str)
        cursor.execute(str)
        mysql.connection.commit()
        print("YUPPPP")
        return "<h1>User Deleted successfully</h1>"


    except Exception as e:

        print("NOOOOO")

        print(e)

        return "<h1>Failed to add user to database.</h1>"
@app.route("/add")  # Add Student
def add():
    name = request.args.get('name')
    email = request.args.get('email')
    cur = mysql.connection.cursor()  # create a connection to the SQL instance

    return insert(cur, name, email)


@app.route("/hello")  # Add Student
def hello():
    return '<h1>Hello World</h1>'


@app.route("/")  # Default - Show Data
def read_users():  # Name of the method
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    return read(cur)

@app.route("/update")  # Default - Show Data
def update_users():  # Name of the method
    cur = mysql.connection.cursor()  # create a connection to the SQL instance

    id = request.args.get('id')
    print(id)
    email = request.args.get('email')
    print(email)
    return update(cur, id, email)


@app.route("/delete", methods=['GET', 'POST'])  # Default - Show Data
def delete_users():
    print(request.json)
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    name = request.json["name"]
    print("Name is " + name)
    return delete(cur, name)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')  # Run the flask app at port 8080
