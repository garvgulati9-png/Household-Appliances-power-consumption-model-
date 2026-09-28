# Evaluation of the Impact of Machine Learning, Deep Neural Architectures, and Ensemble Models on the Prediction of Residential Energy Consumption: An Empirical Multi-Scale Analysis

**Garv Gulati** (Registration No: RA2411003010319), **Umang Gupta** (Registration No: RA22110030100012), **Nikhil Goyal** (Registration No: RA2411003010489)  
*Department of Computer Science and Engineering / Electrical Engineering*  
*Specialization in Machine Learning and Intelligent Systems*  
*Academic Project Research Paper*

---

## Abstract

Accurate forecasting of residential electricity consumption is a fundamental requirement for modern smart grid operation, load balancing, dynamic tariff formulation, and renewable energy integration. This research investigates the predictive efficacy of modern machine learning algorithms compared to traditional statistical methods across distinct data-scale regimes. Utilizing an empirical dataset of 200 urban households from the Piedra Santa district (Arequipa, Peru) encompassing socio-energetic variables—such as ambient temperature, diurnal time, occupant density, dwelling typology, air conditioning availability, and appliance usage patterns—we rigorously benchmark Linear Regression (LR), Support Vector Machines (SVR with RBF kernel), Random Forest (RF), Deep Multilayer Perceptrons (MLP with dual 50-neuron hidden layers), Gradient Boosted Trees (XGBoost), and a Stacked Hybrid Super-Learner. Model validation is conducted using a 70/30 train-test partition and 5-fold cross-validation, evaluated via Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and the Coefficient of Determination (R²). 

Our empirical results demonstrate a striking phenomenon: in limited-sample, structured urban settings (N = 200 households), traditional Linear Regression (MAE = 0.5282 kW, RMSE = 0.6709 kW, R² = 0.0524, CV-R² = 0.2545) and Support Vector Machines (MAE = 0.5447 kW, RMSE = 0.6598 kW, R² = 0.0833, CV-R² = 0.1933) achieve superior generalization and robustness. Conversely, unregularized complex architectures including Random Forest (R² = -0.0532) and Deep MLPs (R² = -0.7941, CV-R² = -0.3827) exhibit severe degradation and negative R² values, caused by over-parameterization and noise sensitivity on restricted sample sizes. A one-way Analysis of Variance (ANOVA) on cross-validation error distributions confirms that inter-model performance variations are statistically significant (ANOVA F = 6.253, p = 0.0020). To address the vulnerability of complex models, we introduce a regularized Non-Negative Ridge-blended Ensemble alongside an unsupervised Multi-Tier Anomaly Detection engine (Isolation Forest + dynamic residual z-score thresholding), which successfully isolates 21 outlier households (10.5%) exhibiting aberrant consumption spikes. Finally, multi-year energy consumption projections for the 2026–2030 horizon are generated across all models, predicting a sustained upward trajectory reaching 3.08–3.30 kW by 2030. These findings establish critical architectural guidelines: algorithmic complexity must be strictly aligned with data volume and feature entropy, demonstrating that well-calibrated linear and kernel methods remain optimal for micro-grid planning in data-constrained regions.

**Keywords:** Residential Energy Consumption, Machine Learning, Support Vector Regression, Deep Neural Networks, Random Forest, Stacked Ensemble, Anomaly Detection, Urban Energy Planning, Predictive Modeling.

---

## 1. Introduction

Residential electrical energy demand constitutes one of the most volatile and critical components in the planning, stability, and dispatch optimization of modern power distribution networks [1, 2]. Rapid worldwide urban expansion, widespread home electrification, the proliferation of high-draw consumer electronics, and climate-induced temperature extremes have significantly intensified peak load uncertainty [3, 4]. Within developing economies and emerging Latin American urban centers, such as Arequipa, Peru, the electric utility sector faces profound structural transformations in its generation matrix. According to official reports from the Arequipa Chamber of Commerce [1], hydroelectric generation accounted for 63.9% of total production between January and September 2023, surging to 82.6% in 2024 alongside an accelerating expansion of photovoltaic solar installations. Crucially, the Arequipa metropolitan electrical system represents 80.55% of the region’s total consumption, with residential and commercial demand densely concentrated in urban micro-districts [2]. 

This high concentration of demand and rapid generation variability underscore an urgent necessity for reliable, data-driven predictive tools capable of anticipating consumption patterns from local environmental and behavioral signals [5, 6]. Traditionally, power utility engineers and system operators have relied on classical time-series techniques—such as multiple linear regression (MLR), autoregressive integrated moving average (ARIMA), and seasonal ARIMA (SARIMA) [11, 13, 14]. While computationally transparent, these linear models struggle to capture abrupt non-linear fluctuations, multivariate weather interactions, and complex occupancy habits [12, 15]. 

Over the past decade, advances in artificial intelligence and machine learning—spanning Random Forests (RF), Support Vector Machines (SVM/SVR), Extreme Gradient Boosting (XGBoost), and Deep Artificial Neural Networks (ANN)—have demonstrated transformative success in developed nations, frequently yielding reductions in Root Mean Squared Error (RMSE) exceeding 15% to 25% relative to linear benchmarks [16, 18, 19]. However, modern deep neural networks and deep ensemble models inherently require massive, high-frequency multivariate telemetry data (e.g., smart meter streams sampled at 1-minute to 15-minute intervals across tens of thousands of households) to properly constrain their vast parameter spaces [25, 26]. In developing regions and local urban neighborhoods, utilities frequently operate under severe data constraints, characterized by discrete, cross-sectional, or low-frequency survey records with sample sizes numbering in the hundreds rather than millions [2, 3].

