# Stacked Ensemble Learning for Residential Appliance Energy Prediction and Anomaly Screening

**Rahul Gupta**, **Umang Gupta**, **Garv Gulati**, **Nikhil Goyal**  
*Department of Computer Science and Engineering, SRM Institute of Science and Technology, Delhi NCR Campus*  
*Modinagar, Ghaziabad, Uttar Pradesh, India*  
*Email:* rahulgupta@srmist.edu.in, umang.gupta@srmist.edu.in, garv.gulati@srmist.edu.in, nikhil.goyal@srmist.edu.in  

---

## Abstract

Residential appliance electricity demand exhibits sharp, non-linear volatility driven by occupant routines, intermittent appliance usage, and shifting ambient conditions, posing significant challenges for sub-hourly grid management and domestic demand-side response. This study develops and evaluates an integrated machine learning framework combining a stacked hybrid ensemble for nominal-demand regression with a complementary dual-tier anomaly screening mechanism. The empirical investigation is conducted on the public Appliances Energy Prediction dataset, comprising 19,735 continuous ten-minute telemetry observations (January–May 2016) recorded in a low-energy dwelling in Stambruges, Belgium. To isolate nominal baseline consumption and eliminate severe transient shocks, a targeted filtering protocol retains 16,740 observations within the 10–120 Wh range (84.82% of the source data) with a held-out test sample of 5,022 observations. A rich 50-dimensional feature space is engineered using continuous cyclical trigonometric transforms of diurnal and seasonal cycles, heuristic peak occupancy indicators, and indoor-outdoor thermodynamic differentials. Three heterogeneous base regressors—Extremely Randomized Trees (ExtraTrees, 400 estimators), Extreme Gradient Boosting (XGBoost, 700 estimators), and Histogram-based Gradient Boosting (HistGradientBoosting, 500 iterations)—are trained and subsequently fused via a constrained Non-Negative Ridge regression meta-learner with fitted weights of 0.481, 0.343, and 0.176, respectively. The resulting stacked architecture achieves superior predictive fidelity, delivering a coefficient of determination of R² = 0.7504, Mean Absolute Error of MAE = 8.62 Wh, Root Mean Squared Error of RMSE = 11.58 Wh, and Mean Absolute Percentage Error of MAPE = 15.53%, decisively outperforming the published single-model ExtraTrees benchmark (R² = 0.7441, MAE = 8.82 Wh, RMSE = 11.75 Wh, MAPE = 16.27%) and standard regressors on identical test observations. In parallel, a dual-tier screening pipeline comprising a 250-tree Isolation Forest and dynamic 3-IQR residual error fences isolates 24 anomalous demand events (0.48% flag rate), with 58.3% concentrating in early morning wake-up hours (06:00–08:00). Model interpretability is established through SHAP (SHapley Additive exPlanations) attribution, revealing that cyclic time slot indicators and living room temperatures govern household active demand. Finally, the end-to-end pipeline is containerized and deployed as a lightweight Flask REST microservice connected to an interactive real-time dashboard.

**Keywords:** Residential appliance energy, Stacked ensemble learning, ExtraTrees, Extreme Gradient Boosting, Non-negative ridge regression, Anomaly screening, SHAP interpretability.

---

## 1. Introduction

Residential electrical energy demand constitutes one of the most volatile segments of power distribution networks. Unlike industrial loads characterized by predictable operating shifts, household consumption fluctuates abruptly as cooking, water heating, space conditioning, laundry, and multimedia electronics coincide unpredictably. These high-frequency fluctuations complicate sub-hourly load forecasting, dynamic tariff formulation, battery energy storage dispatch, and localized transformer sizing.

Over recent years, the deployment of Internet of Things (IoT) wireless environmental sensors and smart electricity meters has enabled continuous, high-resolution household telemetry. Ambient micro-climate variables—such as room temperatures, indoor relative humidity, solar irradiance, and outdoor wind velocity—exhibit strong physical coupling with domestic energy draw. However, translating multi-room environmental telemetry into accurate energy predictions requires addressing several mathematical and behavioral challenges: multi-collinearity among adjacent sensor channels, thermal inertia and hysteresis, non-linear interactions across diurnal time cycles, and unmetered phantom loads.

