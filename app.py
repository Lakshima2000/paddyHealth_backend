import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from models import db as db_instance # Import db as db_instance to avoid naming conflict
from config import Config
import os
from extensions import socketio
from flask_socketio import join_room

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    jwt = JWTManager(app)
    db_instance.init_app(app)
    mail = Mail(app)
    
    # Initialize SocketIO with eventlet
    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     async_mode='eventlet',
                     logger=True,
                     engineio_logger=True)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from auth import auth_bp
    from prediction import prediction_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(prediction_bp, url_prefix='/api/predictions')

    with app.app_context():
        db_instance.create_all()

    return app, socketio # Return both app and socketio

# Add the join handler outside of create_app
@socketio.on('join')
def handle_join(data):
    session_id = data.get('sessionId')
    if session_id:
        join_room(session_id)
        print(f"[SocketIO] Client joined room: {session_id}")
    else:
        print("[SocketIO] No sessionId provided in join event")

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, 
                host='0.0.0.0', 
                port=5001, 
                debug=True, 
                allow_unsafe_werkzeug=True)