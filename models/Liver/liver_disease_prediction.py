import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import VotingClassifier

# Create directories
results_dir = Path('results')
results_dir.mkdir(exist_ok=True)
charts_dir = results_dir / 'charts'
charts_dir.mkdir(exist_ok=True)
saved_models_dir = Path('saved_models')
saved_models_dir.mkdir(exist_ok=True)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("=" * 60)
print("Liver Disease Prediction - Model Training Script")
print("=" * 60)

# Loading the dataset - Updated path
dataset_path = 'Liver Patient Dataset (LPD)_train.csv'
print(f"\nLoading dataset from: {dataset_path}")
df = pd.read_csv(dataset_path, encoding='unicode_escape')

print("Dataset Shape: ", df.shape)
print("\nColumns: ", df.columns.tolist())

# Display first few rows
print("\nFirst 5 rows:")
print(df.head())

# Mapping 'Male' to 1 and 'Female' to 0 in the 'Gender of the patient' column
df['Gender of the patient'] = df['Gender of the patient'].map({'Male': 1, 'Female': 0})

# No liver disease then:=0 for having liver disease then:=1
df['Result'] = df['Result'].map({1: 1, 2: 0})

# Calculate correlation matrix
corr_matrix = df.corr()

# Plot and save the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap="Greens", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix for Liver Dataset", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(charts_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
print(f"\nSaved correlation matrix to: {charts_dir / 'correlation_matrix.png'}")
plt.close()

# Check for null values
print("\nNull values:")
null_counts = df.isnull().sum()
print(null_counts)

# Drop null values
df = df.dropna()
print("\nAfter dropping null values:")
print(df.isnull().sum())

# Drop duplicates
df = df.drop_duplicates()
print("\nDataset info after cleaning:")
print(df.info())

# Splitting dataset into train and test
X = df.drop('Result', axis=1)
y = df['Result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1337)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Store models and accuracies
models = {}
accuracies = {}
predictions = {}

print("\n" + "=" * 60)
print("Training Models...")
print("=" * 60)

# Random Forest (RF)
print("\nTraining Random Forest...")
rf_model = RandomForestClassifier(random_state=1337)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_predictions)
models['Random Forest'] = rf_model
accuracies['Random Forest'] = rf_accuracy
predictions['Random Forest'] = rf_predictions
print(f"Random Forest Accuracy: {rf_accuracy:.6f}")

# Decision Tree Classifier (DT)
print("\nTraining Decision Tree...")
dt_model = DecisionTreeClassifier(random_state=1337)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_predictions)
models['Decision Tree'] = dt_model
accuracies['Decision Tree'] = dt_accuracy
predictions['Decision Tree'] = dt_predictions
print(f"Decision Tree Accuracy: {dt_accuracy:.6f}")

# Multilayer Perceptron (MP)
print("\nTraining Multilayer Perceptron...")
mp_model = MLPClassifier(random_state=1337, max_iter=1000)
mp_model.fit(X_train, y_train)
mp_predictions = mp_model.predict(X_test)
mp_accuracy = accuracy_score(y_test, mp_predictions)
models['Multilayer Perceptron'] = mp_model
accuracies['Multilayer Perceptron'] = mp_accuracy
predictions['Multilayer Perceptron'] = mp_predictions
print(f"Multilayer Perceptron Accuracy: {mp_accuracy:.6f}")

# XGBoost (XGB)
print("\nTraining XGBoost...")
xgb_model = XGBClassifier(random_state=1337, eval_metric='logloss')
xgb_model.fit(X_train, y_train)
xgb_predictions = xgb_model.predict(X_test)
xgb_accuracy = accuracy_score(y_test, xgb_predictions)
models['XGBoost'] = xgb_model
accuracies['XGBoost'] = xgb_accuracy
predictions['XGBoost'] = xgb_predictions
print(f"XGBoost Accuracy: {xgb_accuracy:.6f}")

# Logistic Regression (LR)
print("\nTraining Logistic Regression...")
lr_model = LogisticRegression(random_state=1337, max_iter=1000)
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_predictions)
models['Logistic Regression'] = lr_model
accuracies['Logistic Regression'] = lr_accuracy
predictions['Logistic Regression'] = lr_predictions
print(f"Logistic Regression Accuracy: {lr_accuracy:.6f}")

# K-Nearest Neighbors (KNN)
print("\nTraining K-Nearest Neighbors...")
knn_model = KNeighborsClassifier()
knn_model.fit(X_train, y_train)
knn_predictions = knn_model.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_predictions)
models['K-Nearest Neighbors'] = knn_model
accuracies['K-Nearest Neighbors'] = knn_accuracy
predictions['K-Nearest Neighbors'] = knn_predictions
print(f"K-Nearest Neighbors Accuracy: {knn_accuracy:.6f}")

