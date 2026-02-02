# app.py
# Streamlit Churn Prediction App (Model Selector)
# ✅ Select model from models folder (filters out best_* models)
# ✅ Loads feature schema (per-model .features.json OR global model_features.json)
# ✅ Predicts churn_probability + predicted_churn using threshold slider
# ✅ Shows metrics, distribution chart, top churners, at-risk list
# ✅ Feature importance (RF/linear) + optional permutation importance (slow)

import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from sklearn.inspection import permutation_importance


# ============================
# Page config
# ============================
st.set_page_config(layout="wide", page_title="Churn Prediction — Model Selector")


# ============================
# DEFAULT PATHS (can override in sidebar)
# ============================
DEFAULT_DATA_PATH = Path(
    r"C:\Users\abhin\ai-systems-foundations\DeepLearningProject\data\processed\customer_features_v2.csv"
)
DEFAULT_MODELS_DIR = Path(
    r"C:\Users\abhin\ai-systems-foundations\DeepLearningProject\models"
)

TARGET_COL = "is_churned"
ID_COL_CANDIDATES = ["CustomerID", "Customer ID"]  # supports both variants


# ============================
# Helpers
# ============================
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    df.columns = df.columns.astype(str).str.strip()
    return df


def list_model_files(models_dir: Path):
    if not models_dir.exists():
        return []
    return sorted(models_dir.glob("*.joblib"))


@st.cache_resource
def load_model(model_path: str):
    return joblib.load(model_path)


def load_features_for_model(model_path: Path, models_dir: Path):
    """
    Priority:
    1) model.features.json next to model.joblib
    2) global model_features.json in MODELS_DIR
    """
    per_model = model_path.with_suffix(".features.json")  # model.joblib -> model.features.json
    if per_model.exists():
        with open(per_model, "r") as f:
            return json.load(f), str(per_model)

    global_feats = models_dir / "model_features.json"
    if global_feats.exists():
        with open(global_feats, "r") as f:
            return json.load(f), str(global_feats)

    return None, None


def align_features(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """
    Make df have exactly feature_cols in the same order.
    Missing columns -> add as 0
    Extra columns -> dropped
    """
    out = df.copy()
    for c in feature_cols:
        if c not in out.columns:
            out[c] = 0
    out = out[feature_cols]
    return out


def safe_predict_proba(model, X: pd.DataFrame) -> np.ndarray:
    """
    Most sklearn pipelines support predict_proba.
    If not, try decision_function -> logistic transform.
    """
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]

    if hasattr(model, "decision_function"):
        s = model.decision_function(X)
        return 1 / (1 + np.exp(-s))

    raise ValueError("Selected model has no predict_proba or decision_function.")


def builtin_feature_importance(model, feature_cols: list[str]) -> pd.DataFrame:
    """
    Works for:
    - Tree models: feature_importances_
    - Linear models: coef_
    """
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
        return (
            pd.DataFrame({"Feature": feature_cols, "Importance": imp})
            .sort_values("Importance", ascending=False)
        )

    if hasattr(model, "coef_"):
        coef = model.coef_
        if coef.ndim == 2 and coef.shape[0] == 1:
            imp = np.abs(coef[0])
        else:
            imp = np.abs(coef).mean(axis=0)

        return (
            pd.DataFrame({"Feature": feature_cols, "Importance": imp})
            .sort_values("Importance", ascending=False)
        )

    return pd.DataFrame()


# ============================
# Sidebar: Settings
# ============================
st.sidebar.title("⚙️ Settings")

data_path_str = st.sidebar.text_input("Data CSV path", value=str(DEFAULT_DATA_PATH))
models_dir_str = st.sidebar.text_input("Models folder", value=str(DEFAULT_MODELS_DIR))

DATA_PATH = Path(data_path_str)
MODELS_DIR = Path(models_dir_str)

threshold = st.sidebar.slider("Churn probability threshold", 0.0, 1.0, 0.50, 0.01)

st.sidebar.markdown("---")
compute_perm = st.sidebar.checkbox("Compute permutation importance (slow)", value=False)
perm_repeats = st.sidebar.slider("Permutation repeats", 3, 20, 10, 1)
perm_scoring = st.sidebar.selectbox("Permutation scoring", ["roc_auc", "f1", "accuracy"], index=0)

# Filter models: remove best_* models
HIDE_PREFIXES = ("best_",)  # removes best_churn_model, best_churn_ann_model, etc.


# ============================
# Load data
# ============================
df = load_data(str(DATA_PATH))
if df.empty:
    st.error(f"Dataset not found or empty:\n\n{DATA_PATH}")
    st.stop()


# ============================
# Load models list
# ============================
model_files = list_model_files(MODELS_DIR)
if not model_files:
    st.error(f"No .joblib models found in:\n\n{MODELS_DIR}")
    st.stop()

visible_models = [m for m in model_files if not m.stem.lower().startswith(HIDE_PREFIXES)]
model_names = [m.stem for m in visible_models]

if not model_names:
    st.error(
        "No models available after filtering.\n\n"
        f"Folder: {MODELS_DIR}\n"
        f"Filtered prefixes: {HIDE_PREFIXES}\n"
        "Fix: Put LogReg.joblib / RandomForest.joblib / ANN_MLP.joblib etc in the folder."
    )
    st.stop()

selected_model_name = st.sidebar.selectbox("Select model", model_names, index=0)
selected_model_path = next(m for m in visible_models if m.stem == selected_model_name)


# ============================
# Load selected model
# ============================
try:
    model = load_model(str(selected_model_path))
