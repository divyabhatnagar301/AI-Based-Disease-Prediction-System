"""
MediLedger API - Healthcare Records with Multi-Disease Prediction
Flask API with SQLite database for user management and disease predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import os
import json
import pickle
import joblib
import numpy as np
from functools import wraps
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # Change this in production!
CORS(app)  # Enable CORS for frontend integration

# Database file path (relative to api directory)
DB_PATH = Path(__file__).parent / 'mediledger.db'

# Model paths (relative to project root)
BASE_DIR = Path(__file__).parent.parent  # Go up from api/ to project root
MODEL_PATHS = {
    'diabetes': {
        'model': BASE_DIR / 'models' / 'Diabetes' / 'saved_models' / 'diabetes_rf_model.pkl',
        'metadata': BASE_DIR / 'models' / 'Diabetes' / 'saved_models' / 'diabetes_model_metadata.json'
    },
    'heart': {
        'model': BASE_DIR / 'models' / 'heart' / 'models' / 'best_heart_disease_model.pkl',
        'metadata': BASE_DIR / 'models' / 'heart' / 'models' / 'model_metadata.json'
    },
    'kidney': {
        'model': BASE_DIR / 'models' / 'Kidney' / 'saved_model' / 'best_model.pkl',
        'metadata': BASE_DIR / 'models' / 'Kidney' / 'saved_model' / 'model_metadata.json',
        'scaler': BASE_DIR / 'models' / 'Kidney' / 'saved_model' / 'scaler.pkl',
        'imputer': BASE_DIR / 'models' / 'Kidney' / 'saved_model' / 'imputer.pkl',
        'encoders': BASE_DIR / 'models' / 'Kidney' / 'saved_model' / 'label_encoders.pkl'
    },
    'liver': {
        'model': BASE_DIR / 'models' / 'Liver' / 'saved_models' / 'best_model.pkl',
        'metadata': BASE_DIR / 'models' / 'Liver' / 'saved_models' / 'model_metadata.json'
    },
    'heart_ecg': {
        'model': BASE_DIR / 'models' / 'heart-ecg' / 'saved_model' / 'lstm_heartbeat.keras',
        'metadata': BASE_DIR / 'models' / 'heart-ecg' / 'saved_model' / 'model_metadata.json'
    }
}

# Global variables to store loaded models
loaded_models = {}
model_metadata = {}


def patch_sklearn_imputer(imputer):
    """SimpleImputer pickles from sklearn < 1.8 lack _fill_dtype required at transform."""
    if imputer is not None and not hasattr(imputer, '_fill_dtype'):
        imputer._fill_dtype = np.dtype(np.float64)
    return imputer


def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            disease_type TEXT NOT NULL,
            input_data TEXT NOT NULL,
            prediction_result TEXT NOT NULL,
            prediction_probability REAL,
            saved_to_blockchain INTEGER DEFAULT 0,
            blockchain_tx_hash TEXT,
            blockchain_timestamp TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add columns to existing predictions table if they don't exist
    try:
        cursor.execute('ALTER TABLE predictions ADD COLUMN saved_to_blockchain INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE predictions ADD COLUMN blockchain_tx_hash TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute('ALTER TABLE predictions ADD COLUMN blockchain_timestamp TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # User health records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_type TEXT NOT NULL,
            record_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def load_models():
    """Load all disease prediction models"""
    global loaded_models, model_metadata
    
    print("Loading models...")
    
    # Load Diabetes model
    try:
        with open(str(MODEL_PATHS['diabetes']['model']), 'rb') as f:
            loaded_models['diabetes'] = pickle.load(f)
        with open(str(MODEL_PATHS['diabetes']['metadata']), 'r') as f:
            model_metadata['diabetes'] = json.load(f)
        print("✓ Diabetes model loaded")
    except Exception as e:
        print(f"✗ Error loading Diabetes model: {e}")
    
    # Load Heart model
    try:
        with open(str(MODEL_PATHS['heart']['model']), 'rb') as f:
            loaded_models['heart'] = joblib.load(f)
        with open(str(MODEL_PATHS['heart']['metadata']), 'r') as f:
            model_metadata['heart'] = json.load(f)
        print("✓ Heart model loaded")
    except Exception as e:
        print(f"✗ Error loading Heart model: {e}")
    
    # Load Kidney model
    try:
        with open(str(MODEL_PATHS['kidney']['model']), 'rb') as f:
            loaded_models['kidney'] = joblib.load(f)
        with open(str(MODEL_PATHS['kidney']['metadata']), 'r') as f:
            model_metadata['kidney'] = json.load(f)
        
        # Load preprocessing components
        with open(str(MODEL_PATHS['kidney']['scaler']), 'rb') as f:
            loaded_models['kidney_scaler'] = joblib.load(f)
        with open(str(MODEL_PATHS['kidney']['imputer']), 'rb') as f:
            loaded_models['kidney_imputer'] = patch_sklearn_imputer(joblib.load(f))
        with open(str(MODEL_PATHS['kidney']['encoders']), 'rb') as f:
            loaded_models['kidney_encoders'] = joblib.load(f)
        print("✓ Kidney model loaded")
    except Exception as e:
        print(f"✗ Error loading Kidney model: {e}")
    
    # Load Liver model
    try:
        with open(str(MODEL_PATHS['liver']['model']), 'rb') as f:
            loaded_models['liver'] = pickle.load(f)
        with open(str(MODEL_PATHS['liver']['metadata']), 'r') as f:
            model_metadata['liver'] = json.load(f)
        print("✓ Liver model loaded")
    except Exception as e:
        print(f"✗ Error loading Liver model: {e}")
    
    # Load Heart ECG (LSTM) model
    try:
        import tensorflow as tf
        model_path = MODEL_PATHS['heart_ecg']['model']
        if model_path.exists():
            loaded_models['heart_ecg'] = tf.keras.models.load_model(str(model_path))
            with open(str(MODEL_PATHS['heart_ecg']['metadata']), 'r') as f:
                model_metadata['heart_ecg'] = json.load(f)
            print("✓ Heart ECG model loaded")
        else:
            print(f"✗ Heart ECG model file not found: {model_path}")
    except Exception as e:
        print(f"✗ Error loading Heart ECG model: {e}")
    
    print("Model loading completed!")


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(user_id, username):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_username = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user_id, current_username, *args, **kwargs)
    
    return decorated


# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Username or email already exists'}), 400
        
        # Create new user
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Generate token
        token = generate_token(user_id, username)
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/signin', methods=['POST'])
def signin():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute('''
            SELECT id, username, email, full_name FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        user_id, username, email, full_name = user
        
        # Generate token
        token = generate_token(user_id, username)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile(user_id, username):
    """Get user profile"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, full_name, created_at
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'created_at': user[4]
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PREDICTION ENDPOINTS ====================