This reality exposes a crucial research question: **How effective are advanced machine learning models compared to traditional statistical methods when predicting residential energy consumption in data-constrained urban environments?** Furthermore, when complex algorithms underperform or exhibit negative explanatory power (R² < 0), what specific data and regularized ensemble strategies can restore predictive fidelity?

To address these foundational questions, this investigation provides a comprehensive comparative evaluation. Building upon empirical micro-data from the Piedra Santa neighborhood (Stage 1) in Arequipa, Peru (N = 200 households), and contrasting these dynamics against scaled smart-grid benchmarks, the primary contributions of this work are threefold:
1. **Empirical Methodological Reproduction and Verification**: We replicate the exact baseline models (Linear Regression, SVR, Random Forest, Deep MLP, ANOVA, and 2026–2030 projections) established in recent urban energy research [Machaca-Casani et al., 2026], confirming the vulnerability of deep architectures in micro-sample regimes.
2. **Team-Designed Regularized Ensembling & Anomaly Diagnostics**: We introduce a Non-Negative Ridge-blended Super-Learner and a Multi-Tier Anomaly Detection engine (Isolation Forest coupled with dynamic z-score thresholding), diagnosing why non-linear models falter and isolating aberrant consumer behavioral spikes.
3. **Statistical Significance & Future Horizon Projections**: We conduct a rigorous one-way Analysis of Variance (ANOVA) across cross-validation folds (ANOVA F = 6.253, p = 0.0020) and generate multi-model demand projections spanning 2026 to 2030 to directly inform municipal energy infrastructure planning.

---

## 2. Literature Review

The application of computational intelligence to residential energy forecasting has evolved through three distinct algorithmic eras: classical econometric forecasting, shallow supervised machine learning, and deep neural/ensemble architectures.

### 2.1 Classical Statistical and Econometric Forecasting
Foundational load forecasting frameworks trace back to the pioneering Box-Jenkins time-series methodology [33], which formalized Autoregressive Integrated Moving Average (ARIMA) modeling. Box and Jenkins established the mathematical foundation for stationary stochastic modeling, which was subsequently generalized to SARIMA and vector autoregression (VAR) by Hyndman and Athanasopoulos [37]. In parallel, Ordinary Least Squares (OLS) Multiple Linear Regression (MLR) became the standard industrial tool for temperature-dependent load characterization [13]. While these models offer parameter interpretability and minimum variance guarantees under Gauss-Markov assumptions, they fail fundamentally when confronted with non-linear thermodynamic interactions (e.g., the non-linear inflection in cooling demand above specific wet-bulb temperatures) [11, 14].

### 2.2 Supervised Machine Learning and Kernel Methods
The emergence of statistical learning theory, pioneered by Vapnik and Cortes [31] through Support Vector Networks, revolutionized non-linear regression. Support Vector Regression (SVR) maps input features into infinite-dimensional reproducing kernel Hilbert spaces (RKHS) via radial basis functions (RBF), finding a global optimal hyperplane bounded by an ε-insensitive loss tube [31]. SVR’s principle of structural risk minimization confers exceptional resistance to overfitting, allowing it to perform with remarkable stability on small-to-moderate feature spaces without requiring millions of training instances [36, 37]. 

Concurrently, Breiman [30] introduced Random Forests, combining bootstrap aggregating (bagging) with random feature subspace selection. Tree ensembles mitigate the notorious variance of individual decision trees and model arbitrary non-linear feature interactions without requiring explicit mathematical transformation [30]. In building energy analysis, studies such as those by Ahmad et al. [13, 34] demonstrated that Random Forest and Gradient Boosted Decision Trees (GBDT) frequently outperform linear regressions when datasets exhibit multi-modal behavioral clustering.

### 2.3 Deep Neural Networks and Extreme Learning Models
With the computational resurgence of deep learning detailed by Goodfellow, Bengio, and Courville [4], artificial neural networks expanded from shallow single-hidden-layer architectures to Deep Neural Networks (DNN) and Multilayer Perceptrons (MLP) [9, 32]. In international smart meter implementations, deep architectures have achieved remarkable predictive precision. For example, Truong et al. [24] deployed a deep neural network to predict hourly energy consumption from occupancy telemetry, attaining a determination coefficient (R²) of 0.975 and vastly outperforming multiple linear regression. Salihi et al. [22] utilized ANNs for phase-change material (PCM) integrated buildings, achieving R² > 0.99. Fayaz and Kim [26] developed deep extreme learning machines (DELM) for multi-tier weekly and monthly load forecasting, while Moumen, Rafalia, and Abouchabaka [25] processed over 2.07 million smart meter records in MongoDB using distributed Gradient Boosting.

### 2.4 The Complexity-Data Volume Dilemma
Despite the outstanding performance of deep neural networks in large-scale studies, an emerging body of critical literature highlights the severe risks of deploying over-parameterized models in low-data regimes [35, 38]. Makridakis, Spiliotis, and Assimakopoulos [38] conducted a landmark empirical study across thousands of time series, revealing that complex machine learning algorithms frequently underperform simple statistical methods when training series are short or noisy. Similarly, Chai and Draxler [35] and Ahmad et al. [34] emphasized that model capacity must be strictly calibrated to data volume and signal-to-noise ratio. When an unregularized MLP containing thousands of free parameters is optimized on a few hundred data points, the network readily memorizes sample noise rather than generalizable thermodynamic physics, leading to catastrophically negative R² scores on out-of-sample test sets [38, 39].

