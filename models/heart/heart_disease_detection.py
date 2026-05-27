"""
Heart Disease Detection with Machine Learning
Converts notebook to Python script with model saving and visualization export
"""

import numpy as np
import pandas as pd
import warnings
import os
import json
import joblib
from pathlib import Path

warnings.filterwarnings("ignore")

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.utils.class_weight import compute_sample_weight

import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create directories for results and models
os.makedirs('results', exist_ok=True)
os.makedirs('models', exist_ok=True)


def bar_labels(axes, rotation=0, location="edge"):
    """Helper function to add labels to bar charts"""
    for container in axes.containers:
        axes.bar_label(container, label_type=location, rotation=rotation)
    axes.set_xlabel("")
    axes.set_ylabel("")
    axes.set_yticklabels(())


def training_classification(x_train, x_test, y_train, y_test, save_results=True):
    """
    Train multiple classification models and compare their performance
    
    Args:
        x_train: Training features
        x_test: Test features
        y_train: Training labels
        y_test: Test labels
        save_results: Whether to save results to files
    
    Returns:
        best_model: The best performing model
        best_model_name: Name of the best model
        results_df: DataFrame with model scores
    """
    rfc = RandomForestClassifier()
    abc = AdaBoostClassifier()
    gbc = GradientBoostingClassifier()
    etc = ExtraTreesClassifier()
    lgr = LogisticRegression()
    svc = SVC()
    mnb = MultinomialNB()
    xgb = XGBClassifier()
    lgb = LGBMClassifier(verbose=-100)
    cat = CatBoostClassifier(verbose=False)

    models = [rfc, abc, gbc, etc, lgr,
             svc, mnb, xgb, lgb, cat]

    names = ["Random Forest", "Ada Boost", "Gradient Boosting", "Extra Trees", "Logistic Regression",
            "SVC", "Naive Bayes", "XGBoost", "LightGBM", "Cat Boost"]

    scores = []
    cms = dict()
    reports = dict()
    trained_models = dict()

    sample_weights = compute_sample_weight(
        class_weight='balanced',
        y=y_train
    )

    print("Training models...")
    for i, j in enumerate(names):
        print(f"  Training {j}...")
        models[i].fit(x_train, y_train, sample_weight=sample_weights)
        pred = models[i].predict(x_test)
        score = accuracy_score(pred, y_test)
        scores += [score]
        cms[j] = confusion_matrix(pred, y_test)
        reports[j] = classification_report(pred, y_test)
        trained_models[j] = models[i]

    dt = pd.DataFrame({"scores": scores}, index=names)
    dt = dt.sort_values("scores", ascending=False)

    dt["scores"] = dt["scores"] * 100
    dt["scores"] = round(dt["scores"], 2)

    # Save model comparison bar chart
    if save_results:
        fig, axes = plt.subplots(figsize=(15, 6))
        dt["scores"].plot(kind="bar", ax=axes, color='steelblue')
        bar_labels(axes)
        axes.set_title("Model Accuracy Comparison", fontsize=16, fontweight='bold')
        axes.set_ylabel("Accuracy (%)", fontsize=12)
        axes.set_xlabel("Model", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('results/model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved: results/model_comparison.png")

    # Save confusion matrices
    if save_results:
        index = 0
        fig_count = 0
        for _ in [5, 5]:
            fig, axes = plt.subplots(ncols=5, figsize=(20, 4))
            for i in range(5):
                if index < len(dt.index):
                    sns.heatmap(cms[dt.index[index]], annot=True, ax=axes[i], fmt='d', cmap='Blues')
                    axes[i].set_title("{}: {}%".format(dt.index[index], dt.iloc[index, 0]), fontsize=10)
                    axes[i].set_xlabel("Predicted", fontsize=9)
                    axes[i].set_ylabel("Actual", fontsize=9)
                    index += 1
            plt.tight_layout()
            plt.savefig(f'results/confusion_matrices_{fig_count}.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Saved: results/confusion_matrices_{fig_count}.png")
            fig_count += 1

    # Print classification reports
    print("\n" + "="*80)
    print("CLASSIFICATION REPORTS")
    print("="*80)
    for i in dt.index:
        print("*"*80)
        print(f"\n{i}")
        print("\n")
        print(reports[i])
        print("\n")

    # Get best model
    best_model_name = dt.index[0]
    best_model = trained_models[best_model_name]
    best_score = dt.iloc[0, 0]

    print(f"\n{'='*80}")
    print(f"BEST MODEL: {best_model_name} with {best_score}% accuracy")
    print(f"{'='*80}\n")

    return best_model, best_model_name, dt


def main():
    """Main function to run the heart disease detection pipeline"""
    
    # Update dataset path to use local file
    dataset_path = 'heart.csv'
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please ensure heart.csv is in the current directory.")
    
    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

    cats = [i for i in df.columns if df[i].nunique() <= 4]
    nums = [i for i in df.columns if i not in cats]

    print("="*80)
    print("EXPLORATORY DATA ANALYSIS - General Features")
    print("="*80)
    
    # General EDA visualizations
    index = 0
    fig_count = 0
    
    # First batch of visualizations
    for batch_size in [7, 7]:
        fig, axes = plt.subplots(ncols=batch_size, figsize=(20, 6))
        for i in range(batch_size):
            if index < len(df.columns):
                col_name = df.columns[index]
                if col_name in cats:
                    df[col_name].value_counts()[:10].plot(kind="bar", ax=axes[i], color='coral')
                    bar_labels(axes[i])
                else:
                    sns.histplot(df, x=col_name, kde=True, ax=axes[i], color='steelblue')
                    axes[i].set_xlabel("")
                    axes[i].set_ylabel("")
                axes[i].set_title(col_name.replace('_', ' ').title(), fontsize=10)
                index += 1
        plt.tight_layout()
        plt.savefig(f'results/eda_general_{fig_count}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: results/eda_general_{fig_count}.png")
        fig_count += 1

    print("\n" + "="*80)
    print("EXPLORATORY DATA ANALYSIS - Heart Problem Features")
    print("="*80)

    # Heart problems features visualization
    index = 0
    fig_count = 0
    for batch_size in [4, 4, 5]:
        fig, axes = plt.subplots(ncols=batch_size, figsize=(20, 6))
        for i in range(batch_size):
            if index < len(df.columns) - 1:  # Exclude target column
                col_name = df.columns[index]
                target_col = df.columns[-1]
                if col_name in cats:
                    df.groupby(col_name)[target_col].value_counts().unstack().plot(
                        kind="bar", stacked=True, ax=axes[i], color=['lightcoral', 'steelblue']
                    )
                    bar_labels(axes[i], 0, "center")
                    axes[i].set_title(f"Count of {col_name.replace('_', ' ').title()}\nfor Heart Patients", fontsize=10)
                    axes[i].set_xlabel("")
                    axes[i].legend(title='Heart Disease', labels=['No', 'Yes'])
                else:
                    sns.kdeplot(df, x=col_name, hue=target_col, ax=axes[i], palette=['lightcoral', 'steelblue'])
                    axes[i].set_xlabel("")
                    axes[i].set_ylabel("")
                    axes[i].set_title(f"{col_name.replace('_', ' ').title()}\nDensity Distribution\nfor Heart Patients", fontsize=10)
                    axes[i].legend(title='Heart Disease', labels=['No', 'Yes'])
                index += 1
        plt.tight_layout()
        plt.savefig(f'results/eda_heart_features_{fig_count}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: results/eda_heart_features_{fig_count}.png")
        fig_count += 1

    print("\n" + "="*80)
    print("MACHINE LEARNING MODEL TRAINING")
    print("="*80)

    # Prepare data for ML
    x = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)
    
    print(f"Training set: {x_train.shape[0]} samples")
    print(f"Test set: {x_test.shape[0]} samples\n")

    # Train models and get best model
    best_model, best_model_name, results_df = training_classification(
        x_train, x_test, y_train, y_test, save_results=True
    )

    # Save best model
    model_path = 'models/best_heart_disease_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Saved best model: {model_path}")

    # Save results DataFrame
    results_df.to_csv('results/model_scores.csv')
    print(f"Saved model scores: results/model_scores.csv")

    # Create metadata for frontend
    feature_names = df.columns[:-1].tolist()
    target_name = df.columns[-1]
    
    # Get model predictions for metadata
    predictions = best_model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    
    metadata = {
        "model_name": best_model_name,
        "model_path": model_path,
        "accuracy": float(accuracy),
        "accuracy_percentage": float(results_df.loc[best_model_name, 'scores']),
        "feature_names": feature_names,
        "target_name": target_name,
        "feature_count": len(feature_names),
        "training_samples": int(x_train.shape[0]),
        "test_samples": int(x_test.shape[0]),
        "model_type": type(best_model).__name__,
        "all_model_scores": results_df['scores'].to_dict(),
        "dataset_path": dataset_path
    }

    # Save metadata
    metadata_path = 'models/model_metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved model metadata: {metadata_path}")

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Best Model: {best_model_name}")
    print(f"Accuracy: {metadata['accuracy_percentage']:.2f}%")
    print(f"Model saved to: {model_path}")
    print(f"Metadata saved to: {metadata_path}")
    print(f"All visualizations saved to: results/")
    print("="*80)


if __name__ == "__main__":
    main()