# Support Vector Machine (SVM)
print("\nTraining Support Vector Machine...")
svm_model = SVC(random_state=1337)
svm_model.fit(X_train, y_train)
svm_predictions = svm_model.predict(X_test)
svm_accuracy = accuracy_score(y_test, svm_predictions)
models['Support Vector Machine'] = svm_model
accuracies['Support Vector Machine'] = svm_accuracy
predictions['Support Vector Machine'] = svm_predictions
print(f"Support Vector Machine Accuracy: {svm_accuracy:.6f}")

# Naïve Bayes
print("\nTraining Naïve Bayes...")
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
nb_predictions = nb_model.predict(X_test)
nb_accuracy = accuracy_score(y_test, nb_predictions)
models['Naïve Bayes'] = nb_model
accuracies['Naïve Bayes'] = nb_accuracy
predictions['Naïve Bayes'] = nb_predictions
print(f"Naïve Bayes Accuracy: {nb_accuracy:.6f}")

# LightGBM
print("\nTraining LightGBM...")
lgbm_model = LGBMClassifier(random_state=1337, verbose=-1)
lgbm_model.fit(X_train, y_train)
lgbm_predictions = lgbm_model.predict(X_test)
lgbm_accuracy = accuracy_score(y_test, lgbm_predictions)
models['LightGBM'] = lgbm_model
accuracies['LightGBM'] = lgbm_accuracy
predictions['LightGBM'] = lgbm_predictions
print(f"LightGBM Accuracy: {lgbm_accuracy:.6f}")

# Artificial Neural Network (ANN)
print("\nTraining Artificial Neural Network...")
ann_model = MLPClassifier(random_state=1337, max_iter=1000)
ann_model.fit(X_train, y_train)
ann_predictions = ann_model.predict(X_test)
ann_accuracy = accuracy_score(y_test, ann_predictions)
models['Artificial Neural Network'] = ann_model
accuracies['Artificial Neural Network'] = ann_accuracy
predictions['Artificial Neural Network'] = ann_predictions
print(f"Artificial Neural Network Accuracy: {ann_accuracy:.6f}")

# Gradient Boosting (GB)
print("\nTraining Gradient Boosting...")
gb_model = GradientBoostingClassifier(random_state=1337)
gb_model.fit(X_train, y_train)
gb_predictions = gb_model.predict(X_test)
gb_accuracy = accuracy_score(y_test, gb_predictions)
models['Gradient Boosting'] = gb_model
accuracies['Gradient Boosting'] = gb_accuracy
predictions['Gradient Boosting'] = gb_predictions
print(f"Gradient Boosting Accuracy: {gb_accuracy:.6f}")

# Create accuracy comparison DataFrame
accuracy_data = {
    'Model': list(accuracies.keys()),
    'Accuracy': list(accuracies.values())
}
accuracy_df = pd.DataFrame(accuracy_data)
accuracy_df = accuracy_df.sort_values(by='Accuracy', ascending=False)

print("\n" + "=" * 60)
print("Model Comparison Results:")
print("=" * 60)
print(accuracy_df.to_string(index=False))

# Save accuracy comparison table
accuracy_df.to_csv(results_dir / 'model_comparison.csv', index=False)
print(f"\nSaved model comparison to: {results_dir / 'model_comparison.csv'}")

# Create and save accuracy comparison bar chart
plt.figure(figsize=(14, 8))
colors = plt.cm.viridis(np.linspace(0, 1, len(accuracy_df)))
bars = plt.barh(accuracy_df['Model'], accuracy_df['Accuracy'], color=colors)
plt.xlabel('Accuracy', fontsize=12, fontweight='bold')
plt.ylabel('Model', fontsize=12, fontweight='bold')
plt.title('Model Accuracy Comparison', fontsize=16, fontweight='bold')
plt.xlim([0, 1])
plt.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, (idx, row) in enumerate(accuracy_df.iterrows()):
    plt.text(row['Accuracy'] + 0.01, i, f"{row['Accuracy']:.4f}", 
             va='center', fontsize=10)