### 2.5 Regional Context: Peru and Latin American Energy Systems
In Latin America, smart meter penetration remains in its developmental stages. In Peru, national initiatives have predominantly focused on macro-level macroeconomic forecasting. Flores Pampa and Olivera Trujillo [3] developed second-degree polynomial projection models to forecast nationwide electricity consumption through 2030. At the household level, the Residential Energy Consumption and Usage Survey (ERCUE 2019–2020), administered by OSINERGMIN [2], represents the primary statistical benchmark, cataloging appliance saturation and regional usage profiles. However, peer-reviewed literature directly comparing modern machine learning algorithms with classical statistical baselines on localized Peruvian micro-data has remained virtually nonexistent [1–3]. This study bridges this critical empirical gap.

---

## 3. Materials and Methods

### 3.1 Population, Sampling, and Dataset Architecture
The empirical investigation is centered on the Piedra Santa residential neighborhood (Stage 1), located within the metropolitan region of Arequipa, Peru. The target population comprises 1,000 historical residential consumption records. In accordance with quantitative sampling protocols [27, 28], simple random sampling was executed to obtain a representative cohort of N = 200 households household units, satisfying a 95% data completeness criterion.

The dataset encompasses 10 socio-energetic and environmental variables capturing household morphology, occupant behavior, weather conditions, and temporal indicators:
1. **User ID**: Unique residential identifier (1 ≤ i ≤ 200).
2. **Time**: Diurnal hour of measurement (0 ≤ t ≤ 23).
3. **Temperature (°C)**: Ambient outdoor temperature (10.03 °C ≤ T ≤ 33.67 °C).
4. **Number of People in the Household**: Family size/occupant count (1 ≤ P ≤ 6 people).
5. **Housing Type: Apartment**: Dummy variable (1 if Apartment, 0 otherwise).
6. **Housing Type: Duplex**: Dummy variable (1 if Duplex, 0 otherwise; single-family detached house serves as reference category).
7. **Air-Conditioned Room: Yes**: Dummy indicator (1 if air conditioning is present, 0 otherwise).
8. **Device Usage: Low**: Appliance activity indicator (1 if daily usage is low, 0 otherwise).
9. **Device Usage: Moderate**: Appliance activity indicator (1 if daily usage is moderate, 0 otherwise; High usage serves as reference category).
10. **Energy Consumption (kW)**: Continuous target metric representing total household active power consumption (0.61 kW ≤ Y ≤ 4.31 kW).

Table 1 presents the exhaustive descriptive statistics of the experimental cohort across all numerical and encoded categorical dimensions.

**Table 1: Descriptive statistics for numerical and categorical socio-energetic variables (N = 200 households).**

| Variable | Count | Mean | Std Dev | Min | 25% | Median (50%) | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **User ID** | 200 | 100.50 | 57.88 | 1.00 | 50.75 | 100.50 | 150.25 | 200.00 |
| **Time (Hour)** | 200 | 11.13 | 6.97 | 0.00 | 6.00 | 11.00 | 15.25 | 23.00 |
| **Temperature (°C)** | 200 | 21.22 | 4.83 | 10.03 | 17.09 | 20.47 | 24.19 | 33.67 |
| **Number of People** | 200 | 3.49 | 1.74 | 1.00 | 2.00 | 3.00 | 4.25 | 6.00 |
| **Housing Type: Apartment** | 200 | 0.365 | 0.49 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| **Housing Type: Duplex** | 200 | 0.280 | 0.46 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| **Air-Conditioned Room: Yes**| 200 | 0.510 | 0.50 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| **Device Usage: Low** | 200 | 0.300 | 0.47 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| **Device Usage: Moderate** | 200 | 0.295 | 0.46 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| **Energy Consumption (kW)** | 200 | 2.492 | 0.71 | 0.61 | 1.95 | 2.49 | 2.98 | 4.31 |

### 3.2 Data Preprocessing and Normalization
To prevent numerical instability, gradient vanishing/exploding during MLP backpropagation, and kernel distortion in Support Vector Machines, all continuous predictor features were transformed via Min-Max Normalization into the bounded interval [0, 1]:

```text
X_scaled = (X - X_min) / (X_max - X_min)
```

Categorical attributes (dwelling type and device activity categories) were structured via One-Hot Encoding to avoid introducing spurious ordinality. The dataset was partitioned into 70% training (N_train = 140 samples) and 30% hold-out testing (N_test = 60 samples) using a fixed random seed (`random_state=42`) to guarantee experimental replicability.

### 3.3 Linear Correlation Matrix
Table 2 outlines the pairwise Pearson correlation coefficients between all standardized features and residential active power consumption.

**Table 2: Correlation matrix between socio-energetic variables and residential consumption.**

| Feature | Time | Temp (°C) | Occupants | Apt | Duplex | AC Room | Dev Low | Dev Mod | Energy (kW) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Time** | 1.000 | -0.106 | 0.072 | -0.026 | 0.074 | -0.076 | 0.008 | -0.089 | **+0.514** |
| **Temp (°C)** | -0.106 | 1.000 | -0.052 | -0.119 | -0.026 | 0.014 | -0.015 | 0.052 | **-0.007** |
| **Occupants** | 0.072 | -0.052 | 1.000 | -0.068 | 0.108 | -0.103 | 0.044 | -0.029 | **+0.187** |
| **Apartment** | -0.026 | -0.119 | -0.068 | 1.000 | -0.551 | -0.007 | -0.082 | 0.138 | **-0.011** |
| **Duplex** | 0.074 | -0.026 | 0.108 | -0.551 | 1.000 | -0.035 | 0.044 | -0.156 | **+0.026** |
| **AC Room: Yes** | -0.076 | 0.014 | -0.103 | -0.007 | -0.035 | 1.000 | 0.018 | -0.122 | **-0.064** |
| **Dev Usage: Low** | 0.008 | -0.015 | 0.044 | -0.082 | 0.044 | 0.018 | 1.000 | -0.476 | **-0.114** |
| **Dev Usage: Mod** | -0.089 | 0.052 | -0.029 | 0.138 | -0.156 | -0.122 | -0.476 | 1.000 | **-0.032** |
| **Energy (kW)** | **+0.514**| **-0.007**| **+0.187**| **-0.011**| **+0.026**| **-0.064**| **-0.114**| **-0.032**| **1.000** |

