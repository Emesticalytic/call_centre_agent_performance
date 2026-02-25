# 📖 Data Dictionary

This dictionary defines the columns available in the final `df` dataframe.

| Column Name | Data Type | Description | Origin |
|---|---|---|---|
| `call_id` | int | Unique identifier for each call. | `calls.csv` |
| `customer_id` | int | Unique identifier for each customer. | `calls.csv` |
| `agent_id` | int | Unique identifier for each agent. | `calls.csv` |
| `queue` | object | The queue the call was routed to (e.g., Billing, Tech). | `calls.csv` |
| `call_start` | datetime | Timestamp when the call was initiated. | `calls.csv` |
| `answer_time` | datetime | Timestamp when the agent answered the call. | `calls.csv` |
| `call_end` | datetime | Timestamp when the call ended. | `calls.csv` |
| `after_call_work_sec` | int | Seconds spent by the agent on post-call work. | `calls.csv` |
| `call_outcome` | object | The result of the call (e.g., Completed, Transferred). | `calls.csv` |
| `case_id` | int | Unique identifier for the CRM case. | `crm.csv` |
| `case_type` | object | The type of case opened in the CRM. | `crm.csv` |
| `balance` | float | The outstanding balance on the customer's account. | `collections.csv` |
| `arrangement_status`| object | The status of the payment arrangement (KEPT, BROKEN, ACTIVE). | `collections.csv` |
| `qa_score` | int | The quality assurance score for the call. | `qa.csv` |
| `csat_score` | int | The customer satisfaction score (1-5). | `csat.csv` |
| `talk_time` | float | The duration of the call in seconds (end - answer). | Engineered |
| `queue_time` | float | The time the customer waited in the queue in seconds. | Engineered |
| `aht` | float | Average Handle Time (talk_time + after_call_work_sec). | Engineered |
| `days_past_due` | int | Number of days the account is past its due date. | Engineered |
| `arrangement_kept` | int | Binary flag (1 for KEPT, 0 otherwise). **Target Variable**. | Engineered |
| `call_date` | object | The date part of the call_start timestamp. | Engineered |
| `call_hour` | int | The hour of the day the call started. | Engineered |
| `call_dow` | int | The day of the week the call started (0=Monday). | Engineered |
| `sla_met` | int | Binary flag (1 if queue_time was within SLA). | Engineered |
| `repeat_contact_flag`| int | Binary flag (1 if customer called back within 7 days). | Engineered |
| `fcr_flag` | int | First Contact Resolution flag (1 - repeat_contact_flag). | Engineered |
| `payment_plan_realism`| float | Ratio of instalment amount to disposable income. | Engineered |
