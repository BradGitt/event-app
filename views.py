from flask import request, jsonify, make_response
from runapp import app, db
import uuid
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Event, Feedback, EventFlyer
from functools import wraps
from werkzeug.utils import secure_filename

# create decorated function for token authorization
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is not present!'}), 401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message':'Not a valid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# create decorated function for admin
def admin_required(f):
    @wraps(f)
    def decorated(current_user,*args, **kwargs):
        if not current_user.admin:
            return jsonify({'message':'You are not authorized to perform this action'})
        return f(current_user, *args, **kwargs)
    return decorated

# Create User   
@app.route('/user',methods=['POST'])
def create_user():
    # if not current_user.admin:
    #     return jsonify({'message':'You are not authorized to perform this action'})
    data = request.get_json()
    pword_hashed = generate_password_hash(data['password'],method='sha256')
    user = User(public_id=str(uuid.uuid4()), name=data['name'],password=pword_hashed,admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'The user was created'})

# Edit to Update User profile  
@app.route('/user/edit/<public_id>',methods=['PUT'])
@token_required
def edit_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'This user does not exist!'})
      
    data = request.get_json()
    pword_hashed = generate_password_hash(data['password'],method='sha256')
    user.public_id=user.public_id
    user.name=data['name']
    user.password=pword_hashed
    db.session.commit()
    return jsonify({'message':'The user profile was updated'})

# Read All Users
@app.route('/user',methods=['GET'])
@token_required
@admin_required
def list_users(current_user):
  

    users = User.query.all()
    users_list = []
    for user in users:
        user_data = dict()
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['admin'] = user.admin

        users_list.append(user_data)

    return jsonify({'users':users_list})

# search user by id
@app.route('/user/<public_id>', methods=['GET'])
@token_required
@admin_required
def getuser(current_user, public_id):
    if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'This user does not exist!'})
    user_dict = dict()
    user_dict['public_id'] = user.public_id
    user_dict['name'] = user.name
    user_dict['admin'] = user.admin
    return jsonify({'user':user_dict})