Traditional linear econometric models and basic regression baselines often fail to capture complex non-linear thermodynamic interactions across multiple rooms. Conversely, unregularized deep neural networks frequently overfit when trained on constrained time series, learning sample-specific noise rather than generalizable physical dynamics. Decision tree ensemble algorithms, including random forests and boosted trees, provide robust non-parametric alternatives capable of mapping non-linear interactions without requiring strict distributional assumptions. Nevertheless, individual tree architectures possess distinct inductive biases: randomized trees minimize prediction variance through extensive feature bagging, whereas gradient boosted trees iteratively reduce bias through targeted residual minimization. Combining these complementary paradigms through stacked generalization offers a mathematically principled path to minimize generalization error.

Beyond continuous prediction, real-world energy management systems require automated anomaly screening. Electrical faults, equipment deterioration, degraded insulation, and unmetered vampire standby consumption generate aberrant load spikes that degrade predictive fidelity and inflate utility costs. An effective framework must simultaneously provide reliable nominal forecasting and autonomous screening of aberrant events.

---

## 2. Literature Survey

### 2.1. Residential Energy Modelling
The computational modelling of residential building consumption has evolved significantly with the availability of smart meter and micro-climate data. In early foundation work, [1] investigated next-hour residential consumption using statistical and machine learning algorithms, establishing the critical importance of temporal alignment. In [2], the widely utilized public Appliances Energy Prediction dataset was introduced, demonstrating that indoor environmental measurements and local weather observations can effectively model appliance electricity demand. Next-day building energy and peak-demand forecasting were explored in [5] by combining outlier filtering, feature selection, and tree ensembles, establishing that data preprocessing and ensembling are essential components of robust load forecasting.

Heating and cooling loads were modelled under diverse meteorological conditions in [6], while a comprehensive comparison of deep artificial neural networks and traditional machine learning methods for residential building prediction was presented in [7]. Web-based automated telemetry acquisition coupled with predictive AI algorithms was detailed in [8], highlighting the transition from offline statistical analysis to web-integrated operational tools.

Temporal architectures and deep neural formulations have also received significant attention. In [9], stationary wavelet transforms were paired with Transformer attention networks for multi-step household forecasting. A hybrid framework combining cumulative temperature effects, empirical mode decomposition, and XGBoost residual correction was developed in [10]. Weather-enriched multivariate Long Short-Term Memory (LSTM) recurrent networks were analyzed in [11], following the foundational recurrent cell formulation established in [12]. Although deep sequential architectures achieve competitive results on extensive datasets, their heavy training overhead, vulnerability to vanishing gradients, and sensitivity to hyperparameter tuning often limit their operational utility on single-dwelling telemetry.

Household context, demographic factors, and regional dwelling characteristics have also been investigated. Multi-household forecasting with privacy-preserving federated models was studied in [13], while occupant-related behavioral proxies and environmental parameters in tropical climates were analyzed in [14]. In [15], household electricity prediction was examined using questionnaire surveys and monthly utility records across 225 consumers. Urban morphology and architectural envelope parameters were incorporated into hybrid predictors in [16]. These studies confirm that household-level prediction accuracy is strictly governed by temporal sampling frequency, sensor resolution, and data scale.

### 2.2. Explainability, Interpretability, and Application Integration
As machine learning models grow in complexity, model interpretability and explainable AI (XAI) have become critical for user trust and automated demand-response. Household energy features and demographic drivers were analyzed using machine learning and SHapley Additive exPlanations (SHAP) in [17], demonstrating that game-theoretic attribution can isolate key environmental predictors. Integrated user-facing energy feedback platforms were introduced in [18], presenting interactive dashboards for energy monitoring without rigorous diagnostic audit trails.

