"""
Kidney Disease Prediction Model
Converts notebook to Python script with model training, evaluation, and saving capabilities
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.impute import SimpleImputer
import warnings
import os
import json
import joblib
from datetime import datetime

warnings.filterwarnings('ignore')

# Create results directory if it doesn't exist
RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)

# Dataset path - updated to use local file
DATASET_PATH = 'kidney_disease_dataset.csv'

print("="*50)
print("KIDNEY DISEASE PREDICTION MODEL")
print("="*50)

# Load and explore the dataset
print("\nLoading dataset...")
df = pd.read_csv(DATASET_PATH)

print("Dataset Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nTarget variable distribution:")
target_dist = df['Target'].value_counts()
print(target_dist)

# Data Preprocessing
print("\n" + "="*50)
print("DATA PREPROCESSING")
print("="*50)

# Handle categorical variables
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
    df[col] = df[col].map({'yes': 1, 'no': 0})

# Convert other categorical variables
df['Appetite'] = df['Appetite (good/poor)'].map({'good': 1, 'poor': 0})
df['Physical activity level'] = df['Physical activity level'].map({'low': 0, 'moderate': 1, 'high': 2})

# Handle specific gravity and other categoricals
label_encoders = {}
for col in ['Red blood cells in urine', 'Pus cells in urine', 'Pus cell clumps in urine', 
            'Bacteria in urine', 'Urinary sediment microscopy results']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Handle missing values if any
print("\nMissing values before imputation:")
missing_values = df.isnull().sum()
print(missing_values)

# Impute missing values on all numeric columns first
numeric_columns = df.select_dtypes(include=[np.number]).columns
imputer_all = SimpleImputer(strategy='median')
df[numeric_columns] = imputer_all.fit_transform(df[numeric_columns])

# Prepare features and target variable
print("\n" + "="*50)
print("PREPARING FEATURES AND TARGET")
print("="*50)

X = df.drop('Target', axis=1)
y = df['Target']

# Remove original categorical columns that we've encoded
columns_to_drop = ['Appetite (good/poor)'] + categorical_columns
X = X.drop([col for col in columns_to_drop if col in X.columns], axis=1)

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Save feature names for frontend
feature_names = list(X.columns)

# Split the data
print("\n" + "="*50)
print("SPLITTING DATA")
print("="*50)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Training set size: {X_train.shape}")
print(f"Testing set size: {X_test.shape}")

# Create and fit imputer on the final feature set (29 features) using training data only
# This ensures the imputer matches the features used by the model and avoids data leakage
imputer = SimpleImputer(strategy='median')
X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=feature_names, index=X_train.index)
X_test = pd.DataFrame(imputer.transform(X_test), columns=feature_names, index=X_test.index)

# Feature Scaling
print("\n" + "="*50)
print("FEATURE SCALING")
print("="*50)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
print("\n" + "="*50)
print("INITIALIZING MODELS")
print("="*50)

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Neural Network': MLPClassifier(random_state=42, max_iter=1000)
}

# Train and evaluate models
print("\n" + "="*50)
print("TRAINING AND EVALUATING MODELS")
print("="*50)

results = {}
classification_reports = {}
confusion_matrices = {}
trained_models = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    if name in ['Logistic Regression', 'SVM', 'Neural Network']:
        # Use scaled data for these models
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        # Use unscaled data for tree-based models
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy
    trained_models[name] = model
    classification_reports[name] = classification_report(y_test, y_pred, output_dict=True)
    confusion_matrices[name] = confusion_matrix(y_test, y_pred)
    
    print(f"\n{name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

# Compare model performances
print("\n" + "="*50)
print("MODEL COMPARISON")
print("="*50)

for name, accuracy in results.items():
    print(f"{name}: {accuracy:.4f}")

# Visualize results - Model Comparison Chart
print("\n" + "="*50)
print("GENERATING VISUALIZATIONS")
print("="*50)

plt.figure(figsize=(12, 6))
models_list = list(results.keys())
accuracies = list(results.values())

plt.bar(models_list, accuracies, color=['blue', 'green', 'orange', 'red', 'purple'])
plt.title('Model Comparison - Accuracy Scores', fontsize=14, fontweight='bold')
plt.xlabel('Models', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 1)
for i, v in enumerate(accuracies):
    plt.text(i, v + 0.01, f'{v:.4f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'model_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: model_comparison.png")

# Hyperparameter Tuning for Best Model
print("\n" + "="*50)
print("HYPERPARAMETER TUNING")
print("="*50)

# Determine best model based on accuracy
best_model_name = max(results, key=results.get)
print(f"Best model based on initial evaluation: {best_model_name}")

# Tune Random Forest (often performs well)
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestClassifier(random_state=42)
grid_search_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1)
grid_search_rf.fit(X_train, y_train)

print("Best parameters for Random Forest:", grid_search_rf.best_params_)
print("Best cross-validation score:", grid_search_rf.best_score_)

# Evaluate tuned model
best_rf = grid_search_rf.best_estimator_
y_pred_tuned = best_rf.predict(X_test)
tuned_accuracy = accuracy_score(y_test, y_pred_tuned)
print(f"Tuned Random Forest Test Accuracy: {tuned_accuracy:.4f}")

# Use tuned model if it's better, otherwise use the best from initial evaluation
if tuned_accuracy > results.get('Random Forest', 0):
    best_model = best_rf
    best_model_name = 'Random Forest (Tuned)'
    best_accuracy = tuned_accuracy
    use_scaled = False
else:
    best_model = trained_models[best_model_name]
    best_accuracy = results[best_model_name]
    use_scaled = best_model_name in ['Logistic Regression', 'SVM', 'Neural Network']

print(f"\nFinal Best Model: {best_model_name}")
print(f"Final Best Accuracy: {best_accuracy:.4f}")

# Generate confusion matrix for best model
if use_scaled:
    y_pred_best = best_model.predict(X_test_scaled)
else:
    y_pred_best = best_model.predict(X_test)

best_confusion_matrix = confusion_matrix(y_test, y_pred_best)
best_classification_report = classification_report(y_test, y_pred_best, output_dict=True)

# Visualize confusion matrix for best model
plt.figure(figsize=(10, 8))
sns.heatmap(best_confusion_matrix, annot=True, fmt='d', cmap='Blues', 
            xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))
plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'best_model_confusion_matrix.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: best_model_confusion_matrix.png")

# Generate detailed comparison chart with all metrics
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Accuracy comparison
axes[0, 0].bar(models_list, accuracies, color=['blue', 'green', 'orange', 'red', 'purple'])
axes[0, 0].set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Models')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].set_ylim(0, 1)
for i, v in enumerate(accuracies):
    axes[0, 0].text(i, v + 0.01, f'{v:.4f}', ha='center', va='bottom', fontsize=9)

# Confusion matrices for all models
model_names_short = ['LR', 'DT', 'SVM', 'RF', 'NN']
for idx, (name, cm) in enumerate(confusion_matrices.items()):
    row = (idx // 3) + 1
    col = idx % 3
    if row < 2 and col < 2:
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[row, col], cbar=False)
        axes[row, col].set_title(f'{model_names_short[idx]}', fontsize=10)
        axes[row, col].set_xlabel('Predicted')
        axes[row, col].set_ylabel('True')

# Classification metrics comparison
metrics_data = []
for name in models_list:
    if name in classification_reports:
        report = classification_reports[name]
        metrics_data.append({
            'Model': name,
            'Precision': report['weighted avg']['precision'],
            'Recall': report['weighted avg']['recall'],
            'F1-Score': report['weighted avg']['f1-score']
        })

metrics_df = pd.DataFrame(metrics_data)
x_pos = np.arange(len(models_list))
width = 0.25

axes[1, 0].bar(x_pos - width, metrics_df['Precision'], width, label='Precision', color='skyblue')
axes[1, 0].bar(x_pos, metrics_df['Recall'], width, label='Recall', color='lightgreen')
axes[1, 0].bar(x_pos + width, metrics_df['F1-Score'], width, label='F1-Score', color='salmon')
axes[1, 0].set_title('Precision, Recall, F1-Score Comparison', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Models')
axes[1, 0].set_ylabel('Score')
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(model_names_short, rotation=45)
axes[1, 0].legend()
axes[1, 0].set_ylim(0, 1)

# Target distribution
axes[1, 1].bar(target_dist.index, target_dist.values, color='steelblue')
axes[1, 1].set_title('Target Variable Distribution', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Target Classes')
axes[1, 1].set_ylabel('Count')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'detailed_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Saved: detailed_comparison.png")

# Save model comparison results to CSV
comparison_df = pd.DataFrame({
    'Model': models_list,
    'Accuracy': accuracies,
    'Precision': [classification_reports[m]['weighted avg']['precision'] for m in models_list],
    'Recall': [classification_reports[m]['weighted avg']['recall'] for m in models_list],
    'F1-Score': [classification_reports[m]['weighted avg']['f1-score'] for m in models_list]
})
comparison_df.to_csv(os.path.join(RESULTS_DIR, 'model_comparison.csv'), index=False)
print("Saved: model_comparison.csv")

# Save best model and required components for frontend
print("\n" + "="*50)
print("SAVING BEST MODEL AND METADATA")
print("="*50)

MODEL_DIR = 'saved_model'
os.makedirs(MODEL_DIR, exist_ok=True)

# Save the best model
model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
joblib.dump(best_model, model_path)
print(f"Saved best model to: {model_path}")

# Save scaler if needed
if use_scaled:
    scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"Saved scaler to: {scaler_path}")
else:
    scaler_path = None

# Save label encoders
encoders_path = os.path.join(MODEL_DIR, 'label_encoders.pkl')
joblib.dump(label_encoders, encoders_path)
print(f"Saved label encoders to: {encoders_path}")

# Save imputer
imputer_path = os.path.join(MODEL_DIR, 'imputer.pkl')
joblib.dump(imputer, imputer_path)
print(f"Saved imputer to: {imputer_path}")

# Create metadata for frontend
metadata = {
    'model_name': best_model_name,
    'model_type': type(best_model).__name__,
    'accuracy': float(best_accuracy),
    'use_scaled_features': use_scaled,
    'feature_names': feature_names,
    'target_classes': sorted(y.unique().tolist()),
    'model_path': model_path,
    'scaler_path': scaler_path,
    'imputer_path': imputer_path,
    'encoders_path': encoders_path,
    'training_date': datetime.now().isoformat(),
    'dataset_path': DATASET_PATH,
    'n_features': len(feature_names),
    'n_samples_train': int(X_train.shape[0]),
    'n_samples_test': int(X_test.shape[0]),
    'classification_report': best_classification_report,
    'confusion_matrix': best_confusion_matrix.tolist(),
    'model_parameters': best_model.get_params() if hasattr(best_model, 'get_params') else {}
}

# Save metadata as JSON
metadata_path = os.path.join(MODEL_DIR, 'model_metadata.json')
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=4, default=str)
print(f"Saved metadata to: {metadata_path}")

# Save feature importance if available (for tree-based models)
if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    feature_importance_path = os.path.join(RESULTS_DIR, 'feature_importance.csv')
    feature_importance.to_csv(feature_importance_path, index=False)
    print(f"Saved feature importance to: {feature_importance_path}")
    
    # Visualize feature importance
    plt.figure(figsize=(12, 8))
    top_features = feature_importance.head(15)
    plt.barh(range(len(top_features)), top_features['importance'], color='steelblue')
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance', fontsize=12)
    plt.title('Top 15 Feature Importances', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'feature_importance.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: feature_importance.png")

# Create a summary report
summary_report = f"""
{'='*60}
KIDNEY DISEASE PREDICTION MODEL - TRAINING SUMMARY
{'='*60}

