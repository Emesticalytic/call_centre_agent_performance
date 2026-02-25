import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

def plot_core_kpis(df: pd.DataFrame):
    # AHT by day
    daily = df.groupby("call_date")["aht"].mean().reset_index()
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=daily, x="call_date", y="aht")
    plt.title("Average Handle Time by Day")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_debt_recovery(df: pd.DataFrame):
    # Recovery rate by agent
    if {"agent_id", "arrangement_kept"}.issubset(df.columns):
        agent = df.groupby("agent_id")["arrangement_kept"].mean().reset_index()
        plt.figure(figsize=(10, 4))
        sns.barplot(data=agent, x="agent_id", y="arrangement_kept")
        plt.title("Arrangement Success Rate by Agent")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

def plot_agent_performance(agent_performance: pd.DataFrame, metric: str, title: str, top_n: int = 10):
    """
    Plots the top and bottom N agents for a given metric.
    """
    # Top N
    top_agents = agent_performance.sort_values(by=metric, ascending=False).head(top_n)
    plt.figure(figsize=(12, 5))
    sns.barplot(data=top_agents, x="agent_id", y=metric, order=top_agents["agent_id"])
    plt.title(f"Top {top_n} Agents by {title}")
    plt.xlabel("Agent ID")
    plt.ylabel(title)
    plt.tight_layout()
    plt.show()

    # Bottom N
    bottom_agents = agent_performance.sort_values(by=metric, ascending=True).head(top_n)
    plt.figure(figsize=(12, 5))
    sns.barplot(data=bottom_agents, x="agent_id", y=metric, order=bottom_agents["agent_id"])
    plt.title(f"Bottom {top_n} Agents by {title}")
    plt.xlabel("Agent ID")
    plt.ylabel(title)
    plt.tight_layout()
    plt.show()