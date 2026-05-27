# Diabetes Prediction Model - Python Script
# Converted from Jupyter Notebook

# Importing Python Packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import pickle
import json
import warnings
warnings.filterwarnings("ignore")

# Import ML libraries
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, RobustScaler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

# Create results directory for saving charts
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

# Reading dataset - Updated to use local path
dataset_path = "diabetes_prediction_dataset.csv"
df = pd.read_csv(dataset_path, sep=',')

print("Dataset loaded successfully!")
print(f"Dataset shape: {df.shape}")

# Displaying the dataset
print("\nFirst few rows:")
print(df.head())

# What columns does the dataset
print("\nColumns:", df.columns.tolist())

# Check Instance and Features
print(f"\nDataset shape: {df.shape}")

# Displaying the number of duplicate rows
print(f"\nNumber of duplicate rows before removal: {df.duplicated().sum()}")

# Correlation
numeric_columns = df.select_dtypes(include='number').columns
correlation_matrix = df[numeric_columns].corr()

# Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'correlation_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: correlation_heatmap.png")

# Distribution of Diabetes
plt.figure(figsize=(7, 5))
sns.countplot(x='diabetes', hue='diabetes', data=df, palette='viridis')
plt.title('Distribution of diabetes')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'diabetes_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: diabetes_distribution.png")

# Diabetes or Not Diabetes
diabetes_count = df['diabetes'].value_counts()[1]
not_diabetes_count = df['diabetes'].value_counts()[0]
sizes = [diabetes_count, not_diabetes_count]
labels = ['Diabetes', 'Not Diabetes']
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(sizes, labels=labels, shadow=True, autopct='%1.2f%%')
ax.legend()
ax.set_title("Diabetes VS Not Diabetes", size=15)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'diabetes_pie_chart.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: diabetes_pie_chart.png")

# Age Distribution
plt.figure(figsize=(7, 5))
sns.histplot(df['age'], bins=30, kde=True, color='skyblue')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'age_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: age_distribution.png")

# Age Distribution of Diabetes Patient
plt.figure(figsize=(7, 5))
sns.histplot(data=df, x='age', hue='diabetes', multiple='stack', bins=20)
plt.title('Age Distribution of Diabetes Patient')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'age_distribution_by_diabetes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: age_distribution_by_diabetes.png")

# Diabetes Rate depend of Smoking History
plt.figure(figsize=(7, 5))
sns.countplot(x='smoking_history', hue='diabetes', data=df)
plt.title('Diabetes Rate among Smoker')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'smoking_history_diabetes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: smoking_history_diabetes.png")

# Gender Distribution
counts = df['gender'].value_counts()
ax = sns.countplot(x='gender', data=df, hue='gender', palette='pastel')
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, 
            p.get_height() + 0.1, 
            int(p.get_height()), 
            ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'gender_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: gender_distribution.png")

# Gender-based Diabetes Analysis
plt.figure(figsize=(7, 5))
ax = sns.countplot(x='gender', hue='diabetes', data=df, palette='pastel')
plt.title('Gender-based Diabetes Analysis')
plt.xlabel('Gender')
plt.ylabel('Count')
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', padding=3)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'gender_diabetes_analysis.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: gender_diabetes_analysis.png")

# Gender based Age Comparison
plt.figure(figsize=(7, 5))
sns.boxplot(x='gender', y='age', data=df)
plt.title('Gender based Age Comparison')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'gender_age_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: gender_age_comparison.png")

# BMI Distribution by Diabetes
plt.figure(figsize=(7, 5))
sns.kdeplot(x='bmi', data=df, hue='diabetes', fill=True, common_norm=False, palette='Set2')
plt.title('BMI Distribution by Diabetes')
plt.xlabel('BMI')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'bmi_distribution_by_diabetes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: bmi_distribution_by_diabetes.png")

