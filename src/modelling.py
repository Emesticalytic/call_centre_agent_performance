import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score, classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
import shap
import matplotlib.pyplot as plt

def train_arrangement_success_model(model_df: pd.DataFrame, features, target):
    """
    Trains a Random Forest Classifier.
    """
    X = model_df[features]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("--- Random Forest Results ---")
    print("AUC:", roc_auc_score(y_test, y_proba))
    print("F1:", f1_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    feature_importance = (
        pd.Series(model.feature_importances_, index=features)
        .sort_values(ascending=False)
    )
    print("Feature importance:\n", feature_importance)

    return model, X_train, X_test, y_train, y_test

def train_gradient_boosting_model(model_df: pd.DataFrame, features, target):
    """
    Trains a Gradient Boosting Classifier (sklearn).
    """
    X = model_df[features]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("--- Gradient Boosting Results ---")
    print("AUC:", roc_auc_score(y_test, y_proba))
    print("F1:", f1_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return model, X_train, X_test, y_train, y_test

def train_xgboost_model(model_df: pd.DataFrame, features, target):
    """
    Trains an XGBoost Classifier.
    """
    X = model_df[features]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # scale_pos_weight is useful for imbalanced datasets
    ratio = float(np.sum(y == 0)) / np.sum(y == 1)
    
    # Removed use_label_encoder=False to fix warning
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        scale_pos_weight=ratio,
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("--- XGBoost Results ---")
    print("AUC:", roc_auc_score(y_test, y_proba))
    print("F1:", f1_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return model, X_train, X_test, y_train, y_test

def explain_model_shap(model, X_train, X_test):
    """
    Calculates and plots SHAP values for model explainability.
    Uses the modern shap.Explainer API for better compatibility.
    """
    # Use the generic Explainer which handles Tree models automatically
    explainer = shap.Explainer(model)
    
    # Calculate SHAP values
    shap_values = explainer(X_test)

    # For binary classification, shap_values might have shape (n_samples, n_features, 2)
    # We want the values for the positive class (index 1)
    if len(shap_values.shape) == 3:
        shap_values_class1 = shap_values[:, :, 1]
    else:
        shap_values_class1 = shap_values

    # Summary plot (feature importance)
    print("SHAP Summary Plot:")
    plt.figure()
    shap.summary_plot(shap_values_class1, X_test, plot_type="bar", show=False)
    plt.show()
    
    # Beeswarm plot (detailed impact)
    print("SHAP Beeswarm Plot:")
    plt.figure()
    shap.plots.beeswarm(shap_values_class1, show=False)
    plt.show()

    return shap_values