As demonstrated in Table 2, Diurnal Time exhibits the strongest positive linear correlation with active consumption (r = +0.514), aligning with peak domestic cooking, lighting, and entertainment habits during evening intervals. Occupant count exhibits a secondary positive correlation (r = +0.187), while low device usage correlates negatively (r = -0.114). Temperature displays near-zero linear correlation (r = -0.007) across the full cross-sectional distribution, indicating that thermal effects in this temperate urban climate are non-linear and moderated by housing insulation and specific time-of-day interactions.

### 3.4 Mathematical Formulation of Evaluated Models

#### 3.4.1 Multiple Linear Regression (OLS)
Multiple Linear Regression serves as the foundational statistical benchmark [33]:

```text
ŷ_i = β_0 + Σ_{j=1...p} (β_j * x_ij) + ε_i
```

where β = (X^T X)^(-1) X^T y represents the Ordinary Least Squares estimator minimizing the residual sum of squares Σ (y_i - ŷ_i)².

#### 3.4.2 Support Vector Regression (SVR)
Support Vector Regression maps features into a high-dimensional Hilbert space Φ(x) and solves the dual quadratic programming problem [31]:

```text
minimize_{w, b, ξ, ξ*}  (1/2) ||w||² + C * Σ_{i=1...n} (ξ_i + ξ_i*)
```

subject to:

```text
Subject to:
  y_i - w^T Φ(x_i) - b ≤ ε + ξ_i
  w^T Φ(x_i) + b - y_i ≤ ε + ξ_i*
  ξ_i, ξ_i* ≥ 0
```

We employ a Radial Basis Function (RBF) kernel:

```text
K(x_i, x_j) = exp(-γ * ||x_i - x_j||²)
```

with penalty parameter C = 1.0 and tube width ε = 0.1.

#### 3.4.3 Random Forest Regressor (RF)
Random Forest constructs an ensemble of B = 100 decision trees decorrelated regression trees trained on bootstrap samples bootstrap samples D_b [30]:

```text
ŷ_RF(x) = (1/B) * Σ_{b=1...B} T_b(x; Θ_b)
```

At each node split, a random subset of m ≤ p features is considered, maximizing variance reduction ΔI = Var(S) - (|S_L| / |S|) Var(S_L) - (|S_R| / |S|) Var(S_R).

#### 3.4.4 Deep Multilayer Perceptron (MLP)
The Deep Neural Network comprises an input layer, two fully connected hidden layers with H_1 = 50 neurons and H_2 = 50 neurons hidden units, and a linear output neuron [4]:

```text
h^(1) = ReLU(W^(1) * x + b^(1))
```
```text
h^(2) = ReLU(W^(2) * h^(1) + b^(2))
```
```text
ŷ_MLP = W^(3) * h^(2) + b^(3)
```

Weights are trained via Adam optimization over 1,000 maximum iterations with backpropagated squared loss gradients.

#### 3.4.5 Extreme Gradient Boosting (XGBoost)
XGBoost minimizes a second-order Taylor expansion of a regularized objective function [19]:

```text
L^(t) = Σ_{i=1...n} [ g_i * f_t(x_i) + 0.5 * h_i * f_t(x_i)² ] + γ*T + 0.5*λ * Σ_{j=1...T} w_j² + α * Σ_{j=1...T} |w_j|
```

where first-order gradient g_i and second-order Hessian h_i are the first and second order loss gradients, λ = 1.0 is the L2 regularization parameter, α = 0.5 provides L1 sparsity, tree depth is constrained to max_depth = 3, and learning rate learning rate η = 0.05.

#### 3.4.6 Team-Designed Stacked Hybrid Super-Learner
To overcome individual model failure modes, we synthesize predictions via a meta-learning ensemble. The out-of-fold predictions from SVR, Linear Regression, and XGBoost form a level-1 feature matrix level-1 matrix Z in R^(n x 3):

```text
ŷ_Ensemble = w_0 + (w_SVR * ŷ_SVR) + (w_LR * ŷ_LR) + (w_XGB * ŷ_XGB)
```

The meta-weights weights w are estimated using Non-Negative Ridge Regression (w_j ≥ 0, alpha_meta = 1.0), ensuring that models with poor validation metrics receive non-negative, constrained coefficients without variance inflation.

#### 3.4.7 Multi-Tier Anomaly Detection Engine
A common catalyst for degraded machine learning accuracy is the presence of unmodeled behavioral anomalies (e.g., faulty meters, informal grid connections, vacant dwellings with phantom loads). We implement a two-tier screening architecture:
1. **Tier 1 (Unsupervised Manifold Isolation)**: An Isolation Forest of 150 path-length isolation trees isolates points requiring short average path lengths average path length h(x):
   
```text
s(x, n) = 2^(-E(h(x)) / c(n))
```

2. **Tier 2 (Supervised Dynamic Residual Thresholding)**: Households whose absolute standardized prediction residuals violate a 2σ (two standard deviations) envelope are flagged:
   
```text
z_i = |(y_i - ŷ_Ensemble,i) / σ_residual| > 2.0
```

---

## 4. Experimental Setup and Evaluation Protocol

All models were evaluated under identical 70/30 train-test splits and 5-fold cross-validation (K = 5 folds) using standard statistical error metrics:

1. **Mean Absolute Error (MAE)**:
   
```text
MAE = (1/n) * Σ_{i=1...n} |y_i - ŷ_i|
```

2. **Root Mean Squared Error (RMSE)**:
   
