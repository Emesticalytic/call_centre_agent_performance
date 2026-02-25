import pandas as pd

def prepare_calls(calls: pd.DataFrame) -> pd.DataFrame:
    calls = calls.drop_duplicates(subset=["call_id"])
    calls = calls[calls["call_end"] >= calls["call_start"]]

    calls["talk_time"] = (calls["call_end"] - calls["answer_time"]).dt.total_seconds()
    calls["queue_time"] = (calls["answer_time"] - calls["call_start"]).dt.total_seconds()
    calls["aht"] = calls["talk_time"] + calls["after_call_work_sec"]

    return calls

def prepare_collections(coll: pd.DataFrame) -> pd.DataFrame:
    coll = coll.drop_duplicates(subset=["account_id"])
    coll["days_past_due"] = (pd.Timestamp("today").normalize() - coll["due_date"]).dt.days
    coll["arrangement_length_days"] = (coll["arrangement_end"] - coll["arrangement_start"]).dt.days
    coll["arrangement_kept"] = coll["arrangement_status"].eq("KEPT").astype(int)
    
    # CRITICAL FIX: Deduplicate by customer_id to prevent row explosion during join.
    # We keep the account with the highest balance as the primary account for the customer.
    coll = coll.sort_values("balance", ascending=False).drop_duplicates(subset=["customer_id"])
    
    return coll

def join_datasets(calls, crm, coll, qa, csat):
    # Merge CRM on call_id
    df = calls.merge(crm, on="call_id", how="left", suffixes=("", "_crm"))
    
    # CRITICAL FIX: Merge Collections on customer_id (calls dataset does not have account_id)
    df = df.merge(coll, on="customer_id", how="left", suffixes=("", "_coll"))
    
    # Merge QA and CSAT on call_id
    df = df.merge(qa, on="call_id", how="left", suffixes=("", "_qa"))
    df = df.merge(csat, on="call_id", how="left", suffixes=("", "_csat"))
    
    # Remove any columns that are entirely constant (single value)
    for col in df.columns:
        if df[col].nunique() <= 1:
            df.drop(columns=[col], inplace=True)

    return df