Dataset Information:
- Dataset Path: {DATASET_PATH}
- Total Samples: {df.shape[0]}
- Total Features: {len(feature_names)}
- Training Samples: {X_train.shape[0]}
- Testing Samples: {X_test.shape[0]}

Model Performance Comparison:
"""
for name, acc in results.items():
    summary_report += f"- {name}: {acc:.4f}\n"

summary_report += f"""
Best Model:
- Model Name: {best_model_name}
- Accuracy: {best_accuracy:.4f}
- Model Type: {type(best_model).__name__}
- Uses Scaled Features: {use_scaled}

Target Classes:
"""
for cls in sorted(y.unique()):
    summary_report += f"- {cls}\n"

summary_report += f"""
Saved Files:
- Model: {model_path}
- Metadata: {metadata_path}
- Results Directory: {RESULTS_DIR}/
  - model_comparison.png
  - model_comparison.csv
  - detailed_comparison.png
  - best_model_confusion_matrix.png
  - feature_importance.png (if available)
  - feature_importance.csv (if available)

Training completed successfully!
{'='*60}
"""

print(summary_report)

# Save summary report
summary_path = os.path.join(RESULTS_DIR, 'training_summary.txt')
with open(summary_path, 'w') as f:
    f.write(summary_report)
print(f"Saved summary report to: {summary_path}")

print("\n" + "="*50)
print("ALL TASKS COMPLETED SUCCESSFULLY!")
print("="*50)