# Blood Glucose Level by Diabetes
plt.figure(figsize=(7, 5))
sns.barplot(x='diabetes', y='blood_glucose_level', hue="diabetes", data=df, palette='coolwarm')
plt.title('Blood Glucose Level by Diabetes')
plt.xlabel('Diabetes')
plt.ylabel('Blood Glucose Level')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'blood_glucose_level_by_diabetes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: blood_glucose_level_by_diabetes.png")

# HbA1c level Distribution by Diabetes
plt.figure(figsize=(7, 5))
sns.kdeplot(x='HbA1c_level', data=df, hue='diabetes', fill=True, common_norm=False, palette='Set2')
plt.title('HbA1c_level Distribution by Diabetes')
plt.xlabel('HbA1c_level')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'hba1c_level_distribution_by_diabetes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: hba1c_level_distribution_by_diabetes.png")

# Information about the DataFrame
print("\nDataset Info:")
print(df.info())

# Displaying the number of duplicate rows before removal
print(f"\nNumber of duplicate rows before removal: {df.duplicated().sum()}")

# Remove duplicates
droped_dup_df = df.drop_duplicates()
# Display the number of duplicate rows after removal
print(f"Number of duplicate rows after removal: {droped_dup_df.duplicated().sum()}")

# Duplicates deleted dateset droped_dup_df
print(f"\nDataset shape after removing duplicates: {droped_dup_df.shape}")

# Original Dataset df
print(f"Original dataset shape: {df.shape}")

# Count unique values for each column
unique_counts = droped_dup_df.nunique()
print("\nCount of Unique Values for Each Column:")
print(unique_counts)

# Checking NA or NaN or Null values
print("\nMissing values:")
print(droped_dup_df.isna().sum())

# Label encoding function
def encode_columns(df_cleaned_rows, label_encode_cols=None, onehot_encode_cols=None):
    # Copy the original DataFrame to avoid modifying it
    encoded_df = df_cleaned_rows.copy()

    # Label encoding
    if label_encode_cols:
        label_encoder = LabelEncoder()
        for col in label_encode_cols:
            if col in encoded_df.columns:
                encoded_df[col] = label_encoder.fit_transform(encoded_df[col])

    # One-hot encoding
    if onehot_encode_cols:
        encoded_df = pd.get_dummies(encoded_df, columns=onehot_encode_cols, dtype=int)

    return encoded_df

# Specify columns for label encoding and one-hot encoding
label_encode_columns = ['gender', 'smoking_history']

# Apply the encoding function
df_encoded = encode_columns(droped_dup_df, label_encode_cols=label_encode_columns)

# Set the option to display all columns
pd.set_option('display.max_columns', None)

print("\nEncoded dataset preview:")
print(df_encoded.head())

# Classification function
def run_classification(df, target_column=None, model_name=None):

    # Copy the original DataFrame to avoid modifying it
    df_copy = df.copy()

    # Separate features (X) and target variable (y)
    X = df_copy.drop(columns=[target_column], axis=1)
    y = df_copy[target_column]

    # SPLITTING DATA
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # MODELLING
    # Initialize the selected model
    if model_name == 'LR':
        model_type = 'Logistic Regression'
        model = LogisticRegression(random_state=42, max_iter=10000)
    elif model_name == 'DT':
        model_type = 'Decision Tree'
        model = DecisionTreeClassifier(random_state=42)
    elif model_name == 'NB':
        model_type = 'Naive Bayes'
        model = GaussianNB()
    elif model_name == 'SVM':
        model_type = 'Support Vector Machine'
        model = SVC(random_state=42)
    elif model_name == 'RF':
        model_type = 'Random Forest'
        model = RandomForestClassifier(random_state=42)
    else:
        raise ValueError("Invalid model_name. Choose from 'LR', 'DT', 'NB', 'SVM', 'RF'.")

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1_score, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    # Display the evaluation metrics
    print(f"\n{model_type} Model Accuracy:", accuracy)
    print(f"\n{model_type} Model Confusion Matrix:\n", conf_matrix)
    print(f"\n{model_type} Model Classification Report:\n", classification_rep)

    # Get variable importance if supported by the model
    variable_importance = None
    if hasattr(model, 'feature_importances_'):
        variable_importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        variable_importance = np.abs(model.coef_[0])

    # Display variable importance if available
    if variable_importance is not None:
        variable_importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': variable_importance})
        print(f"\n{model_type} Model Variable Importance:\n")
        print(variable_importance_df)

    # Store metrics in a dictionary
    metrics = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1_score,
        'Variable Importance': variable_importance
    }

    return metrics

