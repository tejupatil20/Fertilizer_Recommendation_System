"""
Training script for the RandomForest fertilizer recommendation model.
Run from the backend/ directory: python ml/train_model.py
"""
import os
import sys
import json
import base64
import io

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Ensure we can import generate_dataset from same directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

DATASET_PATH = os.path.join(SCRIPT_DIR, 'fertilizer_data.csv')
MODEL_PATH = os.path.join(SCRIPT_DIR, 'fertilizer_model.pkl')
METRICS_PATH = os.path.join(SCRIPT_DIR, 'model_metrics.json')

FEATURE_NAMES = ['Nitrogen', 'Phosphorous', 'Potassium', 'Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type']
TARGET_COL = 'Fertilizer Name'


def generate_confusion_matrix_b64(y_true, y_pred, class_names):
    """Generate confusion matrix as base64 PNG string."""
    cm = confusion_matrix(y_true, y_pred, labels=class_names)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Greens',
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )
    ax.set_title('Fertilizer Prediction — Confusion Matrix', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def train():
    # 1. Load or generate dataset
    if not os.path.exists(DATASET_PATH):
        print("[Train] Dataset not found. Generating synthetic dataset...")
        import generate_dataset  # noqa: F401 — runs on import
    else:
        print(f"[Train] Loading dataset from {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    print(f"[Train] Dataset shape: {df.shape}")

    # 2. Encode categorical features
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    le_fertilizer = LabelEncoder()

    df['Soil Type'] = le_soil.fit_transform(df['Soil Type'])
    df['Crop Type'] = le_crop.fit_transform(df['Crop Type'])
    df[TARGET_COL] = le_fertilizer.fit_transform(df[TARGET_COL])

    X = df[FEATURE_NAMES].values
    y = df[TARGET_COL].values

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[Train] Train size: {len(X_train)}, Test size: {len(X_test)}")

    # 4. Train RandomForest
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    print("[Train] Model training complete.")

    # 5. Evaluate
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    class_names = list(le_fertilizer.classes_)
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)

    print(f"\n[Train] Accuracy: {accuracy:.4f}")
    print("[Train] Classification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 6. Confusion matrix as base64 PNG
    cm_b64 = generate_confusion_matrix_b64(y_test, y_pred, list(range(len(class_names))))

    # 7. Save metrics
    metrics = {
        "accuracy": round(accuracy, 4),
        "report": report,
        "confusion_matrix_b64": cm_b64,
        "class_names": class_names,
        "feature_names": FEATURE_NAMES,
    }
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"[Train] Metrics saved to {METRICS_PATH}")

    # 8. Save model bundle
    model_bundle = {
        'model': rf,
        'label_encoder': le_fertilizer,
        'feature_encoders': {
            'Soil Type': le_soil,
            'Crop Type': le_crop,
        },
        'feature_names': FEATURE_NAMES,
        'fertilizer_classes': class_names,
    }
    joblib.dump(model_bundle, MODEL_PATH)
    print(f"[Train] Model saved to {MODEL_PATH}")

    return accuracy


if __name__ == '__main__':
    train()
