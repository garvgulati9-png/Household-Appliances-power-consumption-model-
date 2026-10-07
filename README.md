# ⚡ Residential Appliance Energy Prediction & Anomaly Diagnostics Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask Microservice](https://img.shields.io/badge/backend-Flask%20REST%20API-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20XGBoost%20%7C%20SHAP-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![R2 Score](https://img.shields.io/badge/R%C2%B2-0.7504-brightgreen.svg)](#-model-performance--benchmarks)

An end-to-end Machine Learning research system and full-stack analytics platform for **sub-hourly residential energy demand forecasting** and **dual-tier anomaly screening**. 

Based on high-frequency IoT environmental telemetry (19,735 observations from Stambruges, Belgium), this project introduces a **Stacked Hybrid Ensemble (ExtraTrees + XGBoost + HistGradientBoosting)** fused via a Non-Negative Ridge meta-learner, coupled with an **Isolation Forest + 3-IQR residual error screening engine**.

---

## 👥 Authors & Academic Affiliation

**Rahul Gupta**, **Umang Gupta**, **Garv Gulati**, **Nikhil Goyal**  
*Department of Computer Science and Engineering, SRM Institute of Science and Technology, Delhi NCR Campus*  
*Modinagar, Ghaziabad, Uttar Pradesh, India*  
*Contact:* [garvgulati@srmist.edu.in](mailto:garvgulati@srmist.edu.in)

---

## 📌 Key Highlights & Features

- **🏆 Outperforms Academic Baselines:** Achieves **$R^2 = 0.7504$**, **$MAE = 8.62\text{ Wh}$**, and **$RMSE = 11.58\text{ Wh}$**, outperforming the single-regressor ExtraTrees benchmark ($R^2 = 0.7441$, $MAE = 8.82\text{ Wh}$, $RMSE = 11.75\text{ Wh}$).
- **🧠 50 Engineered Domain Features:** Captures diurnal cycles (sine/cosine transforms), thermal gradients (indoor-outdoor differentials, dew point depression), and occupancy proxies.
- **🛡️ Dual-Tier Anomaly Screening:** 
  1. **Tier 1:** 250-tree unsupervised Isolation Forest for multi-dimensional outlier isolation.
  2. **Tier 2:** Dynamic 3-IQR statistical residual fences ([-46.58 Wh, +46.71 Wh]) flagging abnormal consumption spikes.
- **🔍 Explainable AI (XAI):** Full SHAP (SHapley Additive exPlanations) attribution to verify physical and thermodynamic feature dependencies.
- **💻 Full-Stack Interactive Web Platform:** Production-grade web interface featuring real-time interactive energy prediction, dynamic appliance telemetry sliders, live anomaly diagnostics, and instant PDF/Word research exports.

---

## 📊 Model Performance & Benchmarks

### Primary Evaluation (Hold-out Test Set: 5,022 Samples)