@app.route('/api/predict/diabetes', methods=['POST'])
@token_required
def predict_diabetes(user_id, username):
    """Diabetes prediction endpoint"""
    try:
        if 'diabetes' not in loaded_models:
            return jsonify({'error': 'Diabetes model not loaded'}), 500
        
        data = request.get_json()
        metadata = model_metadata['diabetes']
        
        # Extract and validate features
        features = []
        feature_names = metadata['feature_names']
        
        for feature in feature_names:
            value = data.get(feature)
            if value is None:
                return jsonify({'error': f'Missing required feature: {feature}'}), 400
            features.append(float(value))
        
        # Make prediction
        model = loaded_models['diabetes']
        features_array = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Get prediction label
        prediction_label = metadata['prediction_classes'][str(int(prediction))]
        probability_value = float(max(probability))
        
        # Save prediction to database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, disease_type, input_data, prediction_result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'diabetes', json.dumps(data), prediction_label, probability_value))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction_label,
            'probability': probability_value,
            'prediction_code': int(prediction),
            'model_accuracy': metadata['model_metrics']['accuracy'],
            'input_features': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/heart', methods=['POST'])
@token_required
def predict_heart(user_id, username):
    """Heart disease prediction endpoint"""
    try:
        if 'heart' not in loaded_models:
            return jsonify({'error': 'Heart model not loaded'}), 500
        
        data = request.get_json()
        metadata = model_metadata['heart']
        
        # Extract and validate features
        features = []
        feature_names = metadata['feature_names']
        
        for feature in feature_names:
            value = data.get(feature)
            if value is None:
                return jsonify({'error': f'Missing required feature: {feature}'}), 400
            features.append(float(value))
        
        # Make prediction
        model = loaded_models['heart']
        features_array = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Get prediction label
        prediction_label = 'Heart Disease' if prediction == 1 else 'No Heart Disease'
        probability_value = float(max(probability))
        
        # Save prediction to database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, disease_type, input_data, prediction_result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'heart', json.dumps(data), prediction_label, probability_value))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction_label,
            'probability': probability_value,
            'prediction_code': int(prediction),
            'model_accuracy': metadata['accuracy'],
            'input_features': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/kidney', methods=['POST'])
