import os
import sys
import json
import pickle
import numpy as np
import pandas as pd

sys.path.insert(0, 'c:/Machine learning')
from pipeline_models import TeamEnsemblePipeline

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_pipeline():
    print("==================================================")
    print("STARTING COMPREHENSIVE PIPELINE VERIFICATION")
    print("==================================================")

    # 1. Dataset Verification
    print("\n[Test 1] Verifying paper_dataset.csv...")
    ds_path = 'c:/Machine learning/paper_dataset.csv'
    assert os.path.exists(ds_path), "paper_dataset.csv missing!"
    df = pd.read_csv(ds_path)
    assert df.shape == (200, 10), f"Expected shape (200, 10), got {df.shape}"
    assert 'Energy Consumption (kW)' in df.columns, "Target column missing!"
    assert df['Energy Consumption (kW)'].min() >= 0.60, "Target min out of bounds"
    assert df['Energy Consumption (kW)'].max() <= 4.35, "Target max out of bounds"
    print(f"✓ Dataset verified: {df.shape[0]} records, target mean: {df['Energy Consumption (kW)'].mean():.3f} kW.")

    # 2. Models & Scalers Verification
    print("\n[Test 2] Verifying Serialized Models in paper_models/...")
    models_dir = 'c:/Machine learning/paper_models'
    required_models = [
        'scaler.pkl', 'linear_regression.pkl', 'support_vector_machine.pkl',
        'random_forest.pkl', 'deep_neural_network.pkl', 'xgboost.pkl',
        'team_ensemble.pkl', 'isolation_forest.pkl'
    ]
    for m in required_models:
        path = os.path.join(models_dir, m)
        assert os.path.exists(path), f"Missing model file: {m}"
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            assert obj is not None, f"Failed to deserialize {m}"
    print(f"✓ All {len(required_models)} models successfully verified.")

    # 3. Model Inference Sanity Test
    print("\n[Test 3] Testing Live Model Inference...")
    with open(os.path.join(models_dir, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(models_dir, 'team_ensemble.pkl'), 'rb') as f:
        ensemble = pickle.load(f)
    with open(os.path.join(models_dir, 'support_vector_machine.pkl'), 'rb') as f:
        svm = pickle.load(f)

    dummy_raw = np.array([[100, 12.0, 21.0, 3.0, 0, 0, 1, 0, 1]]) # User 100, 12h, 21C, 3 occ, Single house, AC=1, Dev=Mod
    dummy_scaled = scaler.transform(dummy_raw)
    
    pred_svm = svm.predict(dummy_scaled)[0]
    pred_ens = ensemble.predict(dummy_raw)[0]
    
    assert 1.0 < pred_svm < 4.0, f"SVM prediction out of range: {pred_svm}"
    assert 1.0 < pred_ens < 4.0, f"Ensemble prediction out of range: {pred_ens}"
    print(f"✓ Inference successful: SVR={pred_svm:.3f} kW, Team Ensemble={pred_ens:.3f} kW.")

    # 4. Publication Figures Verification
    print("\n[Test 4] Verifying Publication Figures in paper_plots/...")
    plots_dir = 'c:/Machine learning/paper_plots'
    required_plots = [
        'fig1_consumption_histogram.png',
        'fig2_temp_vs_consumption_scatter.png',
        'fig3_performance_metrics_comparison.png',
        'fig4_projections_2026_2030.png',
        'fig5_correlation_heatmap.png',
        'fig6_anomaly_distribution.png'
    ]
    for p in required_plots:
        path = os.path.join(plots_dir, p)
        assert os.path.exists(path), f"Missing plot: {p}"
        size_kb = os.path.getsize(path) / 1024
        assert size_kb > 50, f"Plot {p} size abnormally small ({size_kb} KB)"
        print(f"  - {p} ({size_kb:.1f} KB): Verified")
    print("✓ All 6 publication figures verified.")

    # 5. Metadata & ANOVA Verification
    print("\n[Test 5] Verifying paper_results_metadata.json & ANOVA...")
    meta_path = 'c:/Machine learning/paper_results_metadata.json'
    assert os.path.exists(meta_path), "Metadata JSON missing!"
    with open(meta_path, 'r') as f:
        meta = json.load(f)
    
    assert "Garv Gulati" in meta['authors']
    assert "Umang Gupta" in meta['authors']
    assert "Nikhil Goyal" in meta['authors']
    
    f_stat = meta['anova_table']['Between groups (models)']['F']
    p_val = meta['anova_table']['Between groups (models)']['p_value']
    assert f_stat > 5.0, f"Expected F > 5.0, got {f_stat}"
    assert p_val < 0.01, f"Expected p < 0.01, got {p_val}"
    print(f"✓ Metadata verified. ANOVA F={f_stat}, p={p_val} (Statistically Significant).")

    # 6. Research Paper Verification
    print("\n[Test 6] Verifying Research Paper Manuscript...")
    paper_path = 'c:/Machine learning/Research_Paper_Residential_Energy_Prediction.md'
    assert os.path.exists(paper_path), "Research paper manuscript missing!"
    with open(paper_path, 'r', encoding='utf-8') as f:
        paper_text = f.read()
    
    assert "Garv Gulati" in paper_text
    assert "Umang Gupta" in paper_text
    assert "Nikhil Goyal" in paper_text
    assert "Abstract" in paper_text
    assert "1. Introduction" in paper_text
    assert "2. Literature Review" in paper_text
    assert "3. Materials and Methods" in paper_text
    assert "5. Experimental Results" in paper_text
    assert "6. Multi-Year Future Projections" in paper_text
    assert "7. Anomaly Diagnostics" in paper_text
    assert "References" in paper_text
    assert "Machaca-Casani" in paper_text
    print(f"✓ Research paper manuscript verified ({len(paper_text.splitlines())} lines, {len(paper_text.split())} words).")

    # 7. Flask Server & API Endpoint Testing
    print("\n[Test 7] Testing Flask API Server Endpoints...")
    sys.path.insert(0, 'c:/Machine learning/frontend')
    from server import app
    client = app.test_client()
    
    # Test /api/metadata
    r_meta = client.get('/api/metadata')
    assert r_meta.status_code == 200, f"/api/metadata returned {r_meta.status_code}"
    
    # Test /api/dataset_summary
    r_ds = client.get('/api/dataset_summary')
    assert r_ds.status_code == 200, f"/api/dataset_summary returned {r_ds.status_code}"
    assert len(r_ds.json['sample_data']) == 10
    
    # Test /api/predict POST
    r_pred = client.post('/api/predict', json={
        'time': 18,
        'temperature': 24.5,
        'occupants': 4,
        'housing_type': 'Apartment',
        'device_usage': 'Moderate',
        'ac_room': True
    })
    assert r_pred.status_code == 200, f"/api/predict returned {r_pred.status_code}"
    pred_res = r_pred.json
    assert 'predictions' in pred_res
    assert 'anomaly_diagnostics' in pred_res
    assert ('Stacked Hybrid Super-Learner' in pred_res['predictions']) or ('Team Hybrid Ensemble' in pred_res['predictions'])
    model_key = 'Stacked Hybrid Super-Learner' if 'Stacked Hybrid Super-Learner' in pred_res['predictions'] else 'Team Hybrid Ensemble'
    print(f"✓ Flask API /api/predict verified. Primary output: {pred_res['predictions'][model_key]} Wh.")

    # Test /api/predict_paper_test POST
    r_paper_pred = client.post('/api/predict_paper_test', json={
        'user_id': 100,
        'time': 18,
        'temperature': 24.5,
        'occupants': 4,
        'housing_type': 'Apartment',
        'device_usage': 'Moderate',
        'ac_room': True
    })
    assert r_paper_pred.status_code == 200, f"/api/predict_paper_test returned {r_paper_pred.status_code}"
    assert 'Cross-Dataset Ensemble' in r_paper_pred.json['predictions']
    print(f"✓ Flask API /api/predict_paper_test verified. SVR: {r_paper_pred.json['predictions']['Support Vector Machine (SVR)']} kW, Ensemble: {r_paper_pred.json['predictions']['Cross-Dataset Ensemble']} kW.")

    print("\n==================================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==================================================")

if __name__ == '__main__':
    test_pipeline()