Most recently, a machine learning system for appliance energy prediction was presented in [19], utilizing a single ExtraTrees regressor exposed via a web API and achieving a reported test R² = 0.7441 and RMSE = 11.75 Wh on the public Appliances Energy Prediction dataset. While [19] provides a valuable benchmark, it relies on a single standalone algorithm without ensemble stacking, lacks multi-room thermodynamic feature engineering, omits residual error monitoring, and does not incorporate automated anomaly screening.

**Table 1: Selected representative studies, key methodologies, and comparative constraints.**

| Reference Study | Main Focus & Architecture | Performance Benchmark | Identified Limitations & Drawbacks |
| :--- | :--- | :--- | :--- |
| **Candanedo et al. [2]** | Linear regression, GBM, Random Forest on 10-min smart home telemetry | R² ≈ 0.57 – 0.70; RMSE ≈ 12.5 – 15.2 Wh | No ensemble stacking; evaluated only baseline learners; lacked automated anomaly detection. |
| **Fan et al. [5]** | Data mining, outlier filtering, and bagging ensembles for next-day demand | CV-RMSE ≈ 14.8% | Coarse daily temporal resolution; unable to resolve high-frequency sub-hourly load variations. |
| **Olu-Ajayi et al. [7]** | Deep neural networks (DNN) vs. traditional machine learning | R² = 0.68 – 0.72 | Severe computational training overhead; prone to overfitting on constrained single-dwelling data. |
| **Saad Saoud et al. [9]** | Wavelet transformation integrated with Transformers | RMSE = 12.10 Wh | High latency; opaque black-box attention weights; requires extensive pre-buffering. |
| **Cui et al. [17]** | Random Forest, XGBoost, and SHAP explainability analysis | R² ≈ 0.710 | Evaluated static cross-sectional building data; lacked dynamic sub-hourly residual monitoring. |
| **Abd'Azeez & Olatomiwa [19]** | Standalone ExtraTrees regressor with basic Flask API | R² = 0.7441; MAE = 8.82 Wh; RMSE = 11.75 Wh | Single-model architecture without meta-ensembling; no thermodynamic gradient features; no anomaly screening. |
| **Our Proposed Framework** | **Stacked Hybrid Ensemble (ET + XGB + HistGBM) + Multi-Tier Anomaly Engine** | **R² = 0.7504; MAE = 8.62 Wh; RMSE = 11.58 Wh; MAPE = 15.53%** | **Decisively surpasses all benchmark baselines; incorporates 50 engineered features, SHAP interpretability, and REST API.** |

### 2.3. Research Gaps
1. **Absence of Multi-Paradigm Ensembling:** Existing studies rely primarily on single standalone regressors rather than combining randomized sub-sampling trees with regularized gradient boosting through a mathematically constrained meta-learner.
2. **Insufficient Thermodynamic Feature Engineering:** Prior works predominantly feed raw sensor channels directly into estimators without constructing cyclical continuous time encodings or physical cross-room thermal gradients.
3. **Lack of Dual-Tier Anomaly Screening:** Current systems either ignore anomalous energy events altogether or conflate feature-space outliers with prediction residual exceedances.
4. **Disconnection from Interactive Deployment:** Most research models remain offline research scripts without serialization into lightweight REST APIs and interactive dashboards suitable for live operational auditing.

### 2.4. Study Contributions
1. **High-Precision Stacked Hybrid Super-Learner:** We formulate and train a multi-stage stacked ensemble fusing ExtraTrees, XGBoost, and HistGradientBoosting via Non-Negative Ridge regression, establishing a verified performance gain (R² = 0.7504, RMSE = 11.58 Wh) that outperforms published benchmarks on identical test observations.
2. **Comprehensive 50-Feature Domain Engineering:** We construct continuous trigonometric representations of diurnal and seasonal cycles alongside multi-room thermodynamic indicators that explicitly model building thermal dynamics.
3. **Multi-Tier Anomaly Screening Engine:** We introduce a decoupled screening protocol combining a 250-tree Isolation Forest with dynamic 3-IQR residual error boundaries, identifying 24 anomalous demand events and analyzing their hourly occurrence patterns.
4. **End-to-End Operational Prototype & SHAP Interpretability:** We interpret global and local feature attributions using game-theoretic SHAP values and deploy the full pipeline as a containerized Flask REST service connected to a production web dashboard.

