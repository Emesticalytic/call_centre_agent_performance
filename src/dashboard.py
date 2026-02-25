import sys
import os

# Add the project root directory to sys.path
# This allows imports to work whether running from root or src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Use absolute imports based on the project structure
from src.data_extraction import load_all
from src.data_preparation import prepare_calls, prepare_collections, join_datasets
from src.feature_engineering import add_temporal_features, add_performance_flags, add_debt_features

# Load and prepare data
print("Loading data for dashboard...")
try:
    calls, crm, coll, qa, csat = load_all()
    calls = prepare_calls(calls)
    coll = prepare_collections(coll)
    df = join_datasets(calls, crm, coll, qa, csat)
    df = add_temporal_features(df)
    df = add_performance_flags(df)
    df = add_debt_features(df)
    
    # Ensure call_date is datetime for plotting
    df['call_date'] = pd.to_datetime(df['call_date'])

    print("Data loaded successfully.")
    print(f"Dataframe shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Please ensure you are running this script from the project root directory.")
    sys.exit(1)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Call Centre Performance Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Agent:"),
        dcc.Dropdown(
            id='agent-dropdown',
            options=[{'label': f'Agent {i}', 'value': i} for i in sorted(df['agent_id'].unique())],
            value=None,
            placeholder="All Agents"
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label("Select Queue:"),
        dcc.Dropdown(
            id='queue-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['queue'].unique())],
            value=None,
            placeholder="All Queues"
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '20px'}),

    html.Div([
        dcc.Graph(id='aht-trend'),
        dcc.Graph(id='csat-distribution'),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    html.Div([
        dcc.Graph(id='recovery-rate'),
        dcc.Graph(id='call-outcome'),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
])

# Callbacks
@app.callback(
    [Output('aht-trend', 'figure'),
     Output('csat-distribution', 'figure'),
     Output('recovery-rate', 'figure'),
     Output('call-outcome', 'figure')],
    [Input('agent-dropdown', 'value'),
     Input('queue-dropdown', 'value')]
)
def update_graphs(selected_agent, selected_queue):
    print(f"Callback triggered. Agent: {selected_agent}, Queue: {selected_queue}")
    filtered_df = df.copy()
    
    if selected_agent:
        filtered_df = filtered_df[filtered_df['agent_id'] == selected_agent]
    if selected_queue:
        filtered_df = filtered_df[filtered_df['queue'] == selected_queue]
        
    print(f"Filtered dataframe shape: {filtered_df.shape}")
    
    if filtered_df.empty:
        print("Warning: Filtered dataframe is empty.")
        empty_fig = px.scatter(title="No Data Available")
        return empty_fig, empty_fig, empty_fig, empty_fig

    try:
        # AHT Trend
        daily_aht = filtered_df.groupby('call_date')['aht'].mean().reset_index()
        fig_aht = px.line(daily_aht, x='call_date', y='aht', title='Average Handle Time (AHT) Trend')
        
        # CSAT Distribution
        fig_csat = px.histogram(filtered_df, x='csat_score', nbins=5, title='CSAT Score Distribution')
        
        # Recovery Rate (if applicable)
        if 'arrangement_kept' in filtered_df.columns:
            recovery_rate = filtered_df['arrangement_kept'].mean()
            fig_recovery = px.bar(x=['Recovery Rate'], y=[recovery_rate], title='Debt Recovery Rate')
            fig_recovery.update_yaxes(range=[0, 1])
        else:
            fig_recovery = px.bar(title='Debt Recovery Rate (No Data)')

        # Call Outcome
        outcome_counts = filtered_df['call_outcome'].value_counts().reset_index()
        outcome_counts.columns = ['outcome', 'count']
        fig_outcome = px.pie(outcome_counts, values='count', names='outcome', title='Call Outcomes')
        
        return fig_aht, fig_csat, fig_recovery, fig_outcome
    except Exception as e:
        print(f"Error in callback: {e}")
        error_fig = px.scatter(title=f"Error: {str(e)}")
        return error_fig, error_fig, error_fig, error_fig

if __name__ == '__main__':
    # Updated to use debug=False for better stability
    app.run(debug=False, host='127.0.0.1', port=8051)