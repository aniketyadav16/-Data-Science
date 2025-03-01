import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from streamlit_bokeh_events import streamlit_bokeh_events
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("DeFi Pulse Explorer")
st.markdown("Dive into decentralized trading dynamics.")

np.random.seed(42)
dates = pd.date_range("2025-03-01", periods=30, freq="D")
df = pd.DataFrame({
    "Date": dates,
    "Swap_Volume_USD": np.random.uniform(50000, 150000, 30),
    "Liquidity_USD": np.random.uniform(200000, 500000, 30),
    "Gas_Cost_ETH": np.random.uniform(0.01, 0.05, 30),
    "Active_Users": np.random.randint(50, 200, 30),
    "Yield_APR": np.random.uniform(5, 25, 30) + np.random.randn(30) * 5,
    "Whale_Trades": np.random.poisson(5, 30),
    "Pool": np.random.choice(["ZAP/ETH", "ZAP/USDC"], 30)
})
df["Yield_Type"] = np.random.choice(["Staking", "Farming", "Lending"], len(df))
df["APR_Size"] = df["Yield_APR"].abs()
df["Day"] = df.index + 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("Yield Farming Breakdown")
    pool_choice = st.radio("Pool", ["ZAP/ETH", "ZAP/USDC", "Both"], index=2)
    filtered_df = df if pool_choice == "Both" else df[df["Pool"] == pool_choice]
    fig1 = px.sunburst(filtered_df, path=["Pool", "Yield_Type", "Date"], values="APR_Size",
                       color="Yield_APR", color_continuous_scale="Plasma",
                       title="Yield Farming Breakdown")
    fig1.update_layout(template="plotly_dark", title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Gas Cost Flow")
    pivot_df = df.pivot_table(values="Gas_Cost_ETH", index="Date", columns="Pool", fill_value=0)
    source = ColumnDataSource(pivot_df)
    p = figure(x_axis_type="datetime", title="Gas Cost Flow", height=300, width=600, background_fill_color="#1a1a1a")
    p.stack(pivot_df.columns, x="Date", source=source, color=["#00b4d8", "#7209b7"], legend_label=list(pivot_df.columns))
    p.legend.location = "top_left"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "#3a3a3a"
    p.outline_line_color = None
    st.bokeh_chart(p, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Whale Trade Swarms")
    pool_filter = st.multiselect("Filter Pools", df["Pool"].unique(), default=df["Pool"].unique())
    filtered_df = df[df["Pool"].isin(pool_filter)]
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#1a1a1a")
    sns.violinplot(x="Pool", y="Whale_Trades", data=filtered_df, ax=ax, inner=None, palette=["#00b4d8", "#7209b7"])
    sns.swarmplot(x="Pool", y="Whale_Trades", data=filtered_df, ax=ax, color="#f72585", size=4)
    ax.set_title("Whale Trade Swarms", color="white")
    ax.set_facecolor("#1a1a1a")
    ax.tick_params(colors="white")
    st.pyplot(fig)

with col4:
    st.subheader("Liquidity Flow Between Pools")
    play_button = st.button("Animate Liquidity Flow")
    labels = ["ZAP/ETH_Day1", "ZAP/USDC_Day1", "ZAP/ETH_Day2", "ZAP/USDC_Day2"]
    fig4 = go.Figure(data=[go.Sankey(
        node=dict(label=labels, color="#7209b7"),
        link=dict(
            source=[0, 1, 0, 1],
            target=[2, 3, 3, 2],
            value=[50000, 30000, 20000, 40000],
            color="#00b4d8"
        ))])
    if play_button:
        frames = [go.Frame(data=[go.Sankey(link=dict(value=[v * (k/10), 30000, 20000, 40000]))]) 
                  for k, v in enumerate([50000, 45000, 40000, 35000, 30000], 1)]
        fig4.frames = frames
        fig4.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                             method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig4.update_layout(template="plotly_dark", title="Liquidity Flow Between Pools", title_x=0.5, font_size=10)
    st.plotly_chart(fig4, use_container_width=True)










