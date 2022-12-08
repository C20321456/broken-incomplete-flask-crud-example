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
        html = html + (f"<tr style='border: 1px solid green'><th  style='border: 1px solid green'>{Result['Name']}</th> <th style='border: 1px solid green'>{Result['Email']}</th></tr> <br>")

    html = f"<table style='border: 1px solid green'><tr style='border: 1px solid green'><th  style='border: 1px solid green'>Name</th><th style='border: 1px solid green'>Email</th></tr>{html}</table>"
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
        return "<h1>Failed to update user in database.,/h1>"


def delete(cursor,name):
    try:
        str = f"DELETE from students where studentName = '{name}'"
        print(str)
        cursor.execute(str)
        mysql.connection.commit()
        print("success")
        return "<h1>Success deleted user in database</h1>"


    except Exception as e:

        print("error")

        print(e)

        return "<h1>Failed to add user to database.</h1>"

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email) # kludge - use stored proc or params
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Success"}' # Really? maybe we should check!
  
@app.route("/") #Default - Show Data
def read(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080

