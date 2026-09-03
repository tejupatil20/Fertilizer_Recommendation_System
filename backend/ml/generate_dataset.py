"""
Dataset generation script for fertilizer recommendation model.
Generates a synthetic 5000-row dataset with realistic correlations.
"""
import numpy as np
import pandas as pd
import os

# Reproducibility
np.random.seed(42)

CROP_TYPES = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts']
SOIL_TYPES = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
FERTILIZERS = ['Urea', 'DAP', '14-35-14', '28-28', '17-17-17', '20-20', '10-26-26']

N_SAMPLES = 5000


def get_fertilizer(row: dict) -> str:
    """Rule-based fertilizer assignment with realistic correlations."""
    N = row['Nitrogen']
    P = row['Phosphorous']
    K = row['Potassium']
    crop = row['Crop Type']
    soil = row['Soil Type']
    temp = row['Temperature']

    # High N deficiency (low N) → Urea
    if N < 30 and P < 40:
        return 'Urea'

    # High P requirement (low P, high N) → DAP
    if P < 35 and N > 35:
        return 'DAP'

    # Paddy / Rice on Black soil → 17-17-17 or 10-26-26
    if crop in ('Paddy',) and soil == 'Black':
        return np.random.choice(['17-17-17', '10-26-26'], p=[0.6, 0.4])

    # Sugarcane needs high N and balanced P/K
    if crop == 'Sugarcane' and N > 60:
        return '20-20'

    # Cotton on Red/Sandy soil → 14-35-14
    if crop == 'Cotton' and soil in ('Red', 'Sandy'):
        return '14-35-14'

    # Wheat/Barley → DAP or 28-28
    if crop in ('Wheat', 'Barley'):
        if P < 50:
            return 'DAP'
        return '28-28'

    # Pulses / Oil seeds → 14-35-14 (low N, high P)
    if crop in ('Pulses', 'Oil seeds', 'Ground Nuts'):
        return '14-35-14'

    # Millets → Urea or 20-20
    if crop == 'Millets':
        return np.random.choice(['Urea', '20-20'], p=[0.7, 0.3])

    # Tobacco on Loamy soil
    if crop == 'Tobacco' and soil == 'Loamy':
        return '17-17-17'

    # Maize needs balanced NPK
    if crop == 'Maize':
        if N < 50 and P < 50 and K < 50:
            return '17-17-17'
        if K > 100:
            return '10-26-26'
        return '28-28'

    # High K requirement
    if K > 140 and P > 80:
        return '10-26-26'

    # Default
    return np.random.choice(FERTILIZERS)


records = []
for _ in range(N_SAMPLES):
    crop = np.random.choice(CROP_TYPES)
    soil = np.random.choice(SOIL_TYPES)
    N = int(np.random.randint(0, 141))
    P = int(np.random.randint(0, 146))
    K = int(np.random.randint(0, 206))
    temp = round(float(np.random.uniform(15, 45)), 1)
    humidity = round(float(np.random.uniform(14, 100)), 1)
    moisture = round(float(np.random.uniform(10, 60)), 1)

    row = {
        'Nitrogen': N,
        'Phosphorous': P,
        'Potassium': K,
        'Temperature': temp,
        'Humidity': humidity,
        'Moisture': moisture,
        'Soil Type': soil,
        'Crop Type': crop,
    }
    row['Fertilizer Name'] = get_fertilizer(row)
    records.append(row)

df = pd.DataFrame(records)

# Save next to this script
output_path = os.path.join(os.path.dirname(__file__), 'fertilizer_data.csv')
df.to_csv(output_path, index=False)
print(f"Dataset saved to: {output_path}")
print(f"Shape: {df.shape}")
print("\nFertilizer distribution:")
print(df['Fertilizer Name'].value_counts())
print("\nCrop distribution:")
print(df['Crop Type'].value_counts())

if __name__ == '__main__':
    pass  # Already runs on import during training