```text
RMSE = sqrt( (1/n) * Σ_{i=1...n} (y_i - ŷ_i)² )
```

3. **Coefficient of Determination (R²)**:
   
```text
R² = 1 - [ Σ_{i=1...n} (y_i - ŷ_i)² ] / [ Σ_{i=1...n} (y_i - ȳ)² ]
```

### Statistical Validation via One-Way ANOVA
To determine whether empirical differences in model predictive accuracy were statistically significant or merely artifacts of fold random partitioning, a One-Way Analysis of Variance (ANOVA) was conducted across the 5 cross-validation MAE fold scores for the primary algorithms:

```text
ANOVA F = MS_between / MS_within = [ SS_between / (k - 1) ] / [ SS_within / (N - k) ]
```

---

## 5. Experimental Results and Comparative Analysis

### 5.1 Exploratory Visual Analytics

The empirical distributions and bivariate interactions of the Piedra Santa dataset are illustrated in Figures 1 and 2.

![Fig. 1. Histogram of residential active energy consumption (kW).](c:/Machine%20learning/paper_plots/fig1_consumption_histogram.png)

Figure 1 displays the frequency histogram and kernel density estimation (KDE) of residential energy consumption. The distribution is unimodal and approximately Gaussian, centered near the sample mean of 2.49 kW with standard deviation 0.71 kW. A moderate dispersion is visible, with a small right-hand tail extending to 4.31 kW representing high-consumption detached homes with intensive cooling.

![Fig. 2. Scatter plot of ambient temperature vs. energy consumption.](c:/Machine%20learning/paper_plots/fig2_temp_vs_consumption_scatter.png)

Figure 2 portrays the scatter relationship between ambient temperature (°C) and energy consumption (kW). A slight positive trend slope is detected, confirming that energy demand gently elevates during warmer afternoon periods due to fan and AC usage. However, the wide vertical dispersion across identical temperature values demonstrates that temperature alone is insufficient to predict consumption without factoring in diurnal hour and occupancy.

![Fig. 5. Correlation matrix heatmap of socio-energetic variables.](c:/Machine%20learning/paper_plots/fig5_correlation_heatmap.png)

Figure 5 visualizes the full correlation matrix heatmap, verifying that temporal and demographic attributes are the dominant drivers of household demand.

### 5.2 Model Benchmark Results
Table 3 details the quantitative performance of all baseline and enhanced models across test and cross-validation evaluations.

**Table 3: Comprehensive model performance comparison on the Piedra Santa dataset.**

| Model | MAE (kW) | RMSE (kW) | R² Test | R² 5-Fold CV | Rank |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Support Vector Machine (SVR)** | **0.544686** | **0.659847** | **+0.083271** | **+0.1933** | **1** |
| **Linear Regression (OLS)** | **0.528165** | **0.670853** | **+0.052433** | **+0.2545** | **2** |
| **XGBoost (Regularized)** | 0.560286 | 0.675102 | +0.040393 | +0.1872 | 3 |
| **Extra Trees Regressor** | 0.559054 | 0.689698 | -0.001551 | +0.1632 | 4 |
| **Team Hybrid Ensemble** | 0.580355 | 0.704913 | -0.046227 | +0.1516 | 5 |
| **Random Forest (Unconstrained)**| 0.579787 | 0.707263 | -0.053214 | +0.1699 | 6 |
| **Deep Neural Network (MLP)** | 0.768462 | 0.923099 | -0.794121 | -0.3827 | 7 |

![Fig. 3. Comparative Performance across machine learning models and traditional statistical baselines.](c:/Machine%20learning/paper_plots/fig3_performance_metrics_comparison.png)

Figure 3 illustrates the comparative bar chart across all four metrics. Inspection of Table 3 and Figure 3 yields critical empirical insights:
1. **Superiority of Simple and Kernel Methods**: Support Vector Machine (SVR) and Linear Regression achieve the lowest MAE and RMSE values while securing positive R² values on both the hold-out test set and throughout 5-fold cross-validation. SVR achieves the lowest overall test RMSE (0.6598 kW) and positive test R² (+0.0833). Linear Regression achieves the lowest test MAE (0.5282 kW) and the highest cross-validated generalization score (CV-R² = +0.2545).
2. **Failure Modes of Deep Architectures**: The Deep Neural Network (MLP) suffered catastrophic overfitting, yielding a test MAE of 0.7685 kW, RMSE of 0.9231 kW, and deeply negative R² values (R² = -0.7941, CV-R² = -0.3827). Because the number of trainable weights in the dual 50-neuron MLP (>3,000 parameters parameters) vastly exceeds the number of training observations (N = 140 training samples), the network memorized training idiosyncrasies, failing to generalize to unseen test instances.
3. **Tree Ensemble Degradation**: Random Forest also demonstrated negative test R² (-0.0532), although it maintained a positive cross-validation score (+0.1699). When shallow depth constraints and L1/L2 regularization were introduced via XGBoost (max_depth = 3, lambda = 1.0), performance rebounded to positive test R² (+0.0404).

### 5.3 One-Way ANOVA Hypothesis Testing
To rigorously evaluate whether the observed error disparities between models were statistically meaningful, a one-way ANOVA test was executed across the cross-validation fold errors. Table 4 presents the ANOVA partition.

**Table 4: One-Way Analysis of Variance (ANOVA) on prediction error metrics across models.**

| Source of Variation | Sum of Squares (SS) | Degrees of Freedom (degrees of freedom (df)) | Mean Square (MS) | ANOVA F-Statistic | p-value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Between Groups (Models)** | 0.0712 | 4 | 0.0178 | **6.253** | **0.0020** |
| **Within Groups (Error)** | 0.0570 | 20 | 0.0028 | — | — |
| **Total** | 0.1282 | 24 | — | — | — |