# Collect accuracy values for each model
accuracies = {}
# Specify the target column name
target_column_name = 'diabetes'

print("\n" + "="*60)
print("TRAINING MODELS")
print("="*60)

# Run Logistic Regression model and print metrics
print("\n[1/5] Training Logistic Regression...")
lr_metrics = run_classification(df_encoded, target_column=target_column_name, model_name='LR')
accuracies['Logistic Regression'] = lr_metrics['Accuracy']

# Run Decision Tree model and print metrics
print("\n[2/5] Training Decision Tree...")
dt_metrics = run_classification(df_encoded, target_column=target_column_name, model_name='DT')
accuracies['Decision Tree'] = dt_metrics['Accuracy']

# Run Naive Bayes model and print metrics
print("\n[3/5] Training Naive Bayes...")
nb_metrics = run_classification(df_encoded, target_column=target_column_name, model_name='NB')
accuracies['Naive Bayes'] = nb_metrics['Accuracy']

# Run Support Vector Machine model and print metrics
print("\n[4/5] Training Support Vector Machine...")
svm_metrics = run_classification(df_encoded, target_column=target_column_name, model_name='SVM')
accuracies['Support Vector Machine'] = svm_metrics['Accuracy']

# Run Random Forest model and print metrics
print("\n[5/5] Training Random Forest...")
rf_metrics = run_classification(df_encoded, target_column=target_column_name, model_name='RF')
accuracies['Random Forest'] = rf_metrics['Accuracy']

# Convert to DataFrame and sort by accuracy
accuracy_df = pd.DataFrame(list(accuracies.items()), columns=['Model', 'Accuracy'])
accuracy_df = accuracy_df.sort_values(by='Accuracy', ascending=False)

# Plot Model Comparison
plt.figure(figsize=(10, 5))
ax = sns.barplot(x='Model', y='Accuracy', data=accuracy_df, palette='mako')

# Display accuracy values on top of bars
for bar in ax.patches:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.005,
        f"{height:.2f}",
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# Final touches
plt.title('Model Comparison - Accuracy', fontsize=14, fontweight='bold')
plt.ylabel('Accuracy', fontsize=12)
plt.xlabel('Model', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'model_comparison_accuracy.png'), dpi=300, bbox_inches='tight')
plt.close()
print("\nSaved: model_comparison_accuracy.png")

print("\n" + "="*60)
print("MODEL ACCURACY SUMMARY")
print("="*60)
print(accuracy_df.to_string(index=False))
print("="*60)

# Save the best model (Random Forest) and required metadata for frontend
print("\n" + "="*60)
print("SAVING BEST MODEL (Random Forest)")
print("="*60)

# Train Random Forest model again to save it with all necessary data
# Prepare data
X_rf = df_encoded.drop(columns=[target_column_name], axis=1)
y_rf = df_encoded[target_column_name]

# Split data (same random_state for consistency)
X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, y_rf, test_size=0.2, random_state=42)

# Train the best model
best_model = RandomForestClassifier(random_state=42)
best_model.fit(X_train_rf, y_train_rf)

# Get feature names
feature_names = list(X_train_rf.columns)

# Create directory for saved models if it doesn't exist
model_dir = "saved_models"
os.makedirs(model_dir, exist_ok=True)

# Save the trained model
model_path = os.path.join(model_dir, "diabetes_rf_model.pkl")
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"[OK] Model saved to: {model_path}")

# Save label encoders mapping (for gender and smoking_history)
label_encoders_info = {
    'gender': {
        'classes': ['Female', 'Male', 'Other'],
        'encoded_values': [0, 1, 2]
    },
    'smoking_history': {
        'classes': ['No Info', 'current', 'ever', 'former', 'never', 'not current'],
        'encoded_values': [0, 1, 2, 3, 4, 5]
    }
}

