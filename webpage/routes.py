from webpage import app,db, bcrypt
from flask import Flask, render_template, url_for, flash, redirect ,session, request
from webpage.forms import RegistrationForm, LoginForm, add_details, drone_details
from webpage.models import User, Details, My_Drone, Dronedetails
from flask_login import login_user, current_user, logout_user, login_required
import requests
from flask_admin import Admin 
from geopy.geocoders import Nominatim
import requests
from flask_admin.contrib.sqla import ModelView


url = ""

admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Details, db.session))
admin.add_view(ModelView(My_Drone, db.session))
admin.add_view(ModelView(Dronedetails,db.session))


@app.route("/home2")
def home2():
    username = session[ "username" ]
    return render_template("view.html", values = User.query.filter_by(username = username), click='login')

@app.route("/db")
def data_base():
    return render_template("database.html", values = User.query.all())


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #r = requests.get(url).json()
    #print(r)
    form = RegistrationForm()
    if "username" in session:
        username = session["username"]
        return render_template("view.html", values = User.query.filter_by(username = username), click='login')
    else:
        if form.validate_on_submit():
            if request.method == "POST":
                username = request.form[ "username" ]
                session[ "username" ] = username
                email = request.form[ "email" ]
                session[ "email" ] = email
                password = request.form[ "password" ]
                session[ "password" ] = password
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
                
                found_user=User.query.filter_by(username = username).first()
                if found_user:
                    flash(f'Account Already exist {form.username.data}!', 'success')
                    return redirect(url_for('register'))
                else:
                    flash(f'Account created for {form.username.data}!', 'success')
                    user = User(username,email,password)
                    db.session.add(user)
                    db.session.commit()

            return redirect(url_for('home2'))
        return render_template('home.html', click= 'home', form=form)



@app.route("/about")
def about():
    click = 'About'
    if "username" in session:
        usr = session[ "username" ]
        if usr :
            click = 'login'
    return render_template('about.html', title='About' , click=click)


@app.route("/reg", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if "username" in session:
        username = session["username"]
        return render_template("view.html", values = User.query.filter_by(username = username), click='login')
    else:
        if form.validate_on_submit():
            if request.method == "POST":
                username = request.form[ "username" ]
                session[ "username" ] = username
                email = request.form[ "email" ]
                session[ "email" ] = email
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  
                #print(password)
                found_user=User.query.filter_by(username = username).first()
                if found_user:
                    flash(f'Username {form.username.data}! Already taken', 'success')
                    return redirect(url_for('register'))
                else:
                    flash(f'Account created for {form.username.data}!', 'success')
                    user = User(username,email,password)
                    db.session.add(user)
                    db.session.commit()

            return redirect(url_for('home2'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "username" in session:
        print("username")
        username = session["username"]
        return render_template("view.html", values = User.query.filter_by(username = username), click='login')
    else:
        if form.validate_on_submit():
            if request.method == "POST":
                email = request.form[ "email" ]
                found_user=User.query.filter_by(email = form.email.data).first()
                #print(found_user)
                if found_user:
                    if found_user.email == email and bcrypt.check_password_hash(found_user.password, form.password.data):
                        click = 'login'
                        session[ "username" ] = found_user.username
                        flash('You have been logged in!', 'success')
                        return redirect(url_for('home2'))
                    else:
                        flash('Login Unsuccessful. Please check username and password', 'danger')
                else:
                     flash('User doesn not exists', 'info')
            else:
                flash('Logged in!')
        return render_template('login.html', click = 'loginhome' ,title='Login', form=form)


'''#@app.route('/upload_yml', methods=['POST'])
def upload_yml():
    """Upload a yaml file."""

    fh = request.files['file']
    _id = randint(1, 100000)

    file_name = '%s.yml' % _id

    file_path = os.path.join(VOLUME_PATH, file_name)

    fh.save(file_path)

    file_entry = FileEntry(
        upload_id=_id,
        file=file_name,
        file_path=file_path
    )

    db.session.add(file_entry)
    db.session.commit()

    return 'FILE UPLOADED SUCCESSFULLY'
'''

@app.route("/details/<u>", methods=['GET', 'POST'])
def details(u=None):
    form = add_details()
    users = User.query.filter_by(username = u).first()
    id = users.id
    D = Details.query.filter_by(user_id = id).first()
    if request.method == "POST":
        fullname = request.form['Fullname']
        print("post:" ,users.id)
        detail = Details(fullname,users.id)
        db.session.add(detail)
        db.session.commit()
        return redirect(url_for('dronename',u=users.username))
    elif D:
        return redirect(url_for('dronename',u=users.username))

    return render_template('details.html',form=form, click = 'login')

@app.route("/<u>/dronename", methods=['GET', 'POST'])
def dronename(u=None):
    form = drone_details()
    if request.method == "POST":
        dname = request.form['Dronename']
        return redirect(url_for('dronedetails', u=u, d=dname))

    return render_template('dronedetails.html', click = 'login' ,title='Mydrone', form=form)

@app.route("/dronedetails/<u>/<d>", methods=['GET', 'POST'])
def dronedetails(d=None,u=None):
    form = drone_details()
    users = User.query.filter_by(username = u).first()
    print(users.id)
    if request.method == "POST":
        Dronename = request.form['Dronename']
        nameOfManufacture = request.form['nameOfManufacture']
        droneType = request.form['droneType']
        maxTakeOffWeight = request.form['maxTakeOffWeight']
        maxHeightAttainable = request.form['maxHeightAttainable']
        dronedetails = Dronedetails(Dronename,nameOfManufacture,droneType,maxTakeOffWeight,maxHeightAttainable,users.id)
        db.session.add(dronedetails)
        db.session.commit()
        return redirect(url_for('home2'))

    return render_template('Mydrone.html', click = 'login' ,title='Mydrone', form=form,values = My_Drone.query.filter_by(model_name = d))

@app.route("/<u>/Dashboard", methods=['GET'])
def Dashboard(u=None):
    users = User.query.filter_by(username = u).first()
    id = users.id
    mydrones = Dronedetails.query.filter_by(owner_id = id).all()
    return render_template('Dashboard.html', click = 'login' ,values = mydrones , title='Mydrones')

@app.route("/<d>/planaflight", methods=['GET','POST'])
def planaflight(d=None):
    name = ""

    geolocator = Nominatim(user_agent="http://127.0.0.1:5000/")
    location = geolocator.geocode("India")
    if request.method == "POST":
        location =  geolocator.geocode(request.form["LOC"])
        name = request.form["LOC"]
        print(location.latitude, location.longitude)
        return render_template('map.html',lat = location.latitude, lng = location.longitude)

    return render_template('map.html',lat = location.latitude, lng = location.longitude)


@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))
