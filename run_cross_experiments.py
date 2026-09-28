import os
import json
import time
import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from pipeline_models import TeamEnsemblePipeline

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class BlendedModel:
    def __init__(self, etr_m, xgb_m, hgb_m, w):
        self.etr = etr_m
        self.xgb = xgb_m
        self.hgb = hgb_m
        self.w = w
    def predict(self, X_in):
        return self.w[0]*self.etr.predict(X_in) + self.w[1]*self.xgb.predict(X_in) + self.w[2]*self.hgb.predict(X_in)



print("======================================================================")
print("RUNNING CROSS-DATASET & CROSS-METHOD EXPERIMENTS")
print("1. G1 Methods on Original Dataset (19,735 records)")
print("2. Our Stacked Hybrid Model on 200-sample Dataset")
print("======================================================================")

# ==============================================================================
# PART 1: ORIGINAL HIGH-FREQUENCY SENSOR DATASET (19,735 Records)
# ==============================================================================
print("\n>>> Loading and Preparing Original Smart Home Telemetry Dataset...")
json_path = 'c:/Machine learning/KAG_Appliance_energydata.json'
if not os.path.exists(json_path):
    json_path = 'c:/Machine learning/household_power.csv'
    df_raw = pd.read_csv(json_path)
    df_raw['date'] = pd.to_datetime(df_raw['date'])
else:
    df_raw = pd.read_json(json_path)
    df_raw['date'] = pd.to_datetime(df_raw['date'])

df_raw = df_raw.sort_values('date').reset_index(drop=True)

# Outlier filter 10 to 120 Wh as per paper protocol
df_clean = df_raw[(df_raw['Appliances'] >= 10) & (df_raw['Appliances'] <= 120)].copy().reset_index(drop=True)
print(f"Operational Records Retained: {len(df_clean)} / {len(df_raw)}")

# Feature Engineering (50 features)
df_clean['Hour'] = df_clean['date'].dt.hour
df_clean['Day'] = df_clean['date'].dt.day
df_clean['Month'] = df_clean['date'].dt.month
df_clean['Weekday'] = df_clean['date'].dt.weekday
df_clean['Weekend'] = (df_clean['Weekday'] >= 5).astype(int)
df_clean['Minute'] = df_clean['date'].dt.minute
df_clean['Time_slot'] = df_clean['Hour'] * 6 + df_clean['Minute'] // 10

df_clean['Hour_sin'] = np.sin(2 * np.pi * df_clean['Hour'] / 24)
df_clean['Hour_cos'] = np.cos(2 * np.pi * df_clean['Hour'] / 24)
df_clean['Time_slot_sin'] = np.sin(2 * np.pi * df_clean['Time_slot'] / 144)
df_clean['Time_slot_cos'] = np.cos(2 * np.pi * df_clean['Time_slot'] / 144)
df_clean['Month_sin'] = np.sin(2 * np.pi * df_clean['Month'] / 12)
df_clean['Month_cos'] = np.cos(2 * np.pi * df_clean['Month'] / 12)
df_clean['Weekday_sin'] = np.sin(2 * np.pi * df_clean['Weekday'] / 7)
df_clean['Weekday_cos'] = np.cos(2 * np.pi * df_clean['Weekday'] / 7)

df_clean['is_morning_peak'] = df_clean['Hour'].isin([6, 7, 8]).astype(int)
df_clean['is_evening_peak'] = df_clean['Hour'].isin([17, 18, 19, 20, 21]).astype(int)
df_clean['is_night_standby'] = df_clean['Hour'].isin([0, 1, 2, 3, 4, 5]).astype(int)

t_cols = ['T1','T2','T3','T4','T5','T6','T7','T8','T9']
rh_cols = ['RH_1','RH_2','RH_3','RH_4','RH_5','RH_6','RH_7','RH_8','RH_9']

df_clean['T_indoor_mean'] = df_clean[t_cols].mean(axis=1)
df_clean['T_indoor_max'] = df_clean[t_cols].max(axis=1)
df_clean['T_indoor_min'] = df_clean[t_cols].min(axis=1)
df_clean['T_spread'] = df_clean['T_indoor_max'] - df_clean['T_indoor_min']
df_clean['Delta_T_out'] = df_clean['T_indoor_mean'] - df_clean['T_out']
df_clean['RH_indoor_mean'] = df_clean[rh_cols].mean(axis=1)
df_clean['Dewpoint_depression'] = df_clean['T_out'] - df_clean['Tdewpoint']
df_clean['T_living_out_diff'] = df_clean['T1'] - df_clean['T_out']

