import pickle
import numpy as np
import pandas as pd
from pipeline_models import TeamEnsemblePipeline

print("==================================================")
print("RESIDENTIAL ENERGY PREDICTION RUNNER")
print("Engineering Team Profile:")
print("  - Garv Gulati  (Reg No: RA2411003010319)")
print("  - Umang Gupta  (Reg No: RA22110030100012)")
print("  - Nikhil Goyal (Reg No: RA2411003010489)")
print("==================================================")

# 1. Load Scaler & Models
models_dir = 'c:/Machine learning/paper_models'

with open(f'{models_dir}/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open(f'{models_dir}/linear_regression.pkl', 'rb') as f:
    m_lr = pickle.load(f)
with open(f'{models_dir}/support_vector_machine.pkl', 'rb') as f:
    m_svm = pickle.load(f)
with open(f'{models_dir}/random_forest.pkl', 'rb') as f:
    m_rf = pickle.load(f)
with open(f'{models_dir}/xgboost.pkl', 'rb') as f:
    m_xgb = pickle.load(f)
with open(f'{models_dir}/deep_neural_network.pkl', 'rb') as f:
    m_mlp = pickle.load(f)
with open(f'{models_dir}/team_ensemble.pkl', 'rb') as f:
    m_ens = pickle.load(f)
with open(f'{models_dir}/isolation_forest.pkl', 'rb') as f:
    m_iso = pickle.load(f)

# 2. Example Household Input
# Feature order: [User_ID, Time, Temperature, Occupants, Apt, Duplex, AC_Room, Dev_Low, Dev_Mod]
example_household = {
    'Time': 19.0,             # 7:00 PM (Evening Peak)
    'Temperature': 22.5,      # 22.5 °C
    'Occupants': 4,           # 4-person family
    'Housing_Type': 'House',  # Single detached house (Apt=0, Duplex=0)
    'AC_Room': True,          # Air conditioning installed (AC=1)
    'Device_Usage': 'Moderate'# Moderate usage (Dev_Low=0, Dev_Mod=1)
}

user_id = 100
time_hr = example_household['Time']
temp_c = example_household['Temperature']
occupants = example_household['Occupants']
apt = 1 if example_household['Housing_Type'] == 'Apartment' else 0
duplex = 1 if example_household['Housing_Type'] == 'Duplex' else 0
ac = 1 if example_household['AC_Room'] else 0
dev_low = 1 if example_household['Device_Usage'] == 'Low' else 0
dev_mod = 1 if example_household['Device_Usage'] == 'Moderate' else 0

raw_vector = np.array([[user_id, time_hr, temp_c, occupants, apt, duplex, ac, dev_low, dev_mod]])
scaled_vector = scaler.transform(raw_vector)

# 3. Predict across all models
p_lr = m_lr.predict(scaled_vector)[0]
p_svm = m_svm.predict(scaled_vector)[0]
p_rf = m_rf.predict(scaled_vector)[0]
p_xgb = m_xgb.predict(scaled_vector)[0]
p_mlp = m_mlp.predict(scaled_vector)[0]
p_ens = m_ens.predict(raw_vector)[0]

# Anomaly screening
is_anomaly = (m_iso.predict(scaled_vector)[0] == -1) or (p_ens > 3.8) or (p_ens < 0.8)

print("\n--- Input Household Profile ---")
for k, v in example_household.items():
    print(f"  {k}: {v}")

print("\n--- Model Predictions (Active Load kW) ---")
print(f"  [1] Team Hybrid Ensemble (Super-Learner): {p_ens:.3f} kW  <-- [RECOMMENDED]")
print(f"  [2] Support Vector Machine (SVR):         {p_svm:.3f} kW")
print(f"  [3] Linear Regression (OLS):              {p_lr:.3f} kW")
print(f"  [4] XGBoost (Regularized):                {p_xgb:.3f} kW")
print(f"  [5] Random Forest (Tree Bagging):         {p_rf:.3f} kW")
print(f"  [6] Deep Neural Network (MLP):            {p_mlp:.3f} kW")

print("\n--- Multi-Tier Anomaly Diagnostics ---")
if is_anomaly:
    print("  STATUS: [ALERT] Abnormal consumption pattern detected!")
else:
    print("  STATUS: [NOMINAL] Consumption within normal 2-sigma confidence bounds.")
print("==================================================")