# Delete user by id
@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
@admin_required
def delete(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'This user does not exist!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'This user was deleted'}) 

# Update user to make admin
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
@admin_required
def make_admin(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message':'This user does not exist!'})
    user.admin=True
    db.session.commit()
    return jsonify({'message':'This user is now an admin'})


# Login 
# Question 1- When the user login it will generate a JSON token where it will be stored in the Headers section in Postman where they can use 
# the different routes for the API.
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Authentication not verified',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Authentcation not verified',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Authentication not verified',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})


#Question 2- When the user is login i.e authenticated they can accesss the dfiiferent routes to perfrom CRUD operations(functions are below) on 
# the events(assuming an event is created.)
#Question 2b- The function get_one_event would deal with searching for one particular event
#Questin 3 - 2 Users already have been created with admin roles in Postman where I called the promote_user function so that they are promoted
# to Admin(in Screenshots).

#######################START VISIBLE EVENTS FOR ALL USERS ####################################

# Get All visible events

@app.route('/events', methods=['GET'])
def get_events():

    
    events= Event.query.filter_by(visible=True).all()
    
    
    if not events:
        return jsonify({'message': 'No event found'})

    
    output=[]

    for event in events:
        event_data={}
        eventflyer= EventFlyer.query.filter_by(eventId=event.id).first()
        event_data['flyer']= eventflyer.flyerPath
        event_data['id']= event.id
        event_data['title']= event.title
        event_data['name']= event.name
        event_data['description']= event.description
        event_data['category']= event.category
        event_data['start_date']= event.start_date
        event_data['start_time']= event.start_time
        event_data['end_date']= event.end_date
        event_data['end_time']= event.end_time
        event_data['cost']= event.cost
        event_data['venue']= event.venue
        event_data['visible']= event.visible
        event_data['creator']= event.creator
        output.append(event_data)

    return jsonify({'event': output})

# search for visible events
# @app.route('/events/<event_id>', methods=['GET'])
# def search_one_event(event_id):

#     event= Event.query.filter_by(id=event_id, visible=True).first()

#     #When searching for an event we are ensuring that the admin has made that event public.
#     if not event.visible:
#         return jsonify({'message':' Admin has not yet made this event public to be seen'})

#     if not event:
#         return jsonify({'message': 'No event found'})

#     event_data={}
#     event_data['id']= event.id
#     event_data['title']= event.title
#     event_data['name']= event.name
#     event_data['description']= event.description
#     event_data['category']= event.category
#     event_data['start_date']= event.start_date
#     event_data['start_time']= event.start_time
#     event_data['end_date']= event.end_date
#     event_data['end_time']= event.end_time
#     event_data['cost']= event.cost
#     event_data['venue']= event.venue

#     event_data['visible']= event.visible
#     event_data['creator']= event.creator

#     return jsonify(event_data)


@app.route('/events/s=<event_name>', methods=['GET'])
def search_event(event_name):

    event= Event.query.filter_by(name=event_name, visible=True).first()

    output=[]
    if not event:
        return jsonify({'message': 'No event found'})

    event_data={}
    eventflyer= EventFlyer.query.filter_by(eventId=event.id).first()
    event_data['flyer']= eventflyer.flyerPath
    event_data['id']= event.id
    event_data['title']= event.title
    event_data['name']= event.name
    event_data['description']= event.description
    event_data['category']= event.category
    event_data['start_date']= event.start_date
    event_data['start_time']= event.start_time
    event_data['end_date']= event.end_date
    event_data['end_time']= event.end_time
    event_data['cost']= event.cost
    event_data['venue']= event.venue
   
    event_data['visible']= event.visible
    event_data['creator']= event.creator
    output.append(event_data)

    return jsonify({'event': output})

@app.route('/events/<event_id>', methods=['GET'])
def event(event_id):

    event= Event.query.filter_by(id=event_id, visible=True).first()


    if not event:
        return jsonify({'message': 'No event found'})

    event_data={}
    event_data['id']= event.id
    event_data['title']= event.title
    event_data['name']= event.name
    event_data['description']= event.description
    event_data['category']= event.category
    event_data['start_date']= event.start_date
    event_data['start_time']= event.start_time
    event_data['end_date']= event.end_date
    event_data['end_time']= event.end_time
    event_data['cost']= event.cost
    event_data['venue']= event.venue
   
    event_data['visible']= event.visible
    event_data['creator']= event.creator

    return jsonify({'event': event_data})


# Event details
@app.route('/events/details/<event_id>', methods=['GET'])
def event_details(event_id):

    event= Event.query.filter_by(id=event_id, visible=True).first()
    eventflyer= EventFlyer.query.filter_by(eventId=event_id).first()


    if not event:
        return jsonify({'message': 'No event found'})

    event_data={}
    event_data['flyer']= eventflyer.flyerPath
    event_data['id']= event.id
    event_data['title']= event.title
    event_data['name']= event.name
    event_data['description']= event.description
    event_data['category']= event.category
    event_data['start_date']= event.start_date
    event_data['start_time']= event.start_time
    event_data['end_date']= event.end_date
    event_data['end_time']= event.end_time
    event_data['cost']= event.cost
    event_data['venue']= event.venue
   
    event_data['visible']= event.visible
    event_data['creator']= event.creator

    return jsonify({'event': event_data})


# Edit to Update Event 
@app.route('/events/<public_name>',methods=['PUT'])

def edit_event(public_name):
    event = Event.query.filter_by(id=public_name).first()
    # eventflyer= EventFlyer.query.filter_by(eventId=public_name).first()
    
    if not event:
        return jsonify({'message':'No event found'})
      
    data = request.get_json()
   
    
    # event.id=event.id
    # event.public_name=event.public_name
    # event.creator=event.creator
    event.title = data['title']
    event.name= data['name']
    event.description = data['description']
    event.category=data['category']
    event.start_date =data['start_date']
    event.start_time =data['start_time']
    event.end_date = data['end_date']
    event.end_time =data['end_time']
    # eventflyer.flyerPath=data['flyer']
    event.cost = data['cost']
    event.venue=data['venue']
    # event.visible =data['visible']
   
   
    # data['title']=event.title
    # data['name']=event.name
    # data['description']=event.description
    # data['category']=event.category
    # data['start_time']=event.start_time
    # data['end_time']=event.end_time
    # data['start_date']=event.start_date
    # data['end_date']=event.end_date
    # data['cost']=event.cost
    # data['venue']=event.venue
    # data['visible']=event.visible


    # if data['name']!='':
    #     event.name= data['name']
    # else:
    #     event.name= event.name

    # if data['description']!='':
    #     event.description= data['description']
    # else:
    #     event.description= event.description

    # if data['category']!='':
    #     event.category=data['category']
    # else:
    #     event.category= event.category

    # if data['start_time']!='':
    #     event.start_time= data['start_time']
    # else:
    #     start_time= event.start_time

    # if data['end_time']!='':
    #     event.end_time= data['end_time']
    # else:
    #     event.end_time= event.end_time
    
    # if data['start_date']!='':
    #     event.start_date= data['start_date']
    # else:
    #     event.start_date= event.start_date

    # if data['end_date']!='':
    #     event.end_date= data['end_date']
    # else:
    #     event.end_date= event.end_date

    # if data['cost']!='':
    #     event.cost= data['cost']
    # else:
    #     event.cost= event.cost
        
    # if data['venue']!='':
    #     event.venue= data['venue']
    # else:
    #     event.venue= event.venue
        
    # if data['visible']!='':
    #     event.visible= data['visible']
    # else:
    #     event.visible= event.visible
   
    db.session.commit()
    
    return jsonify({'message':'The Event details was updated'})


#Question 6-Non-authenticated so we dont need the @token_required decorator
@app.route('/events/feedback/<event_id>', methods=['POST'])  
def comment_event(event_id):
    event= Event.query.filter_by(id=event_id).first()
    if not event:
		return jsonify({'message': 'No Event found!'})

    data = request.get_json()
    new_Feedback= Feedback(email=data['email'],rating=data['rating'],eventId=event.id, comment=data['comment'])
    db.session.add(new_Feedback) 
    db.session.commit()
    return jsonify({"message": "Feedback created!"})


# Get All feedback for particular event
@app.route('/events/feedback/<event_id>', methods=['GET'])
def get_feedback(event_id):

    feedbacks= Feedback.query.filter_by(eventId=event_id).all()

    if not feedbacks:
        return jsonify({'message': 'No Feedback found!'})

    output=[]

    for feedback in feedbacks:
        feedback_data={}
        feedback_data['id']=feedback.id
        feedback_data['email']= feedback.email
        feedback_data['rating']= feedback.rating
        feedback_data['eventId']= feedback.eventId
        feedback_data['comment']= feedback.comment
        output.append(feedback_data)

    return jsonify({'feedback': output})


# Get All visible events
@app.route('/events/feedback', methods=['GET'])
def get_comments():

    feedbacks= Feedback.query.all()

    if not feedbacks:
        return jsonify({'message': 'No Feedback found!'})

    output=[]

    for feedback in feedbacks:
        feedback_data={}
        feedback_data['id']=feedback.id
        feedback_data['email']= feedback.email
        feedback_data['rating']= feedback.rating
        feedback_data['eventId']= feedback.eventId
        feedback_data['comment']= feedback.comment
        output.append(feedback_data)

    return jsonify({'feedback': output})




#######################End VISIBLE EVENTS ####################################




#Note: The @token_required decorator ensures that the user is authenticated.

# Get all events for current user
@app.route('/event', methods=['GET'])
@token_required

def get_my_events(current_user):

    events= Event.query.filter_by(creator=current_user.id).all()

    output=[]

    for event in events:
        event_data={}
        event_data['id']= event.id
        event_data['title']= event.title
        event_data['name']= event.name
        event_data['description']= event.description
        event_data['category']= event.category
        event_data['start_date']= event.start_date
        event_data['start_time']= event.start_time
        event_data['end_date']= event.end_date
        event_data['end_time']= event.end_time
        event_data['cost']= event.cost
        event_data['venue']= event.venue
        event_data['visible']= event.visible
        event_data['creator']= event.creator
        output.append(event_data)

    return jsonify({'event': output})

# Current User search for an event
@app.route('/event/<event_id>', methods=['GET'])
@token_required
def get_one_event(current_user,event_id):

    event= Event.query.filter_by(id=event_id, creator=current_user.id).first()

    if not event:
        return jsonify({'message': 'No event found'})

    event_data={}
    event_data['id']= event.id
    event_data['title']= event.title
    event_data['name']= event.name
    event_data['description']= event.description
    event_data['category']= event.category
    event_data['start_date']= event.start_date
    event_data['start_time']= event.start_time
    event_data['end_date']= event.end_date
    event_data['end_time']= event.end_time
    event_data['cost']= event.cost
    event_data['venue']= event.venue

    event_data['visible']= event.visible
    event_data['creator']= event.creator

    return jsonify(event_data)

#Question6- Authenticated users can create an event
@app.route('/event',methods=['POST'])
#@token_required
def create_event():  
    data= request.get_json()




    new_event= Event(public_name=str(uuid.uuid4()),title=data['title'], name=data['name'], description=data['description'], category=data['category'], start_date=data['start_date'], end_date= data['end_date'], start_time=data['start_time'], end_time= data['end_time'],cost=data['cost'],venue=data['venue'],visible=False,creator=2)
    db.session.add(new_event) 
    db.session.commit()

    #print(data)

    return jsonify({"message": "Event created!"})


 #Question 4
 #Make event visible
@app.route('/event/<event_id>', methods=['PUT'])
@token_required
@admin_required
def set_visible(current_user, event_id): 
    event= Event.query.filter_by(id=event_id, creator=current_user.id).first()
    if not event:
        return jsonify({'message': 'No event found'})
    event.visible= True 
    db.session.commit()
    return jsonify({'message': 'Event has been set to visible!'})

# Current user delete an event
@app.route('/event/<event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
	event= Event.query.filter_by(id=event_id, user_id=current_user.id).first()

	if not event:
		return jsonify({'message': 'No Event found!'})

	db.session.delete(event)
	db.session.commit()

	return jsonify({'message': 'Event deleted!'})



@app.route('/event/<event_id>', methods=['POST'])
def rate_event(event_id):
	return ''


##   
#IMAGE UPLOAD
##

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
@app.route('/upload_flyer/<public_name>', methods=['PUT'])
def upload_file(public_name):
    event= Event.query.filter_by(public_name=public_name).first()
    if request.method == 'PUT':
        if 'file' not in request.files:
            return jsonify({'message':'No file part'})
        file =request.files['file']
        if allowed_file(file.filename):
            # event=Event.query.filter_by(public_name=public_name).first()
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # if name:
            eventimg=EventFlyer(public_name=public_name,eventId=event.id,flyerPath='assets/Flyers/' + filename)
            db.session.add(eventimg)
            db.session.commit()
            return jsonify({'message':'File upload successful'})