# Get feature importance from the model
feature_importance_dict = {
    feature_names[i]: float(importance) 
    for i, importance in enumerate(best_model.feature_importances_)
}

# Save feature names and order
model_metadata = {
    'model_type': 'RandomForestClassifier',
    'feature_names': feature_names,
    'target_column': target_column_name,
    'label_encoders': label_encoders_info,
    'model_metrics': {
        'accuracy': float(rf_metrics['Accuracy']),
        'precision': float(rf_metrics['Precision']),
        'recall': float(rf_metrics['Recall']),
        'f1_score': float(rf_metrics['F1-Score'])
    },
    'feature_importance': feature_importance_dict,
    'model_parameters': {
        'random_state': 42,
        'n_estimators': 100,  # Default for RandomForestClassifier
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1
    },
    'input_features_description': {
        'gender': 'Categorical: Female=0, Male=1, Other=2',
        'age': 'Numeric: Age in years',
        'hypertension': 'Binary: 0=No, 1=Yes',
        'heart_disease': 'Binary: 0=No, 1=Yes',
        'smoking_history': 'Categorical: No Info=0, current=1, ever=2, former=3, never=4, not current=5',
        'bmi': 'Numeric: Body Mass Index',
        'HbA1c_level': 'Numeric: Hemoglobin A1c level (%)',
        'blood_glucose_level': 'Numeric: Blood glucose level (mg/dL)'
    },
    'prediction_classes': {
        0: 'No Diabetes',
        1: 'Diabetes'
    }
}

# Save metadata as JSON
metadata_path = os.path.join(model_dir, "diabetes_model_metadata.json")
with open(metadata_path, 'w') as f:
    json.dump(model_metadata, f, indent=4)
print(f"[OK] Model metadata saved to: {metadata_path}")

# Save a simple example of how to use the model (for frontend reference)
example_usage = {
    'example_input': {
        'gender': 0,  # Female
        'age': 45.0,
        'hypertension': 0,
        'heart_disease': 0,
        'smoking_history': 4,  # never
        'bmi': 25.5,
        'HbA1c_level': 5.5,
        'blood_glucose_level': 100
    },
    'usage_instructions': {
        'step1': 'Load the model using pickle.load()',
        'step2': 'Prepare input data as numpy array with features in order: gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level',
        'step3': 'Use model.predict() for class prediction or model.predict_proba() for probability',
        'step4': 'Map prediction: 0 = No Diabetes, 1 = Diabetes'
    }
}

example_path = os.path.join(model_dir, "model_usage_example.json")
with open(example_path, 'w') as f:
    json.dump(example_usage, f, indent=4)
print(f"[OK] Usage example saved to: {example_path}")

print("\n" + "="*60)
print("[OK] Model and metadata saved successfully!")
print("="*60)
print(f"Files saved in '{model_dir}' directory:")
print(f"   - diabetes_rf_model.pkl (trained model)")
print(f"   - diabetes_model_metadata.json (model metadata)")
print(f"   - model_usage_example.json (usage instructions)")
print("="*60)

print("\n" + "="*60)
print("[OK] All charts saved successfully!")
print("="*60)
print(f"Charts saved in '{results_dir}' directory:")
chart_files = [
    'correlation_heatmap.png',
    'diabetes_distribution.png',
    'diabetes_pie_chart.png',
    'age_distribution.png',
    'age_distribution_by_diabetes.png',
    'smoking_history_diabetes.png',
    'gender_distribution.png',
    'gender_diabetes_analysis.png',
    'gender_age_comparison.png',
    'bmi_distribution_by_diabetes.png',
    'blood_glucose_level_by_diabetes.png',
    'hba1c_level_distribution_by_diabetes.png',
    'model_comparison_accuracy.png'
]
for chart_file in chart_files:
    print(f"   - {chart_file}")
print("="*60)

print("\n[OK] Script execution completed successfully!")
