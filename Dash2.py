import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    st.subheader("Gas vs. Trading Metrics")
    play_button_gas = st.button("Animate Gas Metrics")
    fig2 = px.parallel_coordinates(df, color="Gas_Cost_ETH",
                                   dimensions=["Swap_Volume_USD", "Liquidity_USD", "Active_Users", "Gas_Cost_ETH"],
                                   color_continuous_scale="Plasma",
                                   title="Gas vs. Trading Metrics")
    if play_button_gas:
        frames = [go.Frame(data=[go.Parcoords(line=dict(color=df["Gas_Cost_ETH"] * (k/5)))])
                  for k in range(1, 6)]
        fig2.frames = frames
        fig2.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                             method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig2.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)


col5, col6 = st.columns(2)

with col5:
    st.subheader("Swap Volume by Pool")
    pool_swap = st.selectbox("Select Pool for Volume", ["ZAP/ETH", "ZAP/USDC"])
    filtered_swap = df[df["Pool"] == pool_swap]
    fig5 = px.bar(filtered_swap, x="Date", y="Swap_Volume_USD", 
                  title="Swap Volume by Pool", color_discrete_sequence=["#00b4d8"])
    fig5.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Yield APR Distribution")
    yield_type = st.selectbox("Select Yield Type", ["Staking", "Farming", "Lending"])
    filtered_yield = df[df["Yield_Type"] == yield_type]
    fig6 = px.histogram(filtered_yield, x="Yield_APR", nbins=20, 
                        title="Yield APR Distribution", color_discrete_sequence=["#7209b7"])
    fig6.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Active Users vs. Whale Trades")
    play_bar = st.button("Animate User Bars")
    fig7 = go.Figure(data=[
        go.Bar(x=df["Date"], y=df["Active_Users"], name="Active Users", marker_color="#00b4d8"),
        go.Bar(x=df["Date"], y=df["Whale_Trades"] * 10, name="Whale Trades (x10)", marker_color="#f72585")
    ])
    if play_bar:
        frames = [go.Frame(data=[
            go.Bar(x=df["Date"], y=df["Active_Users"] * (k/5)),
            go.Bar(x=df["Date"], y=df["Whale_Trades"] * 10 * (k/5))
        ]) for k in range(1, 6)]
        fig7.frames = frames
        fig7.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                             method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig7.update_layout(template="plotly_dark", title="Active Users vs. Whale Trades", title_x=0.5, barmode="group")
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.subheader("Gas Cost Spread")
    gas_pool = st.selectbox("Select Pool for Gas", ["ZAP/ETH", "ZAP/USDC"])
    filtered_gas = df[df["Pool"] == gas_pool]
    fig8 = px.histogram(filtered_gas, x="Gas_Cost_ETH", nbins=15, 
                        title="Gas Cost Spread", color_discrete_sequence=["#f72585"])
    fig8.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)
