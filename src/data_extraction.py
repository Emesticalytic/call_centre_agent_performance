# src/data_extraction.py
import pandas as pd
try:
    from src.config import CALLS_FILE, CRM_FILE, COLLECTIONS_FILE, QA_FILE, CSAT_FILE
except ImportError:
    from config import CALLS_FILE, CRM_FILE, COLLECTIONS_FILE, QA_FILE, CSAT_FILE

def load_calls():
    return pd.read_csv(CALLS_FILE, parse_dates=["call_start", "call_end", "answer_time"])

def load_crm():
    return pd.read_csv(CRM_FILE, parse_dates=["case_opened", "case_closed"])

def load_collections():
    return pd.read_csv(COLLECTIONS_FILE, parse_dates=["due_date", "arrangement_start", "arrangement_end"])

def load_qa():
    return pd.read_csv(QA_FILE)

def load_csat():
    return pd.read_csv(CSAT_FILE)

def load_all():
    calls = load_calls()
    crm = load_crm()
    coll = load_collections()
    qa = load_qa()
    csat = load_csat()
    return calls, crm, coll, qa, csat
