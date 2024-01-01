import os
from flask import Flask
from flaskext.mysql import MySQL      # For newer versions of flask-mysql 
app = Flask(__name__)

mysql = MySQL()

mysql_database_host = 'DB_HOST' in os.environ and os.environ['DB_HOST'] or 'localhost'
password_path = '/run/secrets/db_password'
password_file = open(password_path, 'r')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ['DB_USER']
app.config['MYSQL_DATABASE_DB'] = os.environ['DB_NAME']
app.config['MYSQL_DATABASE_HOST'] = mysql_database_host
app.config['MYSQL_DATABASE_PASSWORD'] = password_file.read()
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
    return "hostname: " + os.environ['HOSTNAME']

@app.route('/read')
def read():
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    result = []
    while row is not None:
      result.append(row[0])
      row = cursor.fetchone()

    return ", ".join(result)

# TO DO 
# @app.route('/how are you')
# def hello():
#     return 'I am good, how about you?'

if __name__ == "__main__":
    app.run()