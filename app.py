from flask import Flask, render_template,url_for,request,flash
from flask import request

import ibm_db

app = Flask(__name__)
app.secret_key = 'something'
conn = ibm_db.connect("database=bludb;hostname=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; port=32286; uid = psf41693;password = 9fHmQptEBZvfaGva;security =SSL;sslcertificate = DigiCertGlobalRootCA.crt ","","")
print(conn)
print("connection successful")
@app.route("/")
def index():
    return render_template('index.html')

# @app.route('/register')
# def register():
#     return render_template("register.html")

@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/register", methods=['POST','GET'])
def register():
    Firstname = request.form['firstname']
    Lastname = request.form['lastname']
    Email = request.form['email']
    Password = request.form['password']
    Confirmpassword = request.form['confirmpassword']

    # Check if the email is already registered
    sql = "SELECT * FROM register_course WHERE email = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, Email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    # Validate password and confirm password match
    if Password != Confirmpassword:
        msg = "Password and confirm password do not match"
        return render_template("login.html", msg=msg)
    elif len(Password) < 8:
        msg = "Password must be at least 8 characters long"
        return render_template("login.html", msg=msg)

    # If the email is not registered, insert a new row into the table
    if not account:
        sql = "INSERT INTO register_course (firstname, lastname, email, password) VALUES (?, ?, ?, ?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, Firstname)
        ibm_db.bind_param(stmt, 2, Lastname)
        ibm_db.bind_param(stmt, 3, Email)
        ibm_db.bind_param(stmt, 4, Password)
        ibm_db.execute(stmt)
        msg = "Successfully registered. Please use the same credentials to login."
    else:
        msg = "Already registered."

    return render_template("login.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)