@token_required
def predict_kidney(user_id, username):
    """Kidney disease prediction endpoint"""
    try:
        if 'kidney' not in loaded_models:
            return jsonify({'error': 'Kidney model not loaded'}), 500
        
        data = request.get_json()
        metadata = model_metadata['kidney']
        
        # Extract and validate features
        features = []
        feature_names = metadata['feature_names']
        
        for feature in feature_names:
            value = data.get(feature)
            if value is None:
                return jsonify({'error': f'Missing required feature: {feature}'}), 400
            features.append(float(value))
        
        # Preprocess features (impute, scale)
        features_array = np.array(features).reshape(1, -1)
        features_array = loaded_models['kidney_imputer'].transform(features_array)
        
        if metadata['use_scaled_features']:
            features_array = loaded_models['kidney_scaler'].transform(features_array)
        
        # Make prediction
        model = loaded_models['kidney']
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Get prediction label - handle both string and integer predictions
        target_classes = metadata['target_classes']
        if isinstance(prediction, (str, np.str_)):
            # Model returned a string label directly
            prediction_label = str(prediction)
            # Find the index for prediction_code
            try:
                prediction_code = target_classes.index(prediction_label)
            except ValueError:
                prediction_code = -1
        else:
            # Model returned an integer index
            prediction_code = int(prediction)
            if prediction_code < len(target_classes):
                prediction_label = target_classes[prediction_code]
            else:
                prediction_label = 'Unknown'
        
        probability_value = float(max(probability))
        
        # Save prediction to database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, disease_type, input_data, prediction_result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'kidney', json.dumps(data), prediction_label, probability_value))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction_label,
            'probability': probability_value,
            'prediction_code': prediction_code,
            'model_accuracy': metadata['accuracy'],
            'input_features': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/liver', methods=['POST'])
@token_required
def predict_liver(user_id, username):
    """Liver disease prediction endpoint"""
    try:
        if 'liver' not in loaded_models:
            return jsonify({'error': 'Liver model not loaded'}), 500
        
        data = request.get_json()
        metadata = model_metadata['liver']
        
        # Extract and validate features
        features = []
        feature_names = metadata['feature_names']
        
        for feature in feature_names:
            value = data.get(feature)
            if value is None:
                return jsonify({'error': f'Missing required feature: {feature}'}), 400
            features.append(float(value))
        
        # Make prediction
        model = loaded_models['liver']
        features_array = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Get prediction label
        prediction_mapping = metadata['prediction_mapping']
        prediction_label = prediction_mapping[str(int(prediction))]
        probability_value = float(max(probability))
        
        # Save prediction to database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, disease_type, input_data, prediction_result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'liver', json.dumps(data), prediction_label, probability_value))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction_label,
            'probability': probability_value,
            'prediction_code': int(prediction),
            'model_accuracy': metadata['accuracy'],
            'input_features': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/heart-ecg', methods=['POST'])
@token_required
def predict_heart_ecg(user_id, username):
    """Heartbeat (ECG) classification endpoint - expects 187-sample ECG segment"""
    try:
        if 'heart_ecg' not in loaded_models:
            return jsonify({'error': 'Heart ECG model not loaded'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON with ecg_signal array'}), 400
        
        ecg_signal = data.get('ecg_signal')
        if ecg_signal is None:
            return jsonify({'error': 'Missing required field: ecg_signal (array of 187 floats)'}), 400
        
        try:
            ecg_arr = np.array(ecg_signal, dtype=np.float64)
        except (TypeError, ValueError):
            return jsonify({'error': 'ecg_signal must be an array of numbers'}), 400
        
        metadata = model_metadata['heart_ecg']
        required_len = metadata.get('sequence_length', 187)
        if len(ecg_arr) != required_len:
            return jsonify({
                'error': f'ecg_signal must have exactly {required_len} samples, got {len(ecg_arr)}'
            }), 400
        
        # Reshape to (1, 187, 1) for LSTM
        X = ecg_arr.reshape(1, required_len, 1)
        
        model = loaded_models['heart_ecg']
        proba = model.predict(X, verbose=0)[0]
        class_idx = int(np.argmax(proba))
        probability_value = float(proba[class_idx])
        class_names = metadata.get('class_names', [])
        prediction_label = class_names[class_idx] if class_idx < len(class_names) else f'Class_{class_idx}'
        
        # Save prediction to database (store summary to avoid huge input_data)
        input_summary = {'length': required_len, 'sample_preview': ecg_signal[:10]}
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, disease_type, input_data, prediction_result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'heart_ecg', json.dumps(input_summary), prediction_label, probability_value))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': prediction_label,
            'probability': probability_value,
            'prediction_code': class_idx,
            'class_names': class_names,
            'probabilities': [float(p) for p in proba],
            'model_accuracy': metadata.get('accuracy'),
            'sequence_length': required_len
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PREDICTION HISTORY ENDPOINTS ====================

