from datetime import datetime, timezone
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)


    groups = db.relationship("Group", secondary="user_groups", back_populates="users")


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


    users = db.relationship("User", secondary="user_groups", back_populates="groups")


    printers = db.relationship("Printer", back_populates="group")



user_groups = db.Table(
    "user_groups",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"))
)



class Printer(db.Model):
    __tablename__ = "printers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="offline")
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

   
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    group = db.relationship("Group", back_populates="printers")

   
    type = db.Column(db.String(50), nullable=True) #mudar depois ou não  
    consumable_name = db.Column(db.String(50), nullable=True)  
    consumable_cost = db.Column(db.Float, nullable=True) 
    consumable_life_pages = db.Column(db.Integer, nullable=True)

    print_jobs = db.relationship("PrintJob", back_populates="printer")

class PrintJob(db.Model):
    __tablename__ = "print_jobs"

    id = db.Column(db.Integer, primary_key=True)
    

    printer_id = db.Column(db.Integer, db.ForeignKey("printers.id"), nullable=False)
    printer = db.relationship("Printer", back_populates="print_jobs")


    pages = db.Column(db.Integer, nullable=False)           
    status = db.Column(db.String(20), nullable=False)       
    submitted_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

   
    user_name = db.Column(db.String(50), nullable=True)     
    file_name = db.Column(db.String(200), nullable=True)   
