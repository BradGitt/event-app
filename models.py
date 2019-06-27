from runapp import db

class User(db.Model):
	id 		  = db.Column(db.Integer,primary_key=True)
	public_id = db.Column(db.String(50),unique=True)
	fname 	  = db.Column(db.String(50))
	lname 	  = db.Column(db.String(50))
	password  = db.Column(db.String(80))
	admin 	  = db.Column(db.Boolean)

class Event(db.Model): #Additional Attributes - Question 5
	id   		  = db.Column(db.Integer, primary_key=True)
	title  		  = db.Column(db.String(100),nullable=False)
	name		  = db.Column(db.String(50),nullable=False)
	public_name = db.Column(db.String(50),unique=True)
	description   = db.Column(db.String(1000),nullable=False)
	category      = db.Column(db.String(50),nullable=False)
	start_date    = db.Column(db.String(20),nullable=False)
	start_time    = db.Column(db.String(20),nullable=False)
	end_date	  = db.Column(db.String(20),nullable=False)
	end_time      = db.Column(db.String(20),nullable=False)
	cost		  = db.Column(db.Float,nullable=False)
	venue		  = db.Column(db.String(100),nullable=False)
	visible		  = db.Column(db.Boolean,nullable=False)
	
class Plans(db.Model):
	userId	      = db.Column(db.Integer,db.ForeignKey('user.id'))
	eventId	=db.Column(db.Integer,db.ForeignKey('event.id'))
	

class EventFlyer(db.Model):
	id   		  = db.Column(db.Integer,primary_key=True)
	public_name   = db.Column(db.String(50),unique=True)
	eventId       = db.Column(db.Integer,db.ForeignKey('event.id'))
	flyerPath	  = db.Column(db.String(100),nullable=False)



class EventFeedback(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(50))
	rating = db.Column(db.Integer)
	eventId = db.Column(db.Integer,db.ForeignKey('event.id'))
	comment = db.Column(db.String(100))
