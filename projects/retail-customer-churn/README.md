# 🛍️ Retail Customer Churn Prediction System  
### End-to-End ML & ANN Pipeline with Streamlit Dashboard

Run commands from `projects/retail-customer-churn/`. The dashboard entry point is
`src/app.py`; paths to datasets and models resolve from the project directory.
Launch notebooks with `notebooks/` as their working directory.

The existing local `venv/` was preserved during repository organization, but it
does not currently have Streamlit installed. Set up dependencies from
`requirements.txt` before running the dashboard. Virtual-environment launcher
scripts may retain the previous absolute location; create a fresh `.venv/` when
rebuilding the environment.

This repository implements a **production-style customer churn prediction system** using
classical Machine Learning models and an Artificial Neural Network (ANN), combined with a
fully interactive **Streamlit dashboard** for model selection, prediction, and explainability.

The project is intentionally designed to reflect **real-world ML system design**, not just
academic or notebook-based experimentation.

---

## 📌 Problem Statement

Customer churn is one of the most critical challenges for retail and subscription-based businesses.

**Objective:**
> Predict customer churn probability and identify high-risk customers early so that
> targeted retention strategies can be applied proactively.

---

## 🧠 High-Level Architecture

```

Raw Transaction Data
↓
Feature Engineering (RFM + Behavioral Metrics)
↓
Customer-Level Feature Table
↓
ML & ANN Training Pipelines
↓
Saved Models + Feature Schemas
↓
Streamlit Churn Prediction Dashboard

```

---

## 📂 Project Structure

```

retail-customer-churn/
│
├── data/
│   └── processed/
│       └── customer_features_v2.csv
│
├── models/
│   ├── LogReg.joblib
│   ├── LogReg.features.json
│   ├── RandomForest.joblib
│   ├── RandomForest.features.json
│   ├── ANN_MLP.joblib
│   ├── ANN_MLP.features.json
│   ├── best_churn_model.joblib
│   └── model_features.json
│
├── notebooks/
│   ├── Exploratory Data Analysis.ipynb
│   ├── feature_engineering.ipynb
│   └── model_training_ml_ann_interview_ready.ipynb
│
├── src/
│   └── app.py
├── requirements.txt
└── README.md

```

---

##  Dataset

**File:** `customer_features_v2.csv`  
**Granularity:** One row per customer

### Feature Categories
- **RFM metrics:** Recency, Frequency, Monetary
- **Behavioral metrics:**
  - Average basket value
  - Average items per invoice
  - Purchase gap statistics (mean, median, std)
  - Return rate
- **Customer tenure**
- **Country (one-hot encoded)**
- **Target variable:** `is_churned` (binary)

---

##  Models Implemented

| Model | Purpose |
|-----|--------|
| Logistic Regression | Baseline and interpretable |
| Random Forest | Non-linear patterns and feature importance |
| ANN (MLPClassifier) | Complex feature interactions |

All models are trained using **scikit-learn Pipelines** to ensure:
- Consistent preprocessing
- No data leakage
- Safe deployment

---

##  Why ANN Requires Special Handling

ANN models internally store NumPy random generators.
If NumPy versions differ between training and inference, model loading may fail.

To prevent this:
- Models are trained in a pinned environment
- ANN models are sanitized before saving
- Feature schemas are saved alongside models


---

## 💾 Model Saving Strategy (Production-Grade)

Each model is saved with:
- `model_name.joblib`
- `model_name.features.json`

Benefits:
- Guarantees feature order consistency
- Prevents silent inference bugs
- Allows multiple models to coexist safely

---

## 📈 Model Evaluation

### Metrics Used
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

### Advanced Evaluation
- Confusion matrices
- ROC curves
- Precision–Recall curves
- Threshold tuning (business-driven)

---

## 🔍 Explainability

### Built-in Explainability
- Random Forest → `feature_importances_`
- Logistic Regression → coefficients

### Model-Agnostic Explainability
- Permutation Importance (works for ANN as well)

---

## ▶️ How to Run the Project (End-to-End)

### 1️⃣ Setup Environment

**Recommended Python version**
```

Python 3.11.x

````

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Pinned versions ensure:

* Model compatibility
* Stable ANN loading
* Reproducible results

---

### 2️⃣ Train Models & Export Artifacts

Train ML and ANN models and save them safely:

```bash
python save_trained_models_safe.py
```

This script:

* Trains Logistic Regression, Random Forest, and ANN models
* Applies consistent preprocessing
* Saves models and feature schemas
* Selects and stores the best model automatically

---

### 3️⃣ Run the Streamlit Dashboard

Launch the dashboard:

```bash
python -m streamlit run src/app.py
```

Dashboard capabilities:

* Select ML or ANN model dynamically
* Adjust churn probability threshold
* View churn probability distribution
* Identify at-risk customers
* Visualize feature importance
* Optional permutation importance

---

## 📊 Business Insights

* **High churn probability + high Recency**
  → Inactive customers (re-engagement required)

* **Low Frequency + low Tenure**
  → Early churn risk (onboarding and incentives)

* **Country-specific churn patterns**
  → Geo-targeted retention strategies

### Threshold Tuning

* Lower threshold → higher recall (catch more churners)
* Higher threshold → higher precision (lower retention cost)

Threshold selection is a **business decision**, not a purely technical one.

---

## 🧠 Interview Preparation Notes

### Machine Learning

* Why pipelines are mandatory
* ROC-AUC vs Precision–Recall curves
* Why threshold ≠ 0.5
* Feature leakage prevention

### ANN / Deep Learning

* Importance of feature scaling
* Early stopping
* Overfitting control
* Why ANN models are harder to serialize

### MLOps / Production

* Feature schema versioning
* Environment reproducibility
* Model selection at inference time
* Avoiding silent prediction failures

### Business Perspective

* Cost of churn vs retention
* KPI-driven threshold tuning
* Translating probabilities into actions

---

## 🚀 Future Enhancements

* MLflow model registry
* FastAPI inference service
* Dockerized deployment
* SHAP explainability
* Time-based validation
* Online retraining pipelines

---

## ✅ Final Takeaway

This project is built to mirror **real-world ML systems**, not just academic notebooks.

If you can explain this repository end-to-end, you are ready for:

* Senior Data Scientist roles
* ML Engineer roles
* Production ML system design discussions

```
