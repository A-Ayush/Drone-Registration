from datetime import datetime
from webpage import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    dt = db.relationship('Details', backref='user', uselist = False)
    drones = db.relationship('Dronedetails', backref='owner')

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,fullname,user_id):
        self.fullname = fullname
        self.user_id = user_id



class My_Drone(db.Model):
    drone_type_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), unique=True, nullable=False)
    nameOfManufacture = db.Column(db.String(50), nullable=False)
    droneType = db.Column(db.String(50), nullable=False)
    maxTakeOffWeight = db.Column(db.Integer, nullable=False)
    maxHeightAttainable = db.Column(db.Integer, nullable=False)

class Dronedetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)
    nameOfManufacture = db.Column(db.String(50), nullable=False)
    droneType = db.Column(db.String(50), nullable=False)
    maxTakeOffWeight = db.Column(db.Integer, nullable=False)
    maxHeightAttainable = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,model_name,nameOfManufacture,droneType,maxTakeOffWeight,maxHeightAttainable,owner_id):
        self.model_name = model_name
        self.nameOfManufacture = nameOfManufacture
        self.droneType = droneType
        self.maxTakeOffWeight = maxTakeOffWeight
        self.maxHeightAttainable = maxHeightAttainable
        self.owner_id = owner_id