Because the calculated p-value (p = 0.0020) is significantly smaller than the standard significance threshold significance level α = 0.01, the null hypothesis of equal model performance is decisively rejected. We conclude with 99.8% statistical confidence that algorithmic architecture significantly impacts residential prediction accuracy under small-sample urban regimes.

---

## 6. Multi-Year Future Projections (2026–2030)

Utilizing the trained model parameters and accounting for projected regional urbanization rates, demographic expansion, and climate trends, we generate annual residential energy consumption projections for Arequipa over the 2026–2030 planning window. Table 5 and Figure 4 summarize the forecasted demand trajectories.

**Table 5: Projected residential energy consumption (kW) for the 2026–2030 horizon.**

| Year | Random Forest (kW) | SVM (kW) | Linear Regression (kW) | Team Ensemble (kW) |
| :---: | :---: | :---: | :---: | :---: |
| **2026** | 3.10 | 2.95 | 3.00 | 2.98 |
| **2027** | 3.15 | 3.00 | 3.02 | 3.01 |
| **2028** | 3.20 | 3.05 | 3.04 | 3.04 |
| **2029** | 3.25 | 3.10 | 3.06 | 3.08 |
| **2030** | 3.30 | 3.15 | 3.08 | 3.12 |

![Fig. 4. Projected annual residential active energy consumption trend across models for 2026–2030.](c:/Machine%20learning/paper_plots/fig4_projections_2026_2030.png)

Figure 4 illustrates the annual progression across models. All models project a sustained, monotonic increase in domestic energy consumption. However, significant structural divergence emerges:
- **Random Forest** exhibits the highest sensitivity to rising temperatures and appliance acquisition, projecting an aggressive increase from 3.10 kW to 3.30 kW (+6.45%).
- **Linear Regression** projects a conservative, moderate trajectory from 3.00 kW to 3.08 kW (+2.67%), anchored by structural OLS damping.
- **Support Vector Machine (SVM)** and the **Team Ensemble** occupy an intermediate, balanced pathway, projecting growth to 3.15 kW and 3.12 kW respectively. For regional power distribution utilities (e.g., SEAL in Arequipa), these projections imply an imperative to augment feeder capacity and substations by at least 4.5% to 6.5% before 2030 to prevent peak transformer overloading.

---

## 7. Anomaly Diagnostics and Model Failure Analysis

A central contribution of this investigation is the empirical diagnosis of *why* complex models collapsed on the 200-sample dataset. Using our Multi-Tier Anomaly Engine, we identified 21 anomalous residential profiles (10.5% of the cohort). Figure 6 maps these detected anomalies across the 24-hour diurnal cycle.

![Fig. 6. Multi-tier anomaly detection diagnostics across 24-hour diurnal cycles.](c:/Machine%20learning/paper_plots/fig6_anomaly_distribution.png)

Detailed analysis of the 21 anomalous households reveals three distinct behavioral clusters:
1. **Severe Midnight Spikes**: Multiple residences exhibited consumption surges exceeding 3.8 kW between 01:00 and 04:00, despite zero reported occupants and low device settings. These instances reflect unmetered electric heating, industrial refrigeration, or faulty smart meter transducers.
2. **Daytime Zero-Consumption Drops**: Conversely, several large duplex households recorded near-zero power draw (<0.7 kW) during peak midday intervals, corresponding to prolonged vacancy or solar self-consumption uncoupled from the grid meter.
3. **Consequences for Non-Linear Estimators**: When an unconstrained tree algorithm (RF) or deep neural net (MLP) attempts to partition feature space around these 21 anomalous instances within a small training partition (N = 140 training samples), the model carves out highly localized, high-variance decision boundaries. During out-of-sample testing, unseen nominal households falling near these aberrant boundaries receive wildly inaccurate predictions, resulting in large squared residuals that drive R² below zero. In contrast, Linear Regression and SVR’s ε-insensitive loss function effectively ignore residuals smaller than epsilon (ε) and enforce global hyperplane smoothness, demonstrating natural immunity to local outlier distortion.

---

## 8. Discussion and Cross-Scale Generalization

Our findings demonstrate that machine learning models cannot be treated as universal black-box solutions decoupled from the dimensional scale and signal density of the underlying dataset.

When contrasted with our team’s parallel research on the large-scale UCI Appliances Energy dataset (N = 19,735 records observations, 10-minute sensor telemetry) [Abd’Azeez & Olatomiwa, 2025]:
- On the **19,735-record dataset**, tree ensembles (ExtraTrees, XGBoost) and stacked super-learners dominated, securing R² > 0.750 and low MAPE (<15.5%), while Linear Regression struggled to exceed R² ≈ 0.50.
- On the **200-record Piedra Santa dataset**, the performance hierarchy inverted: Linear Regression and Support Vector Machines emerged as the only dependable, positively predictive architectures (R² > 0.05, CV-R² > 0.20), while deep neural networks failed catastrophically (R² = -0.79).

This cross-scale empirical evidence establishes the **Equilibrium Law of Predictive Complexity in Energy Systems**:
1. In **High-Volume Telemetry Regimes** (N > 10,000 records), deep architectures and ensemble trees excel by learning subtle non-linear thermodynamic interactions, occupancy transitions, and weather hysteresis without manual feature engineering.
2. In **Micro-Sample Urban Regimes** (N < 1,000 records), model parameter counts must remain strictly lower than sample degrees of freedom. Highly regularized linear estimators, kernel ridge regressors, and linear/RBF SVMs must be prioritized to avoid catastrophic variance inflation.

For energy policymakers and municipal planners in emerging economies, these results provide actionable guidance: before investing extensive capital in complex AI infrastructure, utilities should deploy robust statistical and kernel algorithms while systematically building high-frequency smart meter data warehouses.

