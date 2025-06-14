import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import clip
from flask import Blueprint, request, jsonify, current_app
from models import db, Prediction
from auth import jwt_required, get_jwt_identity
from extensions import socketio

prediction_bp = Blueprint('prediction', __name__)

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

# Define disease classes and their cures
disease_cures = {
    'Bacterial Leaf Blight': 'No specific chemical cure available. Focus on resistant varieties, proper nutrient management, and drainage.',
    'Brown Spot': 'Hexaconazole 50g/L EC 160ml per acre',
    'Leaf Smut': 'Tebuconazole 250g/l EW 50ml per acre',
    'Leaf Blast': 'Tebuconazole 250g/l EW 50ml per acre',
    'Sheath Blight': 'Hexaconazole 50g/L EC 160ml per acre',
    'False Smut Disease': 'Consult local agricultural extension for specific recommendations.',
    'Healthy Rice Leaf': 'Maintain good agricultural practices.',
    'Leaf scald': 'Improve drainage and reduce nitrogen fertilization.'
}

disease_cures_si = {
    'Bacterial Leaf Blight': 'නිශ්චිත රසායනික ප්‍රතිකාරයක් නොමැත. ප්‍රතිරෝධී වර්ග, නිවැරදි පෝෂක කළමනාකරණය සහ ජල නිස්සාරණය මත අවධානය යොමු කරන්න.',
    'Brown Spot': 'Hexaconazole 50g/L EC 160ml අක්කරයකට',
    'Leaf Smut': 'Tebuconazole 250g/l EW 50ml අක්කරයකට',
    'Leaf Blast': 'Tebuconazole 250g/l EW 50ml අක්කරයකට',
    'Sheath Blight': 'Hexaconazole 50g/L EC 160ml අක්කරයකට',
    'False Smut Disease': 'විශේෂ නිර්දේශ සඳහා ප්‍රාදේශීය කෘෂි දිගුවෙන් උපදෙස් ලබා ගන්න.',
    'Healthy Rice Leaf': 'හොඳ කෘෂි ක්‍රමෝපායන් රැකීම වැදගත්ය.',
    'Leaf scald': 'ජල නිස්සාරණය වැඩිදියුණු කර නයිට්‍රජන් පොහොර අඩු කරන්න.'
}

disease_cures_ta = {
    'Bacterial Leaf Blight': 'குறிப்பிட்ட வேதியியல் சிகிச்சை கிடையாது. தடுப்பு வகைகள், சரியான ஊட்டச்சத்து மேலாண்மை மற்றும் வடிகால் பராமரிப்பை கவனிக்கவும்.',
    'Brown Spot': 'Hexaconazole 50g/L EC 160ml ஒரு ஏக்கருக்கு',
    'Leaf Smut': 'Tebuconazole 250g/l EW 50ml ஒரு ஏக்கருக்கு',
    'Leaf Blast': 'Tebuconazole 250g/l EW 50ml ஒரு ஏக்கருக்கு',
    'Sheath Blight': 'Hexaconazole 50g/L EC 160ml ஒரு ஏக்கருக்கு',
    'False Smut Disease': 'சிறப்பு பரிந்துரைகளுக்காக உள்ளூர் வேளாண் அலுவலகத்தை அணுகவும்.',
    'Healthy Rice Leaf': 'நல்ல வேளாண்மை பழக்கவழக்கங்களை பின்பற்றுங்கள்.',
    'Leaf scald': 'வடிகால்களை மேம்படுத்தவும், நைட்ரஜன் உரத்தின் அளவைக் குறைக்கவும்.'
}

# Disease classes for the CLIP model should be derived from the keys of disease_cures
disease_classes = list(disease_cures.keys())

def preprocess_image(image_path):
    """Preprocess the image for CLIP model"""
    image = Image.open(image_path).convert('RGB')
    image = preprocess(image).unsqueeze(0).to(device)
    return image

def _perform_prediction_async(app, file_path, user_id, session_id):
    # This function runs in a separate background task
    with app.app_context(): # Ensure application context for database operations
        try:
            # Preprocess the image
            image = preprocess_image(file_path)
            
            # Get image features
            with torch.no_grad():
                image_features = model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            
            # Get text features for each disease class using keys from disease_cures
            text_inputs = torch.cat([clip.tokenize(f"a photo of a rice leaf with {disease}") for disease in disease_classes]).to(device)
            with torch.no_grad():
                text_features = model.encode_text(text_inputs)
                text_features /= text_features.norm(dim=-1, keepdim=True)
            
            # Calculate similarity scores
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            values, indices = similarity[0].topk(1)
            
            # Get prediction and confidence
            predicted_class = disease_classes[indices[0].item()]
            confidence = values[0].item()
            
            # Get cure information for the predicted class
            cure_info = disease_cures.get(predicted_class, 'No specific cure information available for this disease.')
            cure_info_si = disease_cures_si.get(predicted_class, 'මෙම රෝගය සඳහා නිශ්චිත ප්‍රතිකාර තොරතුරු නොමැත.')
            cure_info_ta = disease_cures_ta.get(predicted_class, 'இந்த நோய்க்கு குறிப்பிட்ட சிகிச்சை தகவல் இல்லை.')

            # Save prediction to database (user_id will be None if not authenticated)
            prediction = Prediction(
                user_id=user_id,
                image_path=file_path,
                predicted_class=predicted_class,
                confidence=confidence
            )
            db.session.add(prediction)
            db.session.commit() 
            prediction_id = prediction.id

            response_data = {
                'prediction': predicted_class,
                'confidence': confidence,
                'prediction_id': prediction_id,
                'status': 'completed',
                'session_id': session_id,
                'cure': cure_info,
                'cure_si': cure_info_si,
                'cure_ta': cure_info_ta
            }

            print("==============================================")
            print(response_data)
            print("==============================================")

            # Emit results via WebSocket
            if session_id:
                socketio.emit('prediction_result', response_data, room=session_id)

        except Exception as e:
            error_message = {'error': str(e), 'status': 'failed'}
            if session_id:
                socketio.emit('prediction_result', error_message, room=session_id)
            print(f"Prediction failed: {e}")
        finally:
            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

@prediction_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    user_id = get_jwt_identity()

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Get session ID from request form data (should be part of FormData)
    session_id = request.form.get('session_id')
    if not session_id:
        return jsonify({'error': 'WebSocket session_id is required'}), 400

    # Save the uploaded file temporarily
    upload_folder = os.environ.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    
    print(f"DEBUG: Received file: {file.filename}")
    print(f"DEBUG: Saving file to: {file_path}")
    print(f"DEBUG: session_id from request: {session_id}")

    file.save(file_path)
    
    # Get the current Flask application instance
    app = current_app._get_current_object()

    try:
        # Start prediction in a background task
        socketio.start_background_task(_perform_prediction_async, app, file_path, user_id, session_id)
        
        return jsonify({
            'message': 'Prediction request accepted, results will be sent via WebSocket.',
            'status': 'processing',
            'session_id': session_id
        }), 202
    except Exception as e:
        # If an error occurs here, return a JSON error response
        print(f"Error starting background task or saving file: {e}")
        # Clean up the uploaded file if an error occurred before successful background task start
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        return jsonify({'error': str(e), 'status': 'failed'}), 500

@prediction_bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    """Get all predictions for the current user"""
    user_id = get_jwt_identity()
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'image_path': p.image_path,
        'predicted_class': p.predicted_class,
        'confidence': p.confidence,
        'created_at': p.created_at.isoformat()
    } for p in predictions])