# Quick Start Guide - MediLedger API

## Prerequisites
- Python 3.8 or higher
- All model files in place (they should already be in the models/ directory)

## Installation & Setup

### Option 1: Using Startup Scripts (Recommended)

**Windows:**
```bash
cd api
start_api.bat
```

**Linux/Mac:**
```bash
cd api
chmod +x start_api.sh
./start_api.sh
```

### Option 2: Manual Setup

1. **Navigate to API directory:**
```bash
cd api
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start the server:**
```bash
python app.py
```

The API will start on `http://localhost:3000`

## Quick Test

After starting the server, you can test it:

1. **Health Check:**
```bash
curl http://localhost:3000/api/health
```

2. **Run Test Suite:**
```bash
python test_api.py
```

## API Endpoints Summary

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `GET /api/auth/profile` - Get user profile (requires auth)

### Predictions
- `POST /api/predict/diabetes` - Predict diabetes (requires auth)
- `POST /api/predict/heart` - Predict heart disease (requires auth)
- `POST /api/predict/kidney` - Predict kidney disease (requires auth)
- `POST /api/predict/liver` - Predict liver disease (requires auth)

### History
- `GET /api/predictions` - Get prediction history (requires auth)
- `GET /api/predictions/<id>` - Get specific prediction (requires auth)

### Information
- `GET /api/models/info` - Get all models information
- `GET /api/models/<disease_type>/features` - Get model features
- `GET /api/health` - Health check

## Example: Complete Workflow

1. **Sign Up:**
```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123","full_name":"Test User"}'
```

2. **Sign In (get token):**
```bash
curl -X POST http://localhost:3000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

3. **Make Prediction (use token from step 2):**
```bash
curl -X POST http://localhost:3000/api/predict/diabetes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"gender":0,"age":45.0,"hypertension":0,"heart_disease":0,"smoking_history":4,"bmi":25.5,"HbA1c_level":5.5,"blood_glucose_level":100}'
```

4. **View Predictions:**
```bash
curl http://localhost:3000/api/predictions \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Troubleshooting

### Port Already in Use
If port 3000 is already in use, edit `app.py` and change:
```python
app.run(host='0.0.0.0', port=3000, debug=True)
```
to use a different port (e.g., 3001, 3002, etc.)

### Models Not Found
Make sure you're running the API from the project root or that the model paths are correct. The API expects models to be in:
- `models/Diabetes/saved_models/`
- `models/heart/models/`
- `models/Kidney/saved_model/`
- `models/Liver/saved_models/`

### Database Issues
The database (`mediledger.db`) will be created automatically on first run. If you need to reset it, just delete the file and restart the server.

## Next Steps

- Integrate with your frontend application
- Add more features as needed
- Deploy to production (remember to change SECRET_KEY!)
