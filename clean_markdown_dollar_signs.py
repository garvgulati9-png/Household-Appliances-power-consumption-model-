import re
import os

filepath = r"c:\Machine learning\Research_Paper_Residential_Energy_Prediction.md"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Exact replacement dictionary for block and inline expressions
replacements = {
    # Blocks
    r"$$X_{\text{scaled}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}$$":
        "```text\nX_scaled = (X - X_min) / (X_max - X_min)\n```",

    r"$$\hat{y}_i = \beta_0 + \sum_{j=1}^{p} \beta_j x_{ij} + \epsilon_i$$":
        "```text\nŷ_i = β_0 + Σ_{j=1...p} (β_j * x_ij) + ε_i\n```",

    r"$$\min_{\mathbf{w}, b, \boldsymbol{\xi}, \boldsymbol{\xi}^*} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^{n} (\xi_i + \xi_i^*)$$":
        "```text\nminimize_{w, b, ξ, ξ*}  (1/2) ||w||² + C * Σ_{i=1...n} (ξ_i + ξ_i*)\n```",

    r"""$$\begin{cases} y_i - \mathbf{w}^T \Phi(\mathbf{x}_i) - b \le \epsilon + \xi_i \\ \mathbf{w}^T \Phi(\mathbf{x}_i) + b - y_i \le \epsilon + \xi_i^* \\ \xi_i, \xi_i^* \ge 0 \end{cases}$$""":
        "```text\nSubject to:\n  y_i - w^T Φ(x_i) - b ≤ ε + ξ_i\n  w^T Φ(x_i) + b - y_i ≤ ε + ξ_i*\n  ξ_i, ξ_i* ≥ 0\n```",

    r"$$K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2\right)$$":
        "```text\nK(x_i, x_j) = exp(-γ * ||x_i - x_j||²)\n```",

    r"$$\hat{y}_{\text{RF}}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x}; \Theta_b)$$":
        "```text\nŷ_RF(x) = (1/B) * Σ_{b=1...B} T_b(x; Θ_b)\n```",

    r"$$\mathbf{h}^{(1)} = \text{ReLU}\left(\mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}\right)$$":
        "```text\nh^(1) = ReLU(W^(1) * x + b^(1))\n```",

    r"$$\mathbf{h}^{(2)} = \text{ReLU}\left(\mathbf{W}^{(2)} \mathbf{h}^{(1)} + \mathbf{b}^{(2)}\right)$$":
        "```text\nh^(2) = ReLU(W^(2) * h^(1) + b^(2))\n```",

    r"$$\hat{y}_{\text{MLP}} = \mathbf{W}^{(3)} \mathbf{h}^{(2)} + b^{(3)}$$":
        "```text\nŷ_MLP = W^(3) * h^(2) + b^(3)\n```",

    r"$$\mathcal{L}^{(t)} = \sum_{i=1}^{n} \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^{T} w_j^2 + \alpha \sum_{j=1}^{T} |w_j|$$":
        "```text\nL^(t) = Σ_{i=1...n} [ g_i * f_t(x_i) + 0.5 * h_i * f_t(x_i)² ] + γ*T + 0.5*λ * Σ_{j=1...T} w_j² + α * Σ_{j=1...T} |w_j|\n```",

    r"$$\hat{y}_{\text{Ensemble}} = w_0 + w_{\text{SVR}} \hat{y}_{\text{SVR}} + w_{\text{LR}} \hat{y}_{\text{LR}} + w_{\text{XGB}} \hat{y}_{\text{XGB}}$$":
        "```text\nŷ_Ensemble = w_0 + (w_SVR * ŷ_SVR) + (w_LR * ŷ_LR) + (w_XGB * ŷ_XGB)\n```",

    r"$$s(\mathbf{x}, n) = 2^{-\frac{\mathbb{E}(h(\mathbf{x}))}{c(n)}}$$":
        "```text\ns(x, n) = 2^(-E(h(x)) / c(n))\n```",

    r"$$z_i = \left| \frac{y_i - \hat{y}_{\text{Ensemble}, i}}{\sigma_{\text{residual}}} \right| > 2.0$$":
        "```text\nz_i = |(y_i - ŷ_Ensemble,i) / σ_residual| > 2.0\n```",

    r"$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$":
        "```text\nMAE = (1/n) * Σ_{i=1...n} |y_i - ŷ_i|\n```",

    r"$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$":
        "```text\nRMSE = sqrt( (1/n) * Σ_{i=1...n} (y_i - ŷ_i)² )\n```",

    r"$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}$$":
        "```text\nR² = 1 - [ Σ_{i=1...n} (y_i - ŷ_i)² ] / [ Σ_{i=1...n} (y_i - ȳ)² ]\n```",

    r"$$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}} = \frac{\frac{\text{SS}_{\text{between}}}{k - 1}}{\frac{\text{SS}_{\text{within}}}{N - k}}$$":
        "```text\nANOVA F = MS_between / MS_within = [ SS_between / (k - 1) ] / [ SS_within / (N - k) ]\n```",

    # Inlines
    "$R^2$": "R²",
    "$R^2=0.0524$": "R² = 0.0524",
    "$\\text{CV-}R^2=0.2545$": "CV-R² = 0.2545",
    "$\\text{CV-}R^2=+0.2545$": "CV-R² = +0.2545",
    "$R^2=0.0833$": "R² = 0.0833",
    "$R^2=+0.0833$": "R² = +0.0833",
    "$\\text{CV-}R^2=0.1933$": "CV-R² = 0.1933",
    "$R^2=-0.0532$": "R² = -0.0532",
    "$R^2=-0.7941$": "R² = -0.7941",
    "$R^2 = -0.7941$": "R² = -0.7941",
    "$\\text{CV-}R^2=-0.3827$": "CV-R² = -0.3827",
    "$\\text{CV-}R^2 = -0.3827$": "CV-R² = -0.3827",
    "$R^2 < 0$": "R² < 0",
    "$R^2 > 0.99$": "R² > 0.99",
    "$R^2 > 0.750$": "R² > 0.750",
    "$R^2 \\approx 0.50$": "R² ≈ 0.50",
    "$R^2 > 0.05$": "R² > 0.05",
    "$\\text{CV-}R^2 > 0.20$": "CV-R² > 0.20",
    "$R^2 = -0.79$": "R² = -0.79",
    "$\\text{MAE}=0.5282$": "MAE = 0.5282 kW",
    "$\\text{RMSE}=0.6709$": "RMSE = 0.6709 kW",
    "$\\text{MAE}=0.5447$": "MAE = 0.5447 kW",
    "$\\text{RMSE}=0.6598$": "RMSE = 0.6598 kW",
    "$N=200$": "N = 200 households",
    "$N = 200$": "N = 200 households",
    "$N=140$": "N = 140 training samples",
    "$N_{\\text{train}} = 140$": "N_train = 140 samples",
    "$N_{\\text{test}} = 60$": "N_test = 60 samples",
    "$N = 19,735$": "N = 19,735 records",
    "$N > 10^4$": "N > 10,000 records",
    "$N < 10^3$": "N < 1,000 records",
    "$F = 6.253$": "ANOVA F = 6.253",
    "$p = 0.0020$": "p = 0.0020",
    "$z$-score": "z-score",
    "$z$": "z",
    "$\\epsilon$-insensitive": "ε-insensitive",
    "$\\epsilon$": "epsilon (ε)",
    "$-0.0532$": "-0.0532",
    "$-0.7941$": "-0.7941",
    "$1 \\le i \\le 200$": "1 ≤ i ≤ 200",
    "$0 \\le t \\le 23$": "0 ≤ t ≤ 23",
    "$10.03^\\circ\\text{C} \\le T \\le 33.67^\\circ\\text{C}$": "10.03 °C ≤ T ≤ 33.67 °C",
    "$1 \\le P \\le 6$": "1 ≤ P ≤ 6 people",
    "$0.61 \\le Y \\le 4.31\\text{ kW}$": "0.61 kW ≤ Y ≤ 4.31 kW",
    "$[0, 1]$": "[0, 1]",
    "$r = +0.514$": "r = +0.514",
    "$r = +0.187$": "r = +0.187",
    "$r = -0.114$": "r = -0.114",
    "$r = -0.007$": "r = -0.007",
    "$\\boldsymbol{\\beta} = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$": "β = (X^T X)^(-1) X^T y",
    "$\\sum (y_i - \\hat{y}_i)^2$": "Σ (y_i - ŷ_i)²",
    "$\\Phi(\\mathbf{x})$": "Φ(x)",
    "$C=1.0$": "C = 1.0",
    "$\\epsilon=0.1$": "ε = 0.1",
    "$B=100$": "B = 100 decision trees",
    "$\\mathcal{D}_b$": "bootstrap samples D_b",
    "$m \\le p$": "m ≤ p",
    "$\\Delta I = \\text{Var}(S) - \\frac{|S_L|}{|S|} \\text{Var}(S_L) - \\frac{|S_R|}{|S|} \\text{Var}(S_R)$": "ΔI = Var(S) - (|S_L| / |S|) Var(S_L) - (|S_R| / |S|) Var(S_R)",
    "$H_1=50$": "H_1 = 50 neurons",
    "$H_2=50$": "H_2 = 50 neurons",
    "$g_i$": "first-order gradient g_i",
    "$h_i$": "second-order Hessian h_i",
    "$\\lambda=1.0$": "λ = 1.0",
    "$L_2$": "L2",
    "$\\alpha=0.5$": "α = 0.5",
    "$L_1$": "L1",
    "$\\text{max\\_depth}=3$": "max_depth = 3",
    "$\\eta=0.05$": "learning rate η = 0.05",
    "$\\mathbf{Z} \\in \\mathbb{R}^{n \\times 3}$": "level-1 matrix Z in R^(n x 3)",
    "$\\mathbf{w}$": "weights w",
    "$w_j \\ge 0, \\alpha_\\text{meta}=1.0$": "w_j ≥ 0, alpha_meta = 1.0",
    "$w_j \\ge 0, \\alpha_{\\text{meta}}=1.0$": "w_j ≥ 0, alpha_meta = 1.0",
    "$h(\\mathbf{x})$": "average path length h(x)",
    "$2\\sigma$": "2σ (two standard deviations)",
    "$K=5$": "K = 5 folds",
    "$\\text{CV-}R^2 = +0.2545$": "CV-R² = +0.2545",
    "$>3,000$": ">3,000 parameters",
    "$L_1/L_2$": "L1/L2",
    "$\\text{max\\_depth}=3, \\lambda=1.0$": "max_depth = 3, lambda = 1.0",
    "$df$": "degrees of freedom (df)",
    "$F$-Statistic": "ANOVA F-Statistic",
    "$F$": "F-statistic",
    "$\\alpha = 0.01$": "significance level α = 0.01",
    "$^\\circ\\text{C}$": "°C",
    "$1$": "1",
    "$0$": "0",
    "$p$": "p"
}

for k, v in replacements.items():
    text = text.replace(k, v)

# Update authors with all 3 registration numbers
old_author_line = "**Garv Gulati**, **Umang Gupta**, **Nikhil Goyal**"
new_author_line = "**Garv Gulati** (Registration No: RA2411003010319), **Umang Gupta** (Registration No: RA22110030100012), **Nikhil Goyal** (Registration No: RA2411003010489)"
text = text.replace(old_author_line, new_author_line)

# Check for any remaining dollar signs
remaining = re.findall(r"\$\$[\s\S]*?\$\$|\$[^\$\n]+?\$|\$", text)
print(f"Remaining dollar signs: {len(remaining)}")
for r in remaining[:20]:
    print("REMAINING:", repr(r))

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Saved {filepath} successfully.")
