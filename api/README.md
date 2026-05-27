# MediLedger API - Healthcare Records with Multi-Disease Prediction

A Flask-based REST API for healthcare disease prediction with user authentication and prediction history tracking.

## Features

- 🔐 User Authentication (Signup/Signin)
- 🏥 Multi-Disease Prediction (Diabetes, Heart, Kidney, Liver)
- 📊 Prediction History Storage
- 🔒 JWT-based Authentication
- 💾 SQLite Database
- 📝 User Profile Management

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure all model files are in place:
   - `models/Diabetes/saved_models/diabetes_rf_model.pkl`
   - `models/heart/models/best_heart_disease_model.pkl`
   - `models/Kidney/saved_model/best_model.pkl`
   - `models/Liver/saved_models/best_model.pkl`

3. Run the API:
```bash
python app.py
```

The API will start on `http://localhost:3000`

## API Endpoints

### Authentication

#### Sign Up
```http
POST /api/auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

#### Sign In
```http
POST /api/auth/signin
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

### Disease Predictions

All prediction endpoints require authentication token in the Authorization header.

#### Diabetes Prediction
```http
POST /api/predict/diabetes
Authorization: Bearer <token>
Content-Type: application/json

{
  "gender": 0,
  "age": 45.0,
  "hypertension": 0,
  "heart_disease": 0,
  "smoking_history": 4,
  "bmi": 25.5,
  "HbA1c_level": 5.5,
  "blood_glucose_level": 100
}
```

**Feature Encoding:**
- `gender`: 0=Female, 1=Male, 2=Other
- `smoking_history`: 0=No Info, 1=current, 2=ever, 3=former, 4=never, 5=not current

#### Heart Disease Prediction
```http
POST /api/predict/heart
Authorization: Bearer <token>
Content-Type: application/json

{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

#### Kidney Disease Prediction
```http
POST /api/predict/kidney
Authorization: Bearer <token>
Content-Type: application/json

{
  "Age of the patient": 48,
  "Blood pressure (mm/Hg)": 80,
  "Specific gravity of urine": 1.02,
  "Albumin in urine": 0,
  "Sugar in urine": 0,
  "Random blood glucose level (mg/dl)": 121,
  "Blood urea (mg/dl)": 36,
  "Serum creatinine (mg/dl)": 1.2,
  "Sodium level (mEq/L)": 142,
  "Potassium level (mEq/L)": 4.5,
  "Hemoglobin level (gms)": 15.0,
  "Packed cell volume (%)": 44,
  "White blood cell count (cells/cumm)": 7800,
  "Red blood cell count (millions/cumm)": 5.2,
  "Estimated Glomerular Filtration Rate (eGFR)": 90,
  "Urine protein-to-creatinine ratio": 0.15,
  "Urine output (ml/day)": 1500,
  "Serum albumin level": 4.5,
  "Cholesterol level": 200,
  "Parathyroid hormone (PTH) level": 35,
  "Serum calcium level": 9.5,
  "Serum phosphate level": 3.5,
  "Body Mass Index (BMI)": 25,
  "Duration of diabetes mellitus (years)": 0,
  "Duration of hypertension (years)": 0,
  "Cystatin C level": 0.8,
  "C-reactive protein (CRP) level": 2.0,
  "Interleukin-6 (IL-6) level": 5.0,
  "Appetite": 1
}
```

#### Liver Disease Prediction
```http
POST /api/predict/liver
Authorization: Bearer <token>
Content-Type: application/json

{
  "Age of the patient": 65,
  "Gender of the patient": 1,
  "Total Bilirubin": 0.7,
  "Direct Bilirubin": 0.1,
  " Alkphos Alkaline Phosphotase": 187,
  " Sgpt Alamine Aminotransferase": 16,
  "Sgot Aspartate Aminotransferase": 18,
  "Total Protiens": 6.8,
  " ALB Albumin": 3.3,
  "A/G Ratio Albumin and Globulin Ratio": 0.9
}
```

**Feature Encoding:**
- `Gender of the patient`: 0=Female, 1=Male

### Prediction History

#### Get All Predictions
```http
GET /api/predictions?disease_type=diabetes&limit=50
Authorization: Bearer <token>
```

#### Get Specific Prediction
```http
GET /api/predictions/<prediction_id>
Authorization: Bearer <token>
```

### Model Information

#### Get All Models Info
```http
GET /api/models/info
```

#### Get Model Features
```http
GET /api/models/<disease_type>/features
```

### Health Check

```http
GET /api/health
```

## Response Format

### Success Response
```json
{
  "prediction": "No Diabetes",
  "probability": 0.95,
  "prediction_code": 0,
  "model_accuracy": 0.9686,
  "input_features": {...}
}
```

### Error Response
```json
{
  "error": "Error message here"
}
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `full_name`: User's full name
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Predictions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `disease_type`: Type of disease (diabetes, heart, kidney, liver)
- `input_data`: JSON string of input features
- `prediction_result`: Prediction result
- `prediction_probability`: Confidence score
- `created_at`: Timestamp

### Health Records Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `record_type`: Type of health record
- `record_data`: JSON string of record data
- `created_at`: Timestamp

## Security Notes

⚠️ **Important**: Change the `SECRET_KEY` in `app.py` before deploying to production!

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

## Example Usage with cURL

### Sign Up
```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Sign In
```bash
curl -X POST http://localhost:3000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Predict Diabetes
```bash
curl -X POST http://localhost:3000/api/predict/diabetes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{
    "gender": 0,
    "age": 45.0,
    "hypertension": 0,
    "heart_disease": 0,
    "smoking_history": 4,
    "bmi": 25.5,
    "HbA1c_level": 5.5,
    "blood_glucose_level": 100
  }'
```

## Troubleshooting

1. **Model not found errors**: Ensure all model files exist in the correct paths
2. **Database errors**: The database will be created automatically on first run
3. **Port already in use**: Change the port in `app.py` (default: 3000)
4. **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

## License

This project is part of the MediLedger Blockchain-based Healthcare Records system.
