import pandas as pd

def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    df["call_date"] = df["call_start"].dt.date
    df["call_hour"] = df["call_start"].dt.hour
    df["call_dow"] = df["call_start"].dt.dayofweek
    return df

def add_performance_flags(df: pd.DataFrame, sla_seconds: int = 20, repeat_days: int = 7) -> pd.DataFrame:
    df["sla_met"] = (df["queue_time"] <= sla_seconds).astype(int)

    df = df.sort_values(["customer_id", "call_start"])
    df["next_call_date"] = df.groupby("customer_id")["call_start"].shift(-1)
    df["days_to_next_call"] = (df["next_call_date"] - df["call_start"]).dt.days
    df["repeat_contact_flag"] = (df["days_to_next_call"] <= repeat_days).astype(int)

    df["fcr_flag"] = 1 - df["repeat_contact_flag"]
    return df

def add_debt_features(df: pd.DataFrame) -> pd.DataFrame:
    # Example: payment plan realism proxy
    if {"instalment_amount", "estimated_disposable_income"}.issubset(df.columns):
        df["payment_plan_realism"] = df["instalment_amount"] / df["estimated_disposable_income"]
    return df

def build_modelling_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Example target: arrangement_kept (for payment‑plan success model)
    target = "arrangement_kept"
    feature_cols = [
        "days_past_due",
        "balance",
        "arrangement_length_days",
        "payment_plan_realism",
        "qa_score",
        "aht",
        "queue_time",
        "sla_met",
        "call_hour",
        "call_dow",
    ]
    features = [c for c in feature_cols if c in df.columns]
    model_df = df.dropna(subset=[target])[features + [target]]
    return model_df, features, target