except Exception as e:
    st.error(f"Failed to load model:\n\n{selected_model_path}\n\nError:\n{e}")
    st.stop()


# ============================
# Load features for selected model
# ============================
feature_cols, feature_src = load_features_for_model(selected_model_path, MODELS_DIR)
if not feature_cols:
    st.error(
        "Could not find feature schema JSON.\n\n"
        "Fix by generating one of these:\n"
        f"1) {selected_model_path.with_suffix('.features.json')}\n"
        f"2) {MODELS_DIR / 'model_features.json'}"
    )
    st.stop()

st.sidebar.caption(f"✅ Features loaded from: {feature_src}")


# ============================
# Build X (inference)
# ============================
df_in = df.copy()

y_true = None
if TARGET_COL in df_in.columns:
    y_true = pd.to_numeric(df_in[TARGET_COL], errors="coerce").fillna(0).astype(int)
    df_in = df_in.drop(columns=[TARGET_COL])

for c in ID_COL_CANDIDATES:
    if c in df_in.columns:
        df_in = df_in.drop(columns=[c])

X = align_features(df_in, feature_cols)


# ============================
# Predict
# ============================
try:
    probs = safe_predict_proba(model, X)
except Exception as e:
    st.error(f"Prediction failed for model: {selected_model_path}\n\nError:\n{e}")
    st.stop()

preds = (probs >= threshold).astype(int)

df_out = df.copy()
df_out["churn_probability"] = probs
df_out["predicted_churn"] = preds


# ============================
# UI
# ============================
st.title("🛍️ Churn Prediction Dashboard — Model Selector")
st.caption(f"Selected model: **{selected_model_name}**")

c1, c2, c3, c4 = st.columns(4)

total_customers = df_out["CustomerID"].nunique() if "CustomerID" in df_out.columns else len(df_out)

with c1:
    st.metric("Total Customers", f"{total_customers:,}")

with c2:
    st.metric("Predicted Churn Rate", f"{df_out['predicted_churn'].mean() * 100:.2f}%")

with c3:
    st.metric("Predicted Churners", f"{int(df_out['predicted_churn'].sum()):,}")

with c4:
    st.metric("Avg Churn Probability", f"{df_out['churn_probability'].mean():.3f}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📈 Predictions", "🔍 Feature Importance", "🎯 At-Risk Customers"])


# ============================
# Tab 1: Predictions
# ============================
with tab1:
    st.subheader("Churn Probability Distribution")
    fig = px.histogram(df_out, x="churn_probability", nbins=40, title="Distribution of churn_probability")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Predicted Churners")
    base_cols = [c for c in ["CustomerID", "Customer ID", "Recency", "Frequency", "Monetary", "Tenure"] if c in df_out.columns]
    show_cols = base_cols + ["churn_probability", "predicted_churn"]

    st.dataframe(
        df_out.sort_values("churn_probability", ascending=False)[show_cols].head(50),
        use_container_width=True
    )


# ============================
# Tab 2: Feature importance
# ============================
with tab2:
    st.subheader("Built-in Feature Importance (if supported)")

    # If this is a Pipeline, extract underlying estimator
    estimator = getattr(model, "named_steps", {}).get("model", model)
    fi = builtin_feature_importance(estimator, feature_cols)

    if not fi.empty:
        top = fi.head(20).copy()
        fig = px.bar(top, x="Importance", y="Feature", orientation="h", title="Top 20 Feature Importances")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Built-in feature importance not available for this model type (common for ANN/MLP).")

    st.markdown("---")
    st.subheader("Permutation Importance (model-agnostic)")

    if compute_perm:
        if y_true is None:
            st.warning(
                "Your CSV has no ground-truth 'is_churned'. Permutation importance needs y.\n"
                "Tip: include 'is_churned' column in your dataset to compute this correctly."
            )
        else:
            with st.spinner("Computing permutation importance... (can take time)"):
                try:
                    perm = permutation_importance(
                        model,
                        X,
                        y_true,
                        n_repeats=perm_repeats,
                        random_state=42,
                        scoring=perm_scoring
                    )
                    perm_imp = (
                        pd.DataFrame({"Feature": feature_cols, "Importance": perm.importances_mean})
                        .sort_values("Importance", ascending=False)
                    )
                    top = perm_imp.head(20).copy()
                    fig = px.bar(
                        top, x="Importance", y="Feature", orientation="h",
                        title=f"Permutation Importance (Top 20) — scoring={perm_scoring}"
                    )
                    fig.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Permutation importance failed:\n\n{e}")
    else:
        st.caption("Enable the checkbox in the sidebar to compute permutation importance.")


# ============================
# Tab 3: At-risk customers
# ============================
with tab3:
    st.subheader("At-Risk Customers (by threshold)")
    st.write(f"Threshold: **{threshold:.2f}**")

    at_risk = df_out[df_out["churn_probability"] >= threshold].sort_values("churn_probability", ascending=False)
    st.info(f"Showing **{len(at_risk):,}** customers with churn_probability ≥ {threshold:.2f}")

    display_cols = [c for c in ["CustomerID", "Customer ID", "Recency", "Frequency", "Monetary", "Tenure"] if c in at_risk.columns]
    display_cols += ["churn_probability", "predicted_churn"]

    st.dataframe(at_risk[display_cols].head(500), use_container_width=True)

st.markdown("---")
st.caption(
    "Tip: Threshold tuning is a business decision. Higher threshold → fewer customers flagged (higher precision). "
    "Lower threshold → more customers flagged (higher recall)."
)
