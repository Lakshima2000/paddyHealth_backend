from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from flask_mail import Message
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    user = User(email=data['email'], username=data['username'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Try to send welcome email, but don't fail if it doesn't work
    try:
        msg = Message('Welcome to Rice Leaf Disease Detection',
                      sender=os.environ.get('MAIL_USERNAME'),
                      recipients=[user.email])
        msg.body = f'Welcome {user.username}! Thank you for registering with our service.'
        mail = current_app.extensions.get('mail') # Access mail from current_app.extensions
        if mail: # Ensure mail is initialized
            mail.send(msg)
        else:
            print("Mail extension not found in current_app.extensions. Email not sent.")
    except Exception as e:
        # Log the error but continue with registration
        print(f"Failed to send welcome email: {str(e)}")
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200 