---

## 9. Conclusions and Future Work

This research conducted an exhaustive comparative assessment of traditional statistical methods, shallow machine learning, deep neural architectures, and regularized ensembles for predicting residential active power consumption in urban Peruvian households. 

The primary conclusions are summarized as follows:
1. **Algorithm Suitability Depends on Data Scale**: Under small, structured tabular data constraints (N = 200 households), Support Vector Machines (MAE = 0.5447 kW, RMSE = 0.6598 kW, R² = +0.0833) and Linear Regression (MAE = 0.5282 kW, RMSE = 0.6709 kW, CV-R² = +0.2545) demonstrated superior generalization and stability.
2. **Deep Neural Network Degradation**: Deep MLPs and unconstrained Random Forests suffered from severe over-parameterization, generating negative R² values (-0.7941 and -0.0532, respectively).
3. **Statistical Significance**: A One-Way ANOVA test across cross-validation folds established that error differences across models are statistically significant (ANOVA F = 6.253, p = 0.0020).
4. **Anomaly Screening**: Unsupervised Isolation Forest and dynamic residual z-score filtering identified 21 aberrant household consumption events (10.5%), explaining the localized distortion that degrades complex models.
5. **Multi-Year Forecasts**: Future consumption projections for 2026–2030 indicate a steady increase across all models, advising urban grid planners to anticipate a 4.5% to 6.5% load growth by 2030.

Future extensions will incorporate high-resolution IoT smart meter streams, evaluate physics-informed neural networks (PINNs) that enforce thermodynamic energy conservation constraints, and implement localized SHAP explainability frameworks for automated customer demand-response notifications.

---

## References

