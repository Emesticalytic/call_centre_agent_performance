# ⚙️ MLOps Integration Strategy

This document outlines how to productionize the Call Centre Performance Analysis project using MLOps principles.

### 1. 📦 Experiment Tracking (with MLflow)
*   **Goal:** To log and compare model runs systematically.
*   **Implementation:**
    *   Install `mlflow`.
    *   Before training each model, start an MLflow run: `with mlflow.start_run():`.
    *   Log parameters (`mlflow.log_param()`), metrics (`mlflow.log_metric()`), and the trained model (`mlflow.sklearn.log_model()`).
    *   Run `mlflow ui` in the terminal to view and compare all experiments.

### 2. ✅ Model Registry
*   **Goal:** To version and manage production-ready models.
*   **Implementation:** After identifying the best model in MLflow, register it in the **MLflow Model Registry**. This gives it a version number and a stage (e.g., `Staging`, `Production`). The dashboard or prediction service can then pull the latest production model directly from the registry.

### 3. 🚀 CI/CD for ML (with GitHub Actions)
*   **Goal:** To automate the training and deployment pipeline.
*   **Implementation:**
    *   Create a GitHub Actions workflow (`.github/workflows/main.yml`).
    *   **Trigger:** The workflow can be triggered on a schedule (e.g., weekly) or on a push to the `main` branch.
    *   **Steps:**
        1.  Check out the code.
        2.  Install dependencies.
        3.  Run the data processing and model training script (`main.py`).
        4.  Log the new model to the MLflow Model Registry.
        5.  (Optional) Build and push a new Docker image for the dashboard.

### 4. 📈 Model Monitoring
*   **Goal:** To detect performance degradation in the live model.
*   **Implementation:**
    *   **Data Drift:** Periodically compare the statistical distribution of incoming prediction data with the training data. Tools like `evidently.ai` or `whylogs` can help.
    *   **Concept Drift:** If ground truth becomes available (i.e., we know if an arrangement was *actually* kept), log the live model's predictions and periodically recalculate metrics (AUC, F1).
    *   **Alerting:** Set up alerts to notify the team if performance drops below a certain threshold, triggering a retraining run.