with open('c:/Machine learning/model_metadata.json', 'r') as f:
    orig_meta = json.load(f)
feature_names = orig_meta['feature_names']

X_orig = df_clean[feature_names]
y_orig = df_clean['Appliances']

X_train_o, X_test_o, y_train_o, y_test_o = train_test_split(
    X_orig, y_orig, test_size=0.30, random_state=42
)
print(f"Original Dataset Partition: Train={len(y_train_o)}, Test={len(y_test_o)}")

# Scaler for distance and neural models (SVR, MLP)
scaler_orig = StandardScaler()
X_train_o_scaled = scaler_orig.fit_transform(X_train_o)
X_test_o_scaled = scaler_orig.transform(X_test_o)

def calc_mape(y_true, y_pred):
    y_t = np.array(y_true, dtype=float)
    y_p = np.array(y_pred, dtype=float)
    mask = y_t > 0
    return float(np.mean(np.abs((y_t[mask] - y_p[mask]) / y_t[mask])) * 100)

orig_results = {}

# 1. G1 Method: Linear Regression (OLS)
print("\n[Orig 1] Fitting G1 Method: Linear Regression (OLS)...")
lr_o = LinearRegression()
lr_o.fit(X_train_o, y_train_o)
p_lr_o = lr_o.predict(X_test_o)
r2_lr = r2_score(y_test_o, p_lr_o)
orig_results['Linear Regression (G1 Method)'] = {
    'R2': round(float(r2_lr), 4),
    'MAE': round(float(mean_absolute_error(y_test_o, p_lr_o)), 2),
    'RMSE': round(float(np.sqrt(mean_squared_error(y_test_o, p_lr_o))), 2),
    'MAPE': round(calc_mape(y_test_o, p_lr_o), 2),
    'Flag': 'NORMAL' if r2_lr >= 0 else '⚠️ FLAGGED (R² < 0)'
}
print(f"  -> R2: {r2_lr:.4f}, MAE: {orig_results['Linear Regression (G1 Method)']['MAE']}")

# 2. G1 Method: Random Forest
print("\n[Orig 2] Fitting G1 Method: Random Forest Regressor (100 trees)...")
rf_o = RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
rf_o.fit(X_train_o, y_train_o)
p_rf_o = rf_o.predict(X_test_o)
r2_rf = r2_score(y_test_o, p_rf_o)
orig_results['Random Forest (G1 Method)'] = {
    'R2': round(float(r2_rf), 4),
    'MAE': round(float(mean_absolute_error(y_test_o, p_rf_o)), 2),
    'RMSE': round(float(np.sqrt(mean_squared_error(y_test_o, p_rf_o))), 2),
    'MAPE': round(calc_mape(y_test_o, p_rf_o), 2),
    'Flag': 'NORMAL' if r2_rf >= 0 else '⚠️ FLAGGED (R² < 0)'
}
print(f"  -> R2: {r2_rf:.4f}, MAE: {orig_results['Random Forest (G1 Method)']['MAE']}")

# 3. G1 Method: Deep Neural Network (MLP 50x50)
print("\n[Orig 3] Fitting G1 Method: Deep Neural Network (MLP 50x50)...")
mlp_o = MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=300, random_state=42, early_stopping=True)
mlp_o.fit(X_train_o_scaled, y_train_o)
p_mlp_o = mlp_o.predict(X_test_o_scaled)
r2_mlp = r2_score(y_test_o, p_mlp_o)
orig_results['Deep Neural Network MLP 50x50 (G1 Method)'] = {
    'R2': round(float(r2_mlp), 4),
    'MAE': round(float(mean_absolute_error(y_test_o, p_mlp_o)), 2),
    'RMSE': round(float(np.sqrt(mean_squared_error(y_test_o, p_mlp_o))), 2),
    'MAPE': round(calc_mape(y_test_o, p_mlp_o), 2),
    'Flag': 'NORMAL' if r2_mlp >= 0 else '⚠️ FLAGGED (R² < 0)'
}
print(f"  -> R2: {r2_mlp:.4f}, MAE: {orig_results['Deep Neural Network MLP 50x50 (G1 Method)']['MAE']}")

# 4. G1 Method: Support Vector Machine (SVR with RBF kernel)
print("\n[Orig 4] Fitting G1 Method: Support Vector Machine (SVR RBF)...")
# Using sample of 4000 for fast convergence on CPU
svr_o = SVR(kernel='rbf', C=10.0, epsilon=0.5, max_iter=4000)
svr_o.fit(X_train_o_scaled[:4000], y_train_o.iloc[:4000])
p_svr_o = svr_o.predict(X_test_o_scaled)
r2_svr = r2_score(y_test_o, p_svr_o)
orig_results['Support Vector Machine SVR (G1 Method)'] = {
    'R2': round(float(r2_svr), 4),
    'MAE': round(float(mean_absolute_error(y_test_o, p_svr_o)), 2),
    'RMSE': round(float(np.sqrt(mean_squared_error(y_test_o, p_svr_o))), 2),
    'MAPE': round(calc_mape(y_test_o, p_svr_o), 2),
    'Flag': 'NORMAL' if r2_svr >= 0 else '⚠️ FLAGGED (R² < 0)'
}
print(f"  -> R2: {r2_svr:.4f}, MAE: {orig_results['Support Vector Machine SVR (G1 Method)']['MAE']}")

# 5. Our Project Model: Stacked Hybrid Ensemble (ETR + XGB + HistGBM)
print("\n[Orig 5] Evaluating Our Stacked Hybrid Ensemble (Best_Model.pkl)...")
with open('c:/Machine learning/Best_Model.pkl', 'rb') as f:
    best_blended = pickle.load(f)
p_best_o = best_blended.predict(X_test_o)
r2_best = r2_score(y_test_o, p_best_o)
orig_results['Our Model: Stacked Hybrid Ensemble (ETR + XGB + HistGBM)'] = {
    'R2': round(float(r2_best), 4),
    'MAE': round(float(mean_absolute_error(y_test_o, p_best_o)), 2),
    'RMSE': round(float(np.sqrt(mean_squared_error(y_test_o, p_best_o))), 2),
    'MAPE': round(calc_mape(y_test_o, p_best_o), 2),
    'Flag': 'NORMAL' if r2_best >= 0 else '⚠️ FLAGGED (R² < 0)'
}
print(f"  -> R2: {r2_best:.4f}, MAE: {orig_results['Our Model: Stacked Hybrid Ensemble (ETR + XGB + HistGBM)']['MAE']}")


# ==============================================================================
# PART 2: 200-SAMPLE PIEDRA SANTA URBAN COHORT DATASET
# ==============================================================================
print("\n>>> Loading and Preparing 200-Sample Piedra Santa Dataset...")
df_p = pd.read_csv('c:/Machine learning/paper_dataset.csv')
p_target = 'Energy Consumption (kW)'
p_features = [c for c in df_p.columns if c != p_target]

X_p = df_p[p_features]
y_p = df_p[p_target]

# Min-Max Normalization as in G1 paper
scaler_p = MinMaxScaler()
X_p_scaled = scaler_p.fit_transform(X_p)

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_p_scaled, y_p, test_size=0.30, random_state=42
)
print(f"200-Sample Dataset Partition: Train={len(y_train_p)}, Test={len(y_test_p)}")

paper_models_dir = 'c:/Machine learning/paper_models'
with open(f'{paper_models_dir}/linear_regression.pkl', 'rb') as f:
    p_m_lr = pickle.load(f)
with open(f'{paper_models_dir}/support_vector_machine.pkl', 'rb') as f:
    p_m_svm = pickle.load(f)
with open(f'{paper_models_dir}/random_forest.pkl', 'rb') as f:
    p_m_rf = pickle.load(f)
with open(f'{paper_models_dir}/deep_neural_network.pkl', 'rb') as f:
    p_m_mlp = pickle.load(f)
with open(f'{paper_models_dir}/xgboost.pkl', 'rb') as f:
    p_m_xgb = pickle.load(f)
with open(f'{paper_models_dir}/team_ensemble.pkl', 'rb') as f:
    p_m_ens = pickle.load(f)

# Also train Our Original Architecture (ExtraTrees + XGBoost + HistGBM) directly on the 200 data!
print("\nFitting Our Original Ensemble Architecture (ETR + XGB + HistGBM) on the 200 data...")
etr_200 = ExtraTreesRegressor(n_estimators=100, max_depth=4, min_samples_split=3, random_state=42)
etr_200.fit(X_train_p, y_train_p)

xgb_200 = xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42)
xgb_200.fit(X_train_p, y_train_p)

hgb_200 = HistGradientBoostingRegressor(max_iter=100, max_depth=3, random_state=42)
hgb_200.fit(X_train_p, y_train_p)

# Stack with positive Ridge
meta_200_tr = np.column_stack([etr_200.predict(X_train_p), xgb_200.predict(X_train_p), hgb_200.predict(X_train_p)])
meta_200_te = np.column_stack([etr_200.predict(X_test_p), xgb_200.predict(X_test_p), hgb_200.predict(X_test_p)])
ridge_200 = Ridge(positive=True, alpha=1.0)
ridge_200.fit(meta_200_tr, y_train_p)
p_our_ensemble_on_200 = ridge_200.predict(meta_200_te)
r2_our_on_200 = r2_score(y_test_p, p_our_ensemble_on_200)

paper_200_results = {}

models_200 = {
    'Support Vector Machine SVR (G1 Method)': (p_m_svm.predict(X_test_p), 'G1'),
    'Linear Regression OLS (G1 Method)': (p_m_lr.predict(X_test_p), 'G1'),
    'Random Forest Regressor (G1 Method)': (p_m_rf.predict(X_test_p), 'G1'),
    'Deep Neural Network MLP (G1 Method)': (p_m_mlp.predict(X_test_p), 'G1'),
    'XGBoost Regressor': (p_m_xgb.predict(X_test_p), 'Intermediate'),
    'Our Model: Stacked Tree Ensemble (ETR + XGB + HistGBM)': (p_our_ensemble_on_200, 'OurModel'),
    'Our Model: Regularized Stacked Ensemble (SVR + LR + XGB)': (p_m_ens.predict(scaler_p.inverse_transform(X_test_p)), 'OurModel')
}

for m_name, (preds, origin) in models_200.items():
    r2 = r2_score(y_test_p, preds)
    mae = mean_absolute_error(y_test_p, preds)
    rmse = np.sqrt(mean_squared_error(y_test_p, preds))
    mape = calc_mape(y_test_p, preds)
    is_flagged = r2 < 0
    paper_200_results[m_name] = {
        'R2': round(float(r2), 4),
        'MAE': round(float(mae), 4),
        'RMSE': round(float(rmse), 4),
        'MAPE': round(float(mape), 2),
        'Origin': origin,
        'Flag': '⚠️ FLAGGED (R² < 0)' if is_flagged else 'NORMAL (Passed)',
        'Recommendation': 'Discard for micro-sample deployment; fallback to regularized/linear model.' if is_flagged else 'Safe for deployment in low-sample regime.'
    }
    print(f"[{m_name}] R2: {r2:.4f} | MAE: {mae:.4f} kW | Status: {paper_200_results[m_name]['Flag']}")

# ==============================================================================
# SAVE COMPLETE RESULTS
# ==============================================================================
all_experimental_data = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'experiment_1_original_dataset': {
        'dataset_name': 'UCI Appliances Energy Telemetry',
        'records': len(df_clean),
        'features': len(feature_names),
        'target': 'Appliances (Wh)',
        'results': orig_results
    },
    'experiment_2_small_dataset': {
        'dataset_name': 'Piedra Santa Urban Micro-Cohort (G1 Dataset)',
        'records': len(df_p),
        'features': len(p_features),
        'target': 'Energy Consumption (kW)',
        'results': paper_200_results
    }
}

with open('c:/Machine learning/cross_experiments_results.json', 'w') as f:
    json.dump(all_experimental_data, f, indent=4)

print("\n✓ Experiments complete! Results saved to cross_experiments_results.json")
