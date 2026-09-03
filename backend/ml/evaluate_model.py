"""
Standalone model evaluation script.
Run: python ml/evaluate_model.py
"""
import os
import sys
import json
import base64
import io

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'fertilizer_model.pkl')
DATASET_PATH = os.path.join(SCRIPT_DIR, 'fertilizer_data.csv')
METRICS_PATH = os.path.join(SCRIPT_DIR, 'model_metrics.json')

FEATURE_NAMES = ['Nitrogen', 'Phosphorous', 'Potassium', 'Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type']


def evaluate():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}. Run train_model.py first.")
        sys.exit(1)

    if not os.path.exists(DATASET_PATH):
        print(f"Dataset not found at {DATASET_PATH}. Run train_model.py first.")
        sys.exit(1)

    # Load model
    bundle = joblib.load(MODEL_PATH)
    model = bundle['model']
    le_fertilizer = bundle['label_encoder']
    le_soil = bundle['feature_encoders']['Soil Type']
    le_crop = bundle['feature_encoders']['Crop Type']
    class_names = bundle['fertilizer_classes']

    # Load dataset
    df = pd.read_csv(DATASET_PATH)
    df['Soil Type'] = le_soil.transform(df['Soil Type'])
    df['Crop Type'] = le_crop.transform(df['Crop Type'])
    df['Fertilizer Name'] = le_fertilizer.transform(df['Fertilizer Name'])

    X = df[FEATURE_NAMES].values
    y = df['Fertilizer Name'].values

    # Predict
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    report = classification_report(y, y_pred, target_names=class_names, output_dict=True)

    print(f"\n=== Model Evaluation Results ===")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nClassification Report:")
    print(classification_report(y, y_pred, target_names=class_names))

    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    cm_b64 = base64.b64encode(buf.read()).decode('utf-8')

    metrics = {
        "accuracy": round(accuracy, 4),
        "report": report,
        "confusion_matrix_b64": cm_b64,
        "class_names": class_names,
    }
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\nMetrics saved to {METRICS_PATH}")
    return metrics


if __name__ == '__main__':
    evaluate()
