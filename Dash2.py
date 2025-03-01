import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6

st.title("Dashboard 2")
dates = pd.date_range("2025-03-01", periods=30, freq="D")
np.random.seed(42)
df = pd.DataFrame({
    "Date": dates,
    "Swap_Volume_USD": np.random.uniform(50000, 150000, 30),  
    "Liquidity_USD": np.random.uniform(200000, 500000, 30),   
    "Gas_Cost_ETH": np.random.uniform(0.01, 0.05, 30),        
    "Active_Users": np.random.randint(50, 200, 30),           
    "Pool": np.random.choice(["ZAP/ETH", "ZAP/USDC"], 30)    
})

df["Day"] = df.index + 1 

pool = st.sidebar.selectbox("Select Pool", df["Pool"].unique())
filtered_df = df[df["Pool"] == pool]

fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Swap_Volume_USD"], 
                         fill="tozeroy", name="Swap Volume ($)", mode="lines"))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Liquidity_USD"], 
                         fill="tozeroy", name="Liquidity ($)", mode="lines", opacity=0.5))

frames = [go.Frame(data=[
    go.Scatter(x=filtered_df["Date"][:k], y=filtered_df["Swap_Volume_USD"][:k], fill="tozeroy"),
    go.Scatter(x=filtered_df["Date"][:k], y=filtered_df["Liquidity_USD"][:k], fill="tozeroy")
]) for k in range(1, len(filtered_df)+1)]
fig.frames = frames
fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play", 
                        method="animate", args=[None, {"frame": {"duration": 200}}])])],
                  title="Swap Volume vs. Liquidity (Animated)")
st.plotly_chart(fig)

st.subheader("Second One")
show_both = st.sidebar.checkbox("Show Both Pools", value=True)
filtered_df = df if show_both else df[df["Pool"] == st.sidebar.selectbox("Pool", df["Pool"].unique())]
fig2 = px.scatter_3d(filtered_df, x="Swap_Volume_USD", y="Gas_Cost_ETH", z="Date", 
                    size="Active_Users", color="Pool", title="DeFi Trading Dynamics (3D)",
                    labels={"Swap_Volume_USD": "Volume ($)", "Gas_Cost_ETH": "Gas (ETH)", "Active_Users": "Users"})
fig2.update_traces(marker=dict(opacity=0.8))
st.plotly_chart(fig2)

st.subheader("Third")
pivot_df = df.pivot_table(values="Gas_Cost_ETH", index="Pool", columns="Date", fill_value=0)

gas_thresh = st.sidebar.slider("Gas Cost Threshold (ETH)", 0.0, 0.05, 0.03)
filtered_pivot = pivot_df.where(pivot_df > gas_thresh, 0)

fig3 = px.imshow(filtered_pivot, title="Gas Cost Heatmap (DeFi Pools)", 
                labels=dict(x="Date", y="Pool", color="Gas (ETH)"),
                color_continuous_scale="Viridis")
st.plotly_chart(fig3)

st.header("Fourth")
np.random.seed(42)
dat = pd.date_range("2025-03-01", periods=30, freq="D")
df = pd.DataFrame({
    "Date": dat,
    "Swap_Volume_USD": np.random.uniform(50000, 150000, 30),
    "Liquidity_USD": np.random.uniform(200000, 500000, 30),
    "Gas_Cost_ETH": np.random.uniform(0.01, 0.05, 30),
    "Active_Users": np.random.randint(50, 200, 30),
    "Yield_APR": np.random.uniform(5, 25, 30) + np.random.randn(30) * 5, 
    "Whale_Trades": np.random.poisson(5, 30),  
    "Pool": np.random.choice(["ZAP/ETH", "ZAP/USDC"], 30)
})
pivot_df = df.pivot_table(values="Gas_Cost_ETH", index="Date", columns="Pool", fill_value=0)
source = ColumnDataSource(pivot_df)

p = figure(x_axis_type="datetime", title="Gas Cost Flow (Mock DeFi)", height=300, width=600)
p.stack(pivot_df.columns, x="Date", source=source, color=Spectral6[:2], legend_label=list(pivot_df.columns))
p.legend.location = "top_left"
st.bokeh_chart(p)