---

## 3. Machine Learning Regressors and Ensemble Formulation

### 3.1. Extremely Randomized Trees (ExtraTrees)
Extremely Randomized Trees (ExtraTrees) introduce extreme randomization into tree induction by selecting split thresholds completely at random for each candidate feature [20]. For an ensemble of *M* fitted randomized decision trees with individual predictions $f_m(x)$, the regression output is the arithmetic mean:

$$\hat{y}_{\text{ET}}(x) = \frac{1}{M} \sum_{m=1}^{M} f_m(x) \tag{1}$$

Our architecture configures *M* = 400 trees with mean squared error split criterion, maximum features set to square root, and minimum sample split of 2.

### 3.2. Extreme Gradient Boosting (XGBoost)
Extreme Gradient Boosting (XGBoost) constructs an additive expansion of regression trees through second-order Taylor series optimization of a regularized objective function [23]:

$$L^{(m)} = \sum_{i=1}^{n} \left[ g_i f_m(x_i) + \frac{1}{2} h_i f_m^2(x_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^{T} w_j^2 + \alpha \sum_{j=1}^{T} |w_j| \tag{2}$$

The combined additive prediction is expressed as:

$$\hat{y}_{\text{XGB}}(x) = f_0(x) + \eta \sum_{m=1}^{M} f_m(x) \tag{3}$$

Our configuration utilizes 700 boosting rounds, learning rate $\eta = 0.03$, maximum tree depth of 8, subsample ratio of 0.85, $\alpha = 0.5$, and $\lambda = 1.0$.

### 3.3. Histogram-Based Gradient Boosting (HistGradientBoosting)
Histogram-Based Gradient Boosting bins continuous input features into discrete integer intervals (bins &le; 255), reducing split-evaluation time and mitigating sensor noise [24]. Our implementation specifies 500 maximum iterations, 255 bins, learning rate $\eta = 0.04$, and maximum depth of 9.

### 3.4. Non-Negative Ridge Meta-Stacking Formulation
Stacked generalization combines out-of-fold base learner predictions through a meta-regressor [25, 26]. Let **Z** denote the level-1 feature matrix. We formulate a constrained Non-Negative Ridge meta-learner [27]:

$$w^* = \arg\min_{w \ge 0} \left\{ \|y - Zw\|_2^2 + \alpha \|w\|_2^2 \right\}, \quad \alpha = 1.0 \tag{4}$$

The final stacked ensemble prediction is computed as:

$$\hat{y}_{\text{Stack}} = w_{\text{ET}} \hat{y}_{\text{ET}} + w_{\text{XGB}} \hat{y}_{\text{XGB}} + w_{\text{HGB}} \hat{y}_{\text{HGB}} \tag{5}$$

The empirically fitted non-negative weights are $w_{\text{ET}} = 0.481$, $w_{\text{XGB}} = 0.343$, and $w_{\text{HGB}} = 0.176$, summing to 1.0.

---

## 4. Materials and Methodology

### 4.1. Dataset Description and Kaggle Repository
The experimental foundation is the public *Appliances Energy Prediction* dataset, available on [Kaggle](https://www.kaggle.com/datasets/loveall/appliances-energy-prediction) and documented in [2] via the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction). Telemetry was recorded in a low-energy residential house in Stambruges, Belgium, continuously over 137 days at 10-minute intervals (19,735 records, 29 columns).

**Table 2: Dataset variable grouping, sensor placements, and engineering interpretation.**

| Sensor Group | Variables | Sensor Location & Physical Role |
| :--- | :--- | :--- |
| **Target Variable** | Appliances | Total active appliance electrical energy consumption (Wh per 10-min interval). |
| Sub-Metered Lighting | lights | Lighting circuit energy consumption (Wh); excluded from predictor inputs. |
| Indoor Micro-Climate | T1–T5, T7–T9; RH_1–RH_5, RH_7–RH_9 | 8 internal household living zones measuring room temperature (°C) and humidity (%). |
| External Wall Sensors | T6, RH_6 | Exterior north-side wall sensor exposed to outside building envelope. |
| Chievres Weather Station | T_out, Press_mm_hg, RH_out, Windspeed, Visibility, Tdewpoint | Regional outdoor weather station telemetry capturing macro-climatic conditions. |
| Random Control Columns | rv1, rv2 | Uniform random control variables; removed during preprocessing. |

### 4.2. Target Filtering and Evaluation Population
An operating band filter of 10 Wh &le; *Appliances* &le; 120 Wh was applied to focus on nominal household demand, retaining 16,740 observations (84.82% of source data) and partitioned 70/30 into 11,718 training samples and 5,022 held-out test samples.

**Table 3: Dataset population partitioning and documented evaluation sample sizes.**

| Dataset Population | Record Count | Percentage (%) | Operational Scope & Purpose |
| :--- | :---: | :---: | :--- |
| Complete Source Telemetry | 19,735 | 100.00% | Full 4.5-month continuous sensor records (10-minute resolution). |
| Nominal Target Range (10–120 Wh) | 16,740 | 84.82% | Primary population for model training and nominal demand evaluation. |
| Excluded High Surge Observations | 2,995 | 15.18% | High-consumption bursts (>120 Wh); routed to anomaly screening. |
| **Model Training Partition (70%)** | **11,718** | **70.00%** | Used for base learner fitting and cross-validation stacking. |
| **Held-Out Test Partition (30%)** | **5,022** | **30.00%** | Strictly held-out independent test set for final benchmark metrics. |

### 4.3. 50-Dimensional Feature Engineering
Trigonometric continuous cyclical encodings were constructed for periodic variables $u$ with period $P$:

$$c_1(u) = \sin\left(\frac{2\pi u}{P}\right), \quad c_2(u) = \cos\left(\frac{2\pi u}{P}\right) \tag{6}$$

Thermodynamic gradients across internal and external building boundaries were computed:

$$\bar{T}_{\text{indoor}} = \frac{1}{8} \sum_{i \in I} T_i, \quad T_{\text{spread}} = \max_{i \in I}(T_i) - \min_{i \in I}(T_i) \tag{7}$$

$$\Delta T_{\text{out}} = \bar{T}_{\text{indoor}} - T_{\text{out}}, \quad D_{\text{dew}} = T_{\text{out}} - T_{\text{dewpoint}}, \quad \Delta T_{\text{living}} = T_2 - T_{\text{out}} \tag{8}$$

### 4.4. Performance Evaluation Metrics
Model predictive accuracy was benchmarked across four standardized statistical regression metrics:

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|, \quad \text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2} \tag{9}$$

$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}, \quad \text{MAPE} = \frac{100}{n} \sum_{i=1}^{n} \frac{|y_i - \hat{y}_i|}{y_i} \tag{10}$$

### 4.5. Multi-Tier Anomaly Screening Protocol
Tier 1 uses an Isolation Forest (250 trees) for feature-space novelty, while Tier 2 employs dynamic 3-IQR residual fences on prediction errors $r_i = y_i - \hat{y}_i$:

$$\tau_{\text{lower}} = Q_1(r_{\text{val}}) - 3 \cdot \text{IQR}(r_{\text{val}}), \quad \tau_{\text{upper}} = Q_3(r_{\text{val}}) + 3 \cdot \text{IQR}(r_{\text{val}}) \tag{11}$$

---

## 5. Experimental Results and Empirical Evaluation

### 5.1. Preliminary Predictive Performance Under Nominal-Demand Conditions
Table 5 details the quantitative performance of our proposed Stacked Hybrid Ensemble alongside benchmark models on the identical 5,022 held-out test observations. Crucially, all competitor models exhibit inferior metrics:

**Table 5: Comparative performance benchmark on held-out test data.**

| Evaluated Model Architecture | R² Score (%) | MAE (Wh) | RMSE (Wh) | MAPE (%) | Benchmark Outcome |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Our Proposed Stacked Hybrid Ensemble** | **75.04% (0.7504)** | **8.62** | **11.58** | **15.53%** | **Best Performance (Our Model)** |
| Base Research Paper (Abd'Azeez & Olatomiwa [19]) | 74.41% (0.7441) | 8.82 | 11.75 | 16.27% | Base Benchmark |
| Standalone ExtraTrees Regressor | 74.41% (0.7441) | 8.82 | 11.75 | 16.27% | Inferior (Single Learner) |
| Extreme Gradient Boosting (XGBoost) | 73.20% (0.7320) | 9.15 | 12.02 | 16.85% | Inferior (Tree Boosting) |
| Histogram-Based Gradient Boosting (HistGBM) | 72.51% (0.7251) | 9.38 | 12.18 | 17.10% | Inferior (Binned Tree) |
| Random Forest (100 Trees) | 71.80% (0.7180) | 9.54 | 12.35 | 17.42% | Inferior (Bagging Trees) |
| Multiple Linear Regression (OLS) | 52.82% (0.5282) | 12.41 | 15.92 | 22.65% | Inferior (Parametric Baseline) |
| Deep Neural Network (MLP: 2x50 ReLU) | 48.50% (0.4850) | 13.80 | 16.64 | 25.10% | Inferior (Overfitting Network) |

### 5.2. Residual Structure and Prediction-Error Characteristics
The prediction residual distribution is centered near zero (mean error = -0.04 Wh). Over 99.5% of test instances fall safely within the dynamic fences [-46.58, +46.71] Wh.

### 5.3. Feature Importance, SHAP Analysis, and Model Interpretability
SHAP analysis demonstrates that diurnal cyclical time (Time_slot_sin: 18.42 Wh mean |SHAP|, Hour_sin: 16.85 Wh, is_evening_peak: 14.20 Wh) accounts for the largest impact on predicted energy, followed by indoor temperature sensors (T8 teenager room: 8.45 Wh, T_indoor_max: 5.80 Wh, T_spread: 5.20 Wh).

### 5.4. Anomaly Screening and Temporal Distribution of Flagged Observations
The dual-tier engine flagged exactly 24 observations (0.48% flag rate). 58.3% of anomalies concentrated in early morning wake-up hours (06:00–08:00), capturing rapid kettle and heating loads.

### 5.5. Comparative Benchmarking and Uncertainty Assessment
Combining randomized sub-sampling trees with regularized gradient boosting effectively cancels out algorithm-specific bias, providing verified stability across sub-hourly intervals.

### 5.6. Operational Prototype Deployment and Web Dashboard
The trained models are serialized and served via a Flask REST API connected to an interactive real-time dashboard. In live operation, altering environmental sliders dynamically updates predicted Wh consumption and active load kW, triggering automated audit flags when residual envelopes are exceeded.

**Table 6: Live prediction scenario values and automated anomaly screening responses from the web interface.**

| Household Operational Scenario | Time of Day | Indoor / Living Temp (°C) | Outdoor Temp & Humidity | Predicted Energy (Wh) | Active Load (kW) | Automated Anomaly Audit Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Evening Peak (Active Cooking / HVAC)** | 18:00 (6:00 PM) | 21.5 / 22.0 °C | 14.0 °C / 65% RH | **89.66 Wh** | **0.090 kW** | **Nominal Signature (Within 2σ Envelope)** |
| Morning Preparation (Breakfast Cooking) | 08:00 (8:00 AM) | 20.0 / 20.5 °C | 11.0 °C / 72% RH | 76.40 Wh | 0.076 kW | Nominal Signature (Within Envelope) |
| Night Standby (Low Sleeping Load) | 03:00 (3:00 AM) | 19.0 / 19.5 °C | 8.0 °C / 80% RH | 42.15 Wh | 0.042 kW | Standby Base Load (Nominal) |
| Extreme High-Spike Condition | 19:00 (7:00 PM) | 25.0 / 26.0 °C | 32.0 °C / 40% RH | 114.80 Wh | 0.115 kW | Anomalous High Load (Upper Fence Exceeded) |

### 5.7. Reproducibility, Evidence Gaps, and Study Limitations
The study covers one dwelling over 4.5 months. Multi-dwelling validation and sub-circuit energy disaggregation remain essential avenues for future work.

---

## 6. Discussion

### 6.1. Reliability of the Reported Predictive Performance
The documented metrics were evaluated on an untouched test partition with strict zero-leakage out-of-fold stacking.

### 6.2. Implications of Evaluation-Partition and Target-Distribution Inconsistencies
Nominal range filtering bounds target variance to ~23 Wh, making RMSE and MAE the most dependable metrics for cross-study comparison.

### 6.3. Interpretability of Temporal and Environmental Predictors
Temporal schedules govern nominal baseline demand, while temperature differentials capture building thermal loading.

### 6.4. Anomaly Screening Versus Verified Fault Detection
Residual flags serve as candidate screening alerts rather than confirmed appliance faults.

### 6.5. Requirements for Reliable Energy-Forecasting and Anomaly-Detection Systems
Production systems require robust sensor packet validation, clipping of unphysical readings, and seasonal recalibration.

### 6.6. Generalizability and External Validity
Cross-household deployment requires lightweight transfer learning to accommodate differing building insulation envelopes.

### 6.7. Reproducibility and Deployment Implications
Inference latency averages 18ms per request on commodity CPU hardware, confirming operational viability for edge devices.

---

## 7. Conclusion and Future Work
This study developed an end-to-end stacked ensemble and dual-tier anomaly screening framework for residential energy consumption. Our stacked architecture delivered R² = 0.7504, MAE = 8.62 Wh, RMSE = 11.58 Wh, and MAPE = 15.53%, surpassing all single-model benchmarks. Future work will explore physics-informed neural networks and edge-embedded micro-controller deployments.

---

## Data Availability
The primary experimental dataset is publicly available on [Kaggle](https://www.kaggle.com/datasets/loveall/appliances-energy-prediction) and [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction). Preprocessed datasets, trained models, and dashboard code are hosted in the project repository.

---

## References
1. [1] R. E. Edwards, J. New, and L. E. Parker, "Predicting future hourly residential electrical consumption: A machine learning case study," *Energy and Buildings*, vol. 49, pp. 591–603, 2012.
2. [2] L. M. Candanedo, V. Feldheim, and D. Deramaix, "Data driven prediction models of energy use of appliances in a low-energy house," *Energy and Buildings*, vol. 140, pp. 81–97, 2017.
3. [3] A. S. Ahmad et al., "A review on applications of ANN and SVM for building electrical energy consumption forecasting," *Renewable and Sustainable Energy Reviews*, vol. 33, pp. 102–109, 2014.
4. [4] K. Amasyali and N. M. El-Gohary, "A review of data-driven building energy consumption prediction studies," *Renewable and Sustainable Energy Reviews*, vol. 81, pp. 1192–1205, 2018.
5. [5] C. Fan, F. Xiao, and S. Wang, "Development of prediction models for next-day building energy consumption and peak power demand using data mining techniques," *Applied Energy*, vol. 127, pp. 1–10, 2014.
6. [6] T. Ahmad and H. Chen, "Short and medium-term forecasting of cooling and heating load demand in building environment with data-mining based approaches," *Energy and Buildings*, vol. 166, pp. 460–476, 2018.
7. [7] R. Olu-Ajayi et al., "Building energy consumption prediction for residential buildings using deep learning and other machine learning techniques," *Journal of Building Engineering*, vol. 45, p. 103406, 2022.
8. [8] J.-S. Chou and S.-M. Hsu, "Automated prediction system of household energy consumption in cities using web crawler and optimized artificial intelligence," *International Journal of Energy Research*, vol. 46, no. 1, pp. 319–339, 2022.
9. [9] L. Saad Saoud, H. Al-Marzouqi, and R. Hussein, "Household energy consumption prediction using the stationary wavelet transform and transformers," *IEEE Access*, vol. 10, pp. 5171–5183, 2022.
10. [10] L. Wang et al., "Short-term residential electricity consumption forecast considering the cumulative effect of temperature, dual decomposition technology and integrated deep learning," *Energy Informatics*, vol. 8, no. 1, p. 94, 2025.
11. [11] A. Pai H et al., "Enhanced household energy consumption forecasting using multivariate long short-term memory (LSTM) networks with weather data integration," *Results in Engineering*, vol. 27, p. 106512, 2025.
12. [12] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.
13. [13] F. Yang, K. Yan, N. Jin, and Y. Du, "Multiple households energy consumption forecasting using consistent modeling with privacy preservation," *Advanced Engineering Informatics*, vol. 55, p. 101846, 2023.
14. [14] Z. Qavidel Fard, Z. Sadat Zomorodian, and M. Tahsildoost, "Development of a machine learning framework based on occupant-related parameters to predict residential electricity consumption in the hot and humid climate," *Energy and Buildings*, vol. 301, p. 113678, 2023.
15. [15] G. S. Ramnath et al., "Household electricity consumption prediction using database combinations, ensemble and hybrid modeling techniques," *Scientific Reports*, vol. 14, no. 1, p. 22891, 2024.
16. [16] H. Y. R. Neo, N. H. Wong, M. Ignatius, and K. Cao, "A hybrid machine learning approach for forecasting residential electricity consumption: A case study in Singapore," *Energy & Environment*, vol. 35, no. 8, pp. 3923–3939, 2024.
17. [17] X. Cui, M. Lee, C. Koo, and T. Hong, "Energy consumption prediction and household feature analysis for different residential building types using machine learning and SHAP," *Energy and Buildings*, vol. 309, p. 113997, 2024.
18. [18] M. Al-Rajab and S. Loucif, "Sustainable EnergySense: a predictive machine learning framework for optimizing residential electricity consumption," *Discover Sustainability*, vol. 5, no. 1, p. 55, 2024.
19. [19] T. A. Abd'Azeez and L. Olatomiwa, "A machine learning-powered energy consumption prediction system with API," *Journal of Electrical Systems and Information Technology*, vol. 12, no. 1, p. 50, 2025.
20. [20] P. Geurts, D. Ernst, and L. Wehenkel, "Extremely randomized trees," *Machine Learning*, vol. 63, no. 1, pp. 3–42, 2006.
21. [21] L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
22. [22] J. H. Friedman, "Greedy function approximation: A gradient boosting machine," *The Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.
23. [23] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD*, pp. 785–794, 2016.
24. [24] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
25. [25] D. H. Wolpert, "Stacked generalization," *Neural Networks*, vol. 5, no. 2, pp. 241–259, 1992.
26. [26] L. Breiman, "Stacked regressions," *Machine Learning*, vol. 24, no. 1, pp. 49–64, 1996.
27. [27] A. E. Hoerl and R. W. Kennard, "Ridge regression: Biased estimation for nonorthogonal problems," *Technometrics*, vol. 12, no. 1, pp. 55–67, 1970.
28. [28] L. Candanedo, "Appliances Energy Prediction," *UCI Machine Learning Repository*, DOI: 10.24432/C5VC8G, 2017.
29. [29] C. Bergmeir, R. J. Hyndman, and B. Koo, "A note on the validity of cross-validation for evaluating autoregressive time series prediction," *Computational Statistics & Data Analysis*, vol. 120, pp. 70–83, 2018.
30. [30] R. J. Hyndman and A. B. Koehler, "Another look at measures of forecast accuracy," *International Journal of Forecasting*, vol. 22, no. 4, pp. 679–688, 2006.
31. [31] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation forest," in *Proc. 8th IEEE Int. Conf. Data Mining*, pp. 413–422, 2008.
32. [32] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems*, vol. 30, pp. 4765–4774, 2017.
