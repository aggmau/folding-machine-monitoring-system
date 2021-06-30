from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'bismillah'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/mesintekuk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'secret_xxx'

db = SQLAlchemy(app)
engine = create_engine('mysql://root@localhost/mesintekuk')

class Operasi(db.Model):
    __tablename__   = "operation"
    id_operation    = db.Column(db.Integer, primary_key = True)
    id_order        = db.Column(db.String(12))
    id_operator     = db.Column(db.String(12))
    id_workpiece    = db.Column(db.String(12))
    id_machine      = db.Column(db.String(10))
    start_schedule  = db.Column(db.String(20))
    finish_schedule = db.Column(db.String(20))
    action_on       = db.Column(db.String(30))
    action_off      = db.Column(db.String(30))

    def __init__(self, id_operation, id_order, id_operator,id_workpiece, id_machine, start_schedule, finish_schedule, action_on, action_off):
        self.id_operation       = id_operation
        self.id_order           = id_order
        self.id_operator        = id_operator
        self.id_workpiece       = id_workpiece
        self.id_machine         = id_machine
        self.start_schedule     = start_schedule
        self.finish_schedule    = finish_schedule
        self.action_on          = action_on
        self.action_off         = action_off

class Orders(db.Model) :
    __tablename__   = "orders"
    id_order        = db.Column(db.Integer, primary_key = True)
    id_product      = db.Column(db.String(10))
    id_customer     = db.Column(db.String(10))
    due_date        = db.Column(db.Integer)
    quantity        = db.Column(db.String(30))
    status          = db.Column(db.String(10))

    def __init__(self, id_order, id_product, id_customer, due_date, quantity, status):
        self.id_order   = id_order
        self.id_product = id_product
        self.id_customer= id_customer
        self.due_date   = due_date
        self.quantity   = quantity
        self.status     = status

class akun(db.Model) :
    __tablename__   = "akun"
    username        = db.Column(db.String(12), primary_key = True)
    password        = db.Column(db.String(20))
    email           = db.Column(db.String(50))

    def __init__(self, username, password, email):
        self.username   = username
        self.password   = password
        self.email      = email

pwds = ""
sesi = 0
#login page
@app.route("/login", methods=["GET", "POST"])
def login():
    global username
    global sesi
    global pwds
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pwds = engine.execute("SELECT password FROM akun WHERE username='%s'" % (username)).cursor
        for pwd in pwds :
            if pwd[0] == password :
                sesi = 1
                print('logged in')
                print('sesi = %s'% (sesi))
                return redirect(url_for("dashboard"))
            else :
                flash("Invalid")
                return redirect(url_for("login"))
        pwds.close()
    return render_template('login.html', pwds=pwds)

#logout
@app.route('/logout')
def logout():
    sesi = 0
    return redirect(url_for("login"))

#home
@app.route('/')
def dashboard():
    if sesi == 1 :
        return render_template('dashboard.html')   
    else :
        return redirect(url_for("login"))      

#orders
@app.route("/orders")
def orders():
    if sesi == 1 :
        return(render_template("order.html"))  
    else :
        return redirect(url_for("login"))

#order_details
@app.route("/orders/order_details")
def order_details():
     if sesi == 1 :    
        results = engine.execute("SELECT id_order,id_product,id_customer,due_date, quantity FROM orders WHERE status='ON_GOING'").cursor
        for result in results :
            print(result)
        jums = engine.execute("SELECT COUNT(*) FROM operation WHERE id_order='%s'" %(result[0])).cursor
        for jum in jums :
            print(jum)
        results.close()
        jums.close()
        return render_template("order_details.html", results=results, jums=jums)
     else :
         return redirect(url_for("login"))

#workstations
@app.route("/workstations")
def workstations():
    if sesi == 1 :
        return render_template("workstations.html")
    else :
        return redirect(url_for("login"))
    

#CVWS Folding
@app.route("/workstations/cvws01")
def cvws01():
    if sesi == 1 :
        results = engine.execute("SELECT id_order,id_product,id_customer,due_date, quantity FROM orders WHERE status='ON_GOING'").cursor
        for result in results :
            print(result)
        jums = engine.execute("SELECT COUNT(*) FROM operation WHERE id_order='%s'" %(result[0])).cursor
        for jum in jums :
            print(jum)
        results.close()
        jums.close()
        return(render_template("cvws01.html", results=results, jums=jums))  
    else :
        return redirect(url_for("login"))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