@app.route('/api/predictions', methods=['GET'])
@token_required
def get_predictions(user_id, username):
    """Get user's prediction history"""
    try:
        disease_type = request.args.get('disease_type')  # Optional filter
        limit = request.args.get('limit', 50, type=int)
        
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        if disease_type:
            cursor.execute('''
                SELECT id, disease_type, input_data, prediction_result, prediction_probability, 
                       created_at, saved_to_blockchain, blockchain_tx_hash, blockchain_timestamp
                FROM predictions
                WHERE user_id = ? AND disease_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, disease_type, limit))
        else:
            cursor.execute('''
                SELECT id, disease_type, input_data, prediction_result, prediction_probability, 
                       created_at, saved_to_blockchain, blockchain_tx_hash, blockchain_timestamp
                FROM predictions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        
        predictions = cursor.fetchall()
        conn.close()
        
        result = []
        for pred in predictions:
            result.append({
                'id': pred[0],
                'disease_type': pred[1],
                'input_data': json.loads(pred[2]),
                'prediction_result': pred[3],
                'prediction_probability': pred[4],
                'created_at': pred[5],
                'saved_to_blockchain': bool(pred[6]),
                'blockchain_tx_hash': pred[7],
                'blockchain_timestamp': pred[8]
            })
        
        return jsonify({
            'predictions': result,
            'count': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/<int:prediction_id>', methods=['GET'])
@token_required
def get_prediction(user_id, username, prediction_id):
    """Get a specific prediction by ID"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, disease_type, input_data, prediction_result, prediction_probability, 
                   created_at, saved_to_blockchain, blockchain_tx_hash, blockchain_timestamp
            FROM predictions
            WHERE id = ? AND user_id = ?
        ''', (prediction_id, user_id))
        
        pred = cursor.fetchone()
        conn.close()
        
        if not pred:
            return jsonify({'error': 'Prediction not found'}), 404
        
        return jsonify({
            'id': pred[0],
            'disease_type': pred[1],
            'input_data': json.loads(pred[2]),
            'prediction_result': pred[3],
            'prediction_probability': pred[4],
            'created_at': pred[5],
            'saved_to_blockchain': bool(pred[6]),
            'blockchain_tx_hash': pred[7],
            'blockchain_timestamp': pred[8]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== BLOCKCHAIN ENDPOINTS ====================

@app.route('/api/predictions/<int:prediction_id>/save-to-blockchain', methods=['POST'])
@token_required
def save_to_blockchain(user_id, username, prediction_id):
    """Mark a prediction as saved to blockchain with transaction hash"""
    try:
        data = request.get_json()
        tx_hash = data.get('tx_hash')
        
        if not tx_hash:
            return jsonify({'error': 'Transaction hash is required'}), 400
        
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check if prediction exists and belongs to user
        cursor.execute('''
            SELECT id, saved_to_blockchain FROM predictions
            WHERE id = ? AND user_id = ?
        ''', (prediction_id, user_id))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'Prediction not found'}), 404
        
        if result[1]:  # Already saved to blockchain
            conn.close()
            return jsonify({'error': 'Record already saved to blockchain'}), 400
        
        # Update prediction with blockchain info
        cursor.execute('''
            UPDATE predictions
            SET saved_to_blockchain = 1,
                blockchain_tx_hash = ?,
                blockchain_timestamp = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (tx_hash, prediction_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Record successfully saved to blockchain',
            'prediction_id': prediction_id,
            'tx_hash': tx_hash
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/<int:prediction_id>', methods=['PUT'])
@token_required
def update_prediction(user_id, username, prediction_id):
    """Update a prediction (only if not saved to blockchain)"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check if prediction exists and is saved to blockchain
        cursor.execute('''
            SELECT saved_to_blockchain FROM predictions
            WHERE id = ? AND user_id = ?
        ''', (prediction_id, user_id))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'Prediction not found'}), 404
        
        if result[0]:  # Saved to blockchain
            conn.close()
            return jsonify({
                'error': 'Cannot edit: Record is immutably stored on blockchain'
            }), 403
        
        # Allow update (implement update logic here if needed)
        conn.close()
        
        return jsonify({
            'message': 'Update allowed (implement update logic as needed)'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/<int:prediction_id>', methods=['DELETE'])
@token_required
def delete_prediction(user_id, username, prediction_id):
    """Delete a prediction (only if not saved to blockchain)"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check if prediction exists and is saved to blockchain
        cursor.execute('''
            SELECT saved_to_blockchain FROM predictions
            WHERE id = ? AND user_id = ?
        ''', (prediction_id, user_id))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'Prediction not found'}), 404
        
        if result[0]:  # Saved to blockchain
            conn.close()
            return jsonify({
                'error': 'Cannot delete: Record is immutably stored on blockchain'
            }), 403
        
        # Delete the prediction
        cursor.execute('DELETE FROM predictions WHERE id = ? AND user_id = ?', 
                      (prediction_id, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Prediction deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== MODEL INFO ENDPOINTS ====================

@app.route('/api/models/info', methods=['GET'])
def get_models_info():
    """Get information about all available models"""
    try:
        info = {}
        
        for disease_type in ['diabetes', 'heart', 'kidney', 'liver', 'heart_ecg']:
            if disease_type in model_metadata:
                metadata = model_metadata[disease_type]
                feature_names = metadata.get('feature_names', [])
                if disease_type == 'heart_ecg':
                    feature_count = metadata.get('sequence_length', 187)
                else:
                    feature_count = len(feature_names)
                info[disease_type] = {
                    'model_name': metadata.get('model_name', metadata.get('model_type', 'Unknown')),
                    'accuracy': metadata.get('accuracy', metadata.get('model_metrics', {}).get('accuracy', 0)),
                    'feature_names': feature_names if feature_names else [],
                    'feature_count': feature_count,
                    'loaded': disease_type in loaded_models
                }
        
        return jsonify({'models': info}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/models/<disease_type>/features', methods=['GET'])
def get_model_features(disease_type):
    """Get required features for a specific model"""
    try:
        if disease_type not in model_metadata:
            return jsonify({'error': 'Model not found'}), 404
        
        metadata = model_metadata[disease_type]
        
        if disease_type == 'heart_ecg':
            return jsonify({
                'disease_type': disease_type,
                'input_type': 'ecg_sequence',
                'sequence_length': metadata.get('sequence_length', 187),
                'class_names': metadata.get('class_names', []),
                'feature_names': [],
                'feature_descriptions': {},
                'model_accuracy': metadata.get('accuracy', 0)
            }), 200
        
        return jsonify({
            'disease_type': disease_type,
            'feature_names': metadata.get('feature_names', []),
            'feature_descriptions': metadata.get('input_features_description', metadata.get('feature_descriptions', {})),
            'model_accuracy': metadata.get('accuracy', metadata.get('model_metrics', {}).get('accuracy', 0))
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    models_status = {}
    for disease_type in ['diabetes', 'heart', 'kidney', 'liver', 'heart_ecg']:
        models_status[disease_type] = disease_type in loaded_models
    
    return jsonify({
        'status': 'healthy',
        'models_loaded': models_status,
        'database': 'connected' if DB_PATH.exists() else 'not_found'
    }), 200


# ==================== MAIN ====================

if __name__ == '__main__':
    print("="*60)
    print("MediLedger API - Starting...")
    print("="*60)
    
    # Initialize database
    init_db()
    
    # Load models
    load_models()
    
    # Run Flask app
    print("\n" + "="*60)
    port = int(os.environ.get("PORT", 5001))
    print(f"API Server starting on http://localhost:{port}")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  POST   /api/auth/signup")
    print("  POST   /api/auth/signin")
    print("  GET    /api/auth/profile")
    print("  POST   /api/predict/diabetes")
    print("  POST   /api/predict/heart")
    print("  POST   /api/predict/kidney")
    print("  POST   /api/predict/liver")
    print("  POST   /api/predict/heart-ecg")
    print("  GET    /api/predictions")
    print("  GET    /api/predictions/<id>")
    print("  POST   /api/predictions/<id>/save-to-blockchain")
    print("  PUT    /api/predictions/<id>")
    print("  DELETE /api/predictions/<id>")
    print("  GET    /api/models/info")
    print("  GET    /api/models/<disease_type>/features")
    print("  GET    /api/health")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
