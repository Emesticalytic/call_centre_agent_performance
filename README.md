# Call Centre Performance & Debt-Recovery Analysis

## 🎯 Project Overview
This project analyzes call centre performance and debt recovery effectiveness using a data-driven approach. It integrates data from multiple sources (Telephony, CRM, Collections, QA, CSAT) to build a comprehensive view of operations.

## 🔑 Key Features
*   **Data Integration:** Consolidates disparate data sources into a single analytical dataset.
*   **Predictive Modeling:** Uses Random Forest and XGBoost to predict debt repayment success.
*   **Interactive Dashboard:** A Plotly Dash application for visualizing key metrics.
*   **Agent Performance Analysis:** Identifies top and bottom performers based on AHT, CSAT, and Recovery Rate.

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/call-centre-analysis.git
cd call-centre-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Analysis
Open the Jupyter Notebook `call center.ipynb` and run all cells to generate the analysis and models.

### 4. Run the Dashboard
```bash
python src/dashboard.py
```
Open your browser and navigate to `http://localhost:8050`.

## 🐳 Docker Instructions

### 1. Build the Image
```bash
docker build -t call-centre-dashboard .
```

### 2. Run the Container
```bash
docker run -p 8050:8050 call-centre-dashboard
```

## 📂 Project Structure
*   `data/`: Contains raw CSV data files.
*   `src/`: Source code for data processing, modeling, and visualization.
*   `call center.ipynb`: Main analysis notebook.
*   `requirements.txt`: Python dependencies.
*   `Dockerfile`: Docker configuration.