| Architecture | $R^2$ Score | MAE (Wh) | RMSE (Wh) | MAPE (%) |
| :--- | :---: | :---: | :---: | :---: |
| Linear Regression Baseline | 0.3210 | 14.85 | 19.32 | 26.40% |
| Support Vector Machine (SVM) | 0.5420 | 12.10 | 16.05 | 21.80% |
| Multi-Layer Perceptron (DNN) | 0.6850 | 9.94 | 13.20 | 18.25% |
| Standalone Random Forest | 0.7180 | 9.35 | 12.42 | 17.10% |
| Published Benchmark (*Abd'Azeez & Olatomiwa, 2023*) | 0.7441 | 8.82 | 11.75 | 16.27% |
| **Our Proposed Stacked Hybrid Ensemble** | **0.7504** | **8.62** | **11.58** | **15.53%** |

*Meta-learner weights: ExtraTrees (0.481) + XGBoost (0.343) + HistGradientBoosting (0.176).*

---

## 📁 Repository Structure & Folders

```text
├── frontend/                                   # Interactive Web Platform & REST API
│   ├── index.html                             # Responsive Glassmorphic Dashboard UI
│   ├── styles.css                             # Custom styles, responsive grid, animations
│   ├── app.js                                 # Client-side state, chart rendering, API fetch
│   ├── server.py                              # Flask REST microservice for live inference
│   ├── package.json                           # Frontend package definition & npm scripts
│   ├── package-lock.json                      # Validated lockfile
│   └── assets/                                # UI image assets and slideshows
│
├── notebooks/                                 # Jupyter Notebooks & Experimental Work
│   ├── EDA.ipynb                              # Exploratory data analysis notebook
│   ├── EDA_new.ipynb                          # Extended feature correlation analysis
│   ├── Household_Energy_Basics_and_Anomaly_Guide.ipynb # Anomaly detection tutorial
│   ├── Household_Energy_Prediction_Final.ipynb# Final end-to-end model notebook
│   └── paper_colab.ipynb                      # Google Colab replication notebook
│
├── docs/                                      # Academic Papers, Presentations & Reports
│   ├── Research_Paper_Residential_Energy_Prediction.md   # Complete Academic Paper (MD)
│   ├── Research_Paper_Residential_Energy_Prediction.pdf  # Compiled Research Paper (PDF)
│   ├── Household_Power_Consumption_Final_Research_Paper.docx # Word Publication Manuscript
│   ├── Household_Power_Consumption_Final_Research_Paper.pdf  # Camera-ready Publication PDF
│   ├── Household_Power_Consumption_Final_Research_Paper.html # Web-friendly Paper HTML
│   ├── Household_Power_Consumption_Project_Review.pptx    # Review Presentation Deck
│   ├── Household_Power_Consumption_Prediction_using_ML.pptx # ML Architecture Slide Deck
│   ├── Household_Power_Consumption_Team_Manual.docx       # Project Team Manual
│   ├── G1_vs_OurModel_Comparative_Report.pdf  # Benchmark comparative report
│   └── extracted_files/                       # Reference materials and walkthroughs
│
├── data/                                      # Smart Home & Benchmark Datasets
│   ├── household_power.csv                    # Processed smart home telemetry (19k records)
│   ├── paper_dataset.csv                      # Comparative benchmark dataset
│   ├── KAG_Appliance_energydata.json          # 10-minute IoT raw dataset
│   ├── cross_experiments_results.json         # Cross-model validation metrics
│   └── paper_results_metadata.json            # Comparative performance metadata
│
├── scripts/                                   # Automation, Training & Pipeline Utilities
│   ├── train_paper_models.py                  # Multi-model training and serialization
│   ├── run_cross_experiments.py               # Cross-dataset validation suite
│   ├── run_prediction.py                      # CLI inference tool
│   ├── test_pipeline.py                       # Pipeline test suite
│   ├── build_publication_docx.py              # Word publication generator
│   └── generate_final_project_paper_pdf.py    # Automated paper PDF generator
│
├── paper_models/                              # Serialized Baseline ML Models
│   ├── deep_neural_network.pkl                # Multi-Layer Perceptron regressor
│   ├── extra_trees.pkl                        # Extremely Randomized Trees estimator
│   ├── isolation_forest.pkl                   # Unsupervised anomaly detector (250 trees)
│   ├── linear_regression.pkl                  # Baseline linear regressor
│   ├── random_forest.pkl                      # Random Forest model
│   ├── scaler.pkl                             # Fitted StandardScaler preprocessor
│   ├── support_vector_machine.pkl             # SVR model
│   ├── team_ensemble.pkl                      # Stacked ensemble pipeline artifact
│   └── xgboost.pkl                            # Gradient boosted trees model
│
├── paper_plots/                               # Publication Figures & Analytics
│   ├── fig1_consumption_histogram.png        # Energy consumption distribution
│   ├── fig2_temp_vs_consumption_scatter.png   # Micro-climate temperature regression
│   ├── fig3_performance_metrics_comparison.png# Cross-model accuracy bar charts
│   ├── fig4_projections_2026_2030.png         # Long-term forecasting projections
│   ├── fig5_correlation_heatmap.png           # Feature correlation matrix
│   └── fig6_anomaly_distribution.png          # Temporal distribution of anomalies
│
├── plots/                                     # Diagnostic & Verification Visualizations
│   ├── actual_vs_predicted.png                # Parity plots
│   ├── anomaly_scatter.png                    # Anomaly distribution across time
│   ├── feature_importance.png                 # Gini & permutation feature rankings
│   ├── hourly_anomaly_distribution.png        # Diurnal anomaly histograms
│   ├── model_comparison_bar.png               # Benchmark comparisons
│   ├── residual_analysis.png                  # Error distribution and Q-Q plots
│   ├── shap_summary.png                       # SHAP game-theoretic feature attribution
│   └── website_ui.png                         # Screenshot of interactive dashboard
│
├── Best_Model.pkl                             # Primary Stacked Hybrid Ensemble Model (Git-LFS)
├── Anomaly_Detector.pkl                       # Primary Isolation Forest Anomaly Pipeline
├── model_metadata.json                        # Primary model metrics, features, thresholds
├── pipeline_models.py                         # Model class wrappers for unpickling
├── requirements.txt                           # Python dependencies
└── README.md                                  # Project overview and documentation
```

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/garvgulati9-png/Household-Appliances-power-consumption-model-.git
cd Household-Appliances-power-consumption-model-
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
# Core dependencies:
# pip install numpy pandas scikit-learn xgboost flask shap matplotlib seaborn
```

### 3. Launch the Interactive Dashboard & REST API
```bash
python frontend/server.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🔌 REST API Endpoints

The Flask microservice exposes real-time endpoints for programmatic load forecasting:

### `POST /api/predict`
Executes real-time inference using the primary Stacked Hybrid Ensemble.
```json
{
  "features": {
    "T1": 19.89,
    "RH_1": 47.596,
    "T2": 19.2,
    "RH_2": 44.79,
    "T3": 19.79,
    "RH_3": 44.73,
    "T_out": 6.6,
    "Press_mm_hg": 733.5,
    "RH_out": 92.0,
    "Windspeed": 7.0,
    "Hour": 17,
    "Minute": 0
  }
}
```
**Response:**
```json
{
  "predicted_consumption_wh": 78.45,
  "anomaly_flag": false,
  "confidence_interval": [72.10, 84.80],
  "model_used": "Stacked Hybrid Ensemble (ExtraTrees + XGBoost + HistGBM)"
}
```

### `GET /api/benchmark-results`
Returns comparative accuracy scores across all 7 evaluated architectures.

---

## 📜 Academic Research Paper

The complete scientific paper detailing mathematical formulations, feature derivations, cross-validation protocols, and ablation experiments is available in multiple formats:
- **Markdown:** [`docs/Research_Paper_Residential_Energy_Prediction.md`](docs/Research_Paper_Residential_Energy_Prediction.md)
- **PDF (IEEE Format):** [`docs/Household_Power_Consumption_Final_Research_Paper.pdf`](docs/Household_Power_Consumption_Final_Research_Paper.pdf)
- **Word Manuscript:** [`docs/Household_Power_Consumption_Final_Research_Paper.docx`](docs/Household_Power_Consumption_Final_Research_Paper.docx)

---

## 🤝 Citation & Acknowledgements

If you use this work, models, or datasets in your academic research, please cite:

```bibtex
@article{gupta2026residentialenergy,
  title={Stacked Ensemble Learning for Residential Appliance Energy Prediction and Anomaly Screening},
  author={Gupta, Rahul and Gupta, Umang and Gulati, Garv and Goyal, Nikhil},
  journal={Department of Computer Science and Engineering, SRM Institute of Science and Technology},
  year={2026}
}
```
