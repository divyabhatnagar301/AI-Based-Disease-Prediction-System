"""
Test script for MediLedger API
Run this after starting the API server to test all endpoints
"""

import requests
import json

BASE_URL = "http://localhost:3000"

def test_signup():
    """Test user signup"""
    print("\n" + "="*60)
    print("Testing Signup...")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/api/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()['token']
    return None

def test_signin():
    """Test user signin"""
    print("\n" + "="*60)
    print("Testing Signin...")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/api/auth/signin", json={
        "username": "testuser",
        "password": "password123"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_diabetes_prediction(token):
    """Test diabetes prediction"""
    print("\n" + "="*60)
    print("Testing Diabetes Prediction...")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "gender": 0,
        "age": 45.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": 4,
        "bmi": 25.5,
        "HbA1c_level": 5.5,
        "blood_glucose_level": 100
    }
    
    response = requests.post(f"{BASE_URL}/api/predict/diabetes", 
                           headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_heart_prediction(token):
    """Test heart disease prediction"""
    print("\n" + "="*60)
    print("Testing Heart Disease Prediction...")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
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
    
    response = requests.post(f"{BASE_URL}/api/predict/heart", 
                           headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_kidney_prediction(token):
    """Test kidney disease prediction"""
    print("\n" + "="*60)
    print("Testing Kidney Disease Prediction...")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
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
    
    response = requests.post(f"{BASE_URL}/api/predict/kidney", 
                           headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_liver_prediction(token):
    """Test liver disease prediction"""
    print("\n" + "="*60)
    print("Testing Liver Disease Prediction...")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
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
    
    response = requests.post(f"{BASE_URL}/api/predict/liver", 
                           headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_predictions(token):
    """Test getting prediction history"""
    print("\n" + "="*60)
    print("Testing Get Predictions...")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/predictions", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_models_info():
    """Test getting models info"""
    print("\n" + "="*60)
    print("Testing Models Info...")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/models/info")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health_check():
    """Test health check"""
    print("\n" + "="*60)
    print("Testing Health Check...")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MediLedger API Test Suite")
    print("="*60)
    print("\nMake sure the API server is running on http://localhost:3000")
    
    # Test health check first
    if not test_health_check():
        print("\n❌ Health check failed! Make sure the API server is running.")
        return
    
    # Test signup
    token = test_signup()
    
    # If signup fails (user already exists), try signin
    if not token:
        print("\n⚠️  Signup failed, trying signin...")
        token = test_signin()
    
    if not token:
        print("\n❌ Authentication failed! Cannot proceed with tests.")
        return
    
    print(f"\n✅ Authentication successful! Token: {token[:20]}...")
    
    # Test all prediction endpoints
    test_diabetes_prediction(token)
    test_heart_prediction(token)
    test_kidney_prediction(token)
    test_liver_prediction(token)
    
    # Test prediction history
    test_get_predictions(token)
    
    # Test models info
    test_models_info()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Make sure the API server is running on http://localhost:3000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