plt.tight_layout()
plt.savefig(charts_dir / 'accuracy_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved accuracy comparison chart to: {charts_dir / 'accuracy_comparison.png'}")
plt.close()

# Create confusion matrices for top 3 models
top_3_models = accuracy_df.head(3)['Model'].tolist()
print(f"\nCreating confusion matrices for top 3 models: {top_3_models}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, model_name in enumerate(top_3_models):
    cm = confusion_matrix(y_test, predictions[model_name])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], 
                cbar_kws={'label': 'Count'})
    axes[idx].set_title(f'{model_name}\nAccuracy: {accuracies[model_name]:.4f}', 
                        fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Predicted', fontsize=10)
    axes[idx].set_ylabel('Actual', fontsize=10)

plt.suptitle('Confusion Matrices - Top 3 Models', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(charts_dir / 'confusion_matrices_top3.png', dpi=300, bbox_inches='tight')
print(f"Saved confusion matrices to: {charts_dir / 'confusion_matrices_top3.png'}")
plt.close()

# Ensemble Voting Classifier with top 3 models
print("\n" + "=" * 60)
print("Training Ensemble Voting Classifier...")
print("=" * 60)

# Get top 3 models
top_3_model_names = accuracy_df.head(3)['Model'].tolist()
print(f"Using models: {top_3_model_names}")

# Create fresh instances for voting classifier
rf_voting = RandomForestClassifier(random_state=1337)
xgb_voting = XGBClassifier(random_state=1337, eval_metric='logloss')
lgbm_voting = LGBMClassifier(random_state=1337, verbose=-1)

voting_classifier = VotingClassifier(
    estimators=[('rf', rf_voting), ('xgb', xgb_voting), ('lgbm', lgbm_voting)],
    voting='hard'
)

voting_classifier.fit(X_train, y_train)
voting_accuracy = voting_classifier.score(X_test, y_test)
print(f"Ensemble Voting Classifier Accuracy: {voting_accuracy:.6f}")

# Determine best model
best_model_name = accuracy_df.iloc[0]['Model']
best_model = models[best_model_name]
best_accuracy = accuracies[best_model_name]

print("\n" + "=" * 60)
print(f"Best Model: {best_model_name} with Accuracy: {best_accuracy:.6f}")
print("=" * 60)

# Save the best model
model_path = saved_models_dir / 'best_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"\nSaved best model to: {model_path}")

# Save ensemble model as well
ensemble_path = saved_models_dir / 'ensemble_model.pkl'
with open(ensemble_path, 'wb') as f:
    pickle.dump(voting_classifier, f)
print(f"Saved ensemble model to: {ensemble_path}")

# Create model metadata for frontend
feature_names = X.columns.tolist()
model_metadata = {
    'model_name': best_model_name,
    'model_file': str(model_path),
    'ensemble_model_file': str(ensemble_path),
    'accuracy': float(best_accuracy),
    'ensemble_accuracy': float(voting_accuracy),
    'feature_names': feature_names,
    'feature_count': len(feature_names),
    'dataset_path': dataset_path,
    'training_samples': int(X_train.shape[0]),
    'test_samples': int(X_test.shape[0]),
    'model_type': type(best_model).__name__,
    'prediction_mapping': {
        '0': 'No Liver Disease',
        '1': 'Liver Disease'
    },
    'feature_descriptions': {
        'Age of the patient': 'Age in years',
        'Gender of the patient': '1 for Male, 0 for Female',
        'Total Bilirubin': 'Total bilirubin level',
        'Direct Bilirubin': 'Direct bilirubin level',
        ' Alkphos Alkaline Phosphotase': 'Alkaline phosphatase level',
        ' Sgpt Alamine Aminotransferase': 'ALT (SGPT) level',
        'Sgot Aspartate Aminotransferase': 'AST (SGOT) level',
        'Total Protiens': 'Total protein level',
        ' ALB Albumin': 'Albumin level',
        'A/G Ratio Albumin and Globulin Ratio': 'Albumin/Globulin ratio'
    },
    'all_model_accuracies': {k: float(v) for k, v in accuracies.items()}
}

# Save metadata as JSON
metadata_path = results_dir / 'model_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(model_metadata, f, indent=4)
print(f"Saved model metadata to: {metadata_path}")

# Create a summary report
summary_report = f"""
Liver Disease Prediction Model - Training Summary
{'=' * 60}

Dataset Information:
- Dataset Path: {dataset_path}
- Original Shape: {df.shape[0]} samples, {df.shape[1]} features
- Training Samples: {X_train.shape[0]}
- Test Samples: {X_test.shape[0]}

Best Model:
- Model Name: {best_model_name}
- Accuracy: {best_accuracy:.6f}
- Model File: {model_path}

Ensemble Model:
- Accuracy: {voting_accuracy:.6f}
- Model File: {ensemble_path}

Top 3 Models:
{accuracy_df.head(3).to_string(index=False)}

All Model Accuracies:
{accuracy_df.to_string(index=False)}

Feature Names:
{', '.join(feature_names)}

Results Saved:
- Model comparison CSV: {results_dir / 'model_comparison.csv'}
- Correlation matrix: {charts_dir / 'correlation_matrix.png'}
- Accuracy comparison chart: {charts_dir / 'accuracy_comparison.png'}
- Confusion matrices: {charts_dir / 'confusion_matrices_top3.png'}
- Best model: {model_path}
- Ensemble model: {ensemble_path}
- Model metadata: {metadata_path}

{'=' * 60}
"""

report_path = results_dir / 'training_summary.txt'
with open(report_path, 'w') as f:
    f.write(summary_report)
print(f"\nSaved training summary to: {report_path}")

print("\n" + "=" * 60)
print("Training Complete! All results saved to 'results' directory.")
print("=" * 60)
