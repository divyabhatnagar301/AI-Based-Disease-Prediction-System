"""
Quick fix script to regenerate the imputer with correct number of features (29)
This script processes the data the same way as the training script and saves a new imputer
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

# Dataset path
DATASET_PATH = 'kidney_disease_dataset.csv'
MODEL_DIR = 'saved_model'

print("="*50)
print("FIXING IMPUTER - Regenerating with 29 features")
print("="*50)

# Load dataset
print("\nLoading dataset...")
df = pd.read_csv(DATASET_PATH)

print(f"Dataset Shape: {df.shape}")

# Handle categorical variables (same as training script)
categorical_columns = ['Red blood cells in urine', 'Pus cells in urine', 'Pus cell clumps in urine', 
                      'Bacteria in urine', 'Hypertension (yes/no)', 'Diabetes mellitus (yes/no)', 
                      'Coronary artery disease (yes/no)', 'Appetite (good/poor)', 'Pedal edema (yes/no)', 
                      'Anemia (yes/no)', 'Family history of chronic kidney disease', 'Smoking status', 
                      'Physical activity level', 'Urinary sediment microscopy results']

# Convert yes/no to 1/0
binary_columns = ['Hypertension (yes/no)', 'Diabetes mellitus (yes/no)', 'Coronary artery disease (yes/no)', 
                  'Pedal edema (yes/no)', 'Anemia (yes/no)', 'Family history of chronic kidney disease', 
                  'Smoking status']

for col in binary_columns:
    if col in df.columns:
        df[col] = df[col].map({'yes': 1, 'no': 0})

# Convert other categorical variables
if 'Appetite (good/poor)' in df.columns:
    df['Appetite'] = df['Appetite (good/poor)'].map({'good': 1, 'poor': 0})

if 'Physical activity level' in df.columns:
    df['Physical activity level'] = df['Physical activity level'].map({'low': 0, 'moderate': 1, 'high': 2})

# Handle specific gravity and other categoricals
label_encoders = {}
for col in ['Red blood cells in urine', 'Pus cells in urine', 'Pus cell clumps in urine', 
            'Bacteria in urine', 'Urinary sediment microscopy results']:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# Handle missing values on all numeric columns first
print("\nImputing missing values on all numeric columns...")
numeric_columns = df.select_dtypes(include=[np.number]).columns
imputer_all = SimpleImputer(strategy='median')
df[numeric_columns] = imputer_all.fit_transform(df[numeric_columns])

# Prepare features (drop target and categorical columns)
X = df.drop('Target', axis=1)
columns_to_drop = ['Appetite (good/poor)'] + categorical_columns
X = X.drop([col for col in columns_to_drop if col in X.columns], axis=1)

print(f"\nFinal features shape: {X.shape}")
print(f"Number of features: {len(X.columns)}")

# Create and fit imputer on the final feature set (29 features)
print("\nCreating new imputer with 29 features...")
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

print(f"Imputer fitted successfully!")
print(f"Imputer expects {imputer.n_features_in_} features")

# Save the new imputer
os.makedirs(MODEL_DIR, exist_ok=True)
imputer_path = os.path.join(MODEL_DIR, 'imputer.pkl')
joblib.dump(imputer, imputer_path)
print(f"\n[SUCCESS] Saved new imputer to: {imputer_path}")
print(f"[SUCCESS] Imputer now expects {imputer.n_features_in_} features (matches model)")

print("\n" + "="*50)
print("IMPUTER FIXED SUCCESSFULLY!")
print("="*50)