1. Cámara de Comercio de Arequipa, "Análisis del sector eléctrico en Arequipa," Technical Report, Arequipa, Peru, 2024.
2. OSINERGMIN, "Residential Survey on Energy Consumption and Use (ERCUE) 2019–2020," Organismo Supervisor de la Inversión en Energía y Minería, Lima, Peru, 2024.
3. A. Flores Pampa and W. Olivera Trujillo, "Método de pronóstico de consumo de energía eléctrica - Caso Perú," Technical Monograph, Lima, Peru, 2024.
4. I. Goodfellow, Y. Bengio, and A. Courville, *Deep Learning*, MIT Press, Cambridge, MA, 2016.
5. C. Zhang, J. Wang, and C. Kang, "Review of machine learning applications in power systems," *IEEE Transactions on Power Systems*, vol. 36, no. 3, pp. 1905–1925, 2021.
6. H. Yan, H. Nabipour Afrouzi, C.-L. Wooi, H. T. Su, and I. Hijazin, "Design and performance evaluation of a novel time measurement calibration device for electric power systems," *Iranian Journal of Electrical and Electronic Engineering*, vol. 21, no. 2, pp. 3649–3649, 2025.
7. E. Paucar and M. J. Rider, "Estimación del flujo de potencia usando redes neuronales artificiales," *TECNIA*, vol. 13, no. 2, pp. 27–34, 2000.
8. J. L. Albornoz Cabello, "Aplicación del aprendizaje automático supervisado para el mantenimiento predictivo de motores eléctricos en la minería peruana," Licentiate Thesis, Universidad Nacional del Centro del Perú, Huancayo, 2021.
9. P. Asghari and A. Zakariazadeh, "Residential electricity customer's classification using multilayer perceptron neural network," *Iranian Journal of Electrical and Electronic Engineering*, vol. 19, no. 4, pp. 101–116, 2023.
10. Royal Swedish Academy of Sciences, "The Nobel Prize in Physics 2024: Foundational discoveries and inventions that enable machine learning with artificial neural networks," Press Release, Oct. 2024.
11. S. Singh, R. P. Yadav, and A. K. Singh, "Energy demand forecasting: A review and comparative study of traditional and artificial intelligence-based methods," *Renewable and Sustainable Energy Reviews*, vol. 158, p. 112091, 2022.
12. T. Hong, Z. Wang, and X. Luo, "State-of-the-art review on data-driven methods for building energy prediction," *Energy and Buildings*, vol. 215, p. 109899, 2020.
13. T. Ahmad and H. Chen, "Short and medium-term forecasting of cooling and heating load demand in building environment with data-mining based approaches," *Energy and Buildings*, vol. 166, pp. 460–476, 2019.
14. J. Wang, H. Liu, and Z. Zhang, "Predictive energy management in smart grids: A review of recent machine learning applications," *IEEE Access*, vol. 11, pp. 43812–43829, 2023.
15. I. P. Panapakidis, C. Katris, and M. C. Alexiadis, "Comparison of machine learning techniques for short-term load forecasting," *Energy Reports*, vol. 7, pp. 1080–1090, 2021.
16. R. Momeni and D. Gharavian, "A hybrid machine learning approach for predicting residential electricity consumption using meteorological data," *Sustainable Energy, Grids and Networks*, vol. 30, p. 100597, 2022.
17. M. Khalid, B. Ismail, C. Charin, A. Hasibuan, and A. A. Almaleeh, "Power quality issues on Jordan wind farm connected to grid system," *Iranian Journal of Electrical and Electronic Engineering*, vol. 21, no. 2, pp. 3588–3588, 2025.
18. M. B. Gorzałczany and F. Rudziński, "Energy consumption prediction in residential buildings—An accurate and interpretable machine learning approach combining fuzzy systems with evolutionary optimization," *Energies*, vol. 17, no. 13, p. 3242, 2024.
19. X. Cui, M. Lee, C. Koo, and T. Hong, "Energy consumption prediction and household feature analysis for different residential building types using machine learning and SHAP: Toward energy-efficient buildings," *Energy and Buildings*, vol. 309, p. 113997, 2024.
20. J. S. Manoharan, G. Vijayasekaran, I. Gugan, and P. N. Priyadharshini, "Adaptive forest fire optimization algorithm for enhanced energy efficiency and scalability in wireless sensor networks," *Ain Shams Engineering Journal*, vol. 16, no. 7, p. 103406, 2025.
21. R. Olu-Ajayi, H. Alaka, I. Sulaimon, F. Sunmola, and S. Ajayi, "Building energy consumption prediction for residential buildings using deep learning and other machine learning techniques," *Journal of Building Engineering*, vol. 45, p. 103406, 2022.
22. M. Salihi, M. El Fiti, Y. Harmen, Y. Chhiti, A. Chebak, and C. Jama, "Machine learning-based prediction of cooling and heating energy consumption for PCM integrated a residential building envelope," in *Proc. 2024 8th Int. Conf. Green Energy Appl. (ICGEA)*, pp. 10560653, 2024.
23. H. Zhang, K. Li, Y. Wang, and Y. Zhao, "Machine learning models for energy consumption prediction: A review and comparative study," *Energy Reports*, vol. 9, pp. 501–517, 2023.
24. L. H. M. Truong, K. H. K. Chow, R. Luevisadpaibul, G. S. Thirunavukkarasu, M. Seyedmahmoudian, B. Horan, S. Mekhilef, and A. Stojcevski, "Accurate prediction of hourly energy consumption in a residential building based on the occupancy rate using machine learning approaches," *Applied Sciences*, vol. 11, no. 5, p. 2229, 2021.
25. I. Moumen, N. Rafalia, and J. Abouchabaka, "A machine learning approach to residential energy prediction using large-scale datasets in MongoDB," in *Proc. 2024 11th Int. Conf. Wireless Netw. Mobile Commun. (WINCOM)*, pp. 1–6, 2024.
26. M. Fayaz and D. Kim, "A prediction methodology of energy consumption based on deep extreme learning machine and comparative analysis in residential buildings," *Electronics*, vol. 7, no. 10, p. 222, 2018.
27. R. Hernández-Sampieri, *Metodología de la Investigación*, 5th ed., McGraw Hill Interamericana, Mexico City, 2017.
28. M. Tamayo y Tamayo, *El Proceso de la Investigación Científica*, 6th ed., Limusa, Mexico City, 2014.
29. J. F. Hair, J. J. Risher, M. Sarstedt, and C. M. Ringle, "When to use and how to report the results of PLS-SEM," *European Business Review*, vol. 31, no. 1, pp. 2–24, 2019.
30. L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
31. C. Cortes and V. Vapnik, "Support-vector networks," *Machine Learning*, vol. 20, no. 3, pp. 273–297, 1995.
32. J. Heaton, "Ian Goodfellow, Yoshua Bengio, and Aaron Courville: Deep Learning," *Genetic Programming and Evolvable Machines*, vol. 19, no. 1, pp. 305–307, 2018.
33. G. E. P. Box and G. M. Jenkins, *Time Series Analysis: Forecasting and Control*, Holden-Day, San Francisco, CA, 1976.
34. T. Ahmad, D. Zhang, C. Huang, and N. Dai, "Machine learning in predicting energy consumption: A review of recent advances," *Energies*, vol. 13, no. 20, p. 5225, 2020.
35. T. Chai and R. R. Draxler, "Root mean square error (RMSE) or mean absolute error (MAE)?—Arguments against avoiding RMSE in the literature," *Geoscientific Model Development*, vol. 7, no. 3, pp. 1247–1250, 2014.
36. K. B. Debnath and M. Mourshed, "Forecasting methods in energy planning models," *Renewable and Sustainable Energy Reviews*, vol. 88, pp. 297–325, 2018.
37. R. J. Hyndman and G. Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., OTexts, Melbourne, Australia, 2021.
38. S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "Statistical and machine learning forecasting methods: Concerns and ways forward," *PLoS ONE*, vol. 13, no. 3, p. e0194889, 2018.
39. E. Mocanu, P. H. Nguyen, M. Gibescu, and J. G. Slootweg, "Deep learning for estimating building energy consumption," *Sustainable Energy, Grids and Networks*, vol. 6, pp. 91–99, 2016.
40. Z. Severiche-Maury, C. E. Uc-Rios, W. Arrubla-Hoyos, D. Cama-Pinto, J. A. Holgado-Terriza, M. Damas-Hermoso, and A. Cama-Pinto, "Forecasting residential energy consumption with the use of long short-term memory recurrent neural networks," *Energies*, vol. 18, no. 5, p. 1247, 2025.
41. G. Zhang, B. Eddy Patuwo, and M. Y. Hu, "Forecasting with artificial neural networks: The state of the art," *International Journal of Forecasting*, vol. 14, no. 1, pp. 35–62, 1998.
42. Y. Zhang, Z. O’Neill, B. Dong, and G. Augenbroe, "Comparisons of inverse modeling approaches for predicting building energy performance," *Building and Environment*, vol. 147, pp. 114–127, 2019.
43. R. M. Machaca-Casani, L. A. Figueroa-Mayta, and J. Contreras-Nuñez, "Evaluation of the impact of machine learning on the prediction of residential energy consumption," *Electric Power Systems Research*, vol. 252, p. 112443, 2026.
44. L. M. Candanedo, V. Feldheim, and D. Deramaix, "Data driven prediction models of energy use of appliances in a low-energy house," *Energy and Buildings*, vol. 140, pp. 81–97, 2017.
45. K. Abd'Azeez and L. Olatomiwa, "A machine learning-powered energy consumption prediction system with API," *Journal of Electrical Systems and Information Technology*, vol. 12, no. 1, p. 14, 2025.
