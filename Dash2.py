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
df_defi = pd.DataFrame({
    "Date": dates,
    "Swap_Volume_USD": np.random.uniform(50000, 150000, 30),
    "Liquidity_USD": np.random.uniform(200000, 500000, 30),
    "Gas_Cost_ETH": np.random.uniform(0.01, 0.05, 30),
    "Active_Users": np.random.randint(50, 200, 30),
    "Yield_APR": np.random.uniform(5, 25, 30) + np.random.randn(30) * 5,
    "Whale_Trades": np.random.poisson(5, 30),
    "Pool": np.random.choice(["ZAP/ETH", "ZAP/USDC"], 30)
})
df_defi["Yield_Type"] = np.random.choice(["Staking", "Farming", "Lending"], len(df_defi))
df_defi["APR_Size"] = df_defi["Yield_APR"].abs()
df_defi["Day"] = df_defi.index + 1

df_truck = pd.DataFrame({
    "Date": dates,
    "ETH_Gas_Cost": np.random.uniform(0.02, 0.08, 30),
    "BTC_Tx_Fee": np.random.uniform(0.0005, 0.002, 30),
    "Haul_Value_USD": np.random.uniform(10000, 50000, 30),
    "Driver_Payout_ETH": np.random.uniform(0.1, 0.5, 30),
    "Truck_ID": np.random.choice(["Truck_A", "Truck_B", "Truck_C"], 30)
})
df_truck["Day"] = df_truck.index + 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("Yield Farming Breakdown")
    pool_choice = st.radio("Pool", ["ZAP/ETH", "ZAP/USDC", "Both"], index=2)
    filtered_df = df_defi if pool_choice == "Both" else df_defi[df_defi["Pool"] == pool_choice]
    fig1 = px.sunburst(filtered_df, path=["Pool", "Yield_Type", "Date"], values="APR_Size",
                       color="Yield_APR", color_continuous_scale="Plasma",
                       title="Yield Farming Breakdown")
    fig1.update_layout(template="plotly_dark", title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Gas vs. Trading Metrics")
    play_button_gas = st.button("Animate Gas Metrics")
    fig2 = px.parallel_coordinates(df_defi, color="Gas_Cost_ETH",
                                   dimensions=["Swap_Volume_USD", "Liquidity_USD", "Active_Users", "Gas_Cost_ETH"],
                                   color_continuous_scale="Plasma",
                                   title="Gas vs. Trading Metrics")
    if play_button_gas:
        frames = [go.Frame(data=[go.Parcoords(line=dict(color=df_defi["Gas_Cost_ETH"] * (k/5)))])
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
    filtered_swap = df_defi[df_defi["Pool"] == pool_swap]
    fig5 = px.bar(filtered_swap, x="Date", y="Swap_Volume_USD", 
                  title="Swap Volume by Pool", color_discrete_sequence=["#00b4d8"])
    fig5.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Yield APR Distribution")
    yield_type = st.selectbox("Select Yield Type", ["Staking", "Farming", "Lending"])
    filtered_yield = df_defi[df_defi["Yield_Type"] == yield_type]
    fig6 = px.histogram(filtered_yield, x="Yield_APR", nbins=20, 
                        title="Yield APR Distribution", color_discrete_sequence=["#7209b7"])
    fig6.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Active Users vs. Whale Trades")
    play_bar = st.button("Animate User Bars")
    fig7 = go.Figure(data=[
        go.Bar(x=df_defi["Date"], y=df_defi["Active_Users"], name="Active Users", marker_color="#00b4d8"),
        go.Bar(x=df_defi["Date"], y=df_defi["Whale_Trades"] * 10, name="Whale Trades (x10)", marker_color="#f72585")
    ])
    if play_bar:
        frames = [go.Frame(data=[
            go.Bar(x=df_defi["Date"], y=df_defi["Active_Users"] * (k/5)),
            go.Bar(x=df_defi["Date"], y=df_defi["Whale_Trades"] * 10 * (k/5))
        ]) for k in range(1, 6)]
        fig7.frames = frames
        fig7.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                              method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig7.update_layout(template="plotly_dark", title="Active Users vs. Whale Trades", title_x=0.5, barmode="group")
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.subheader("Gas Cost Spread")
    gas_pool = st.selectbox("Select Pool for Gas", ["ZAP/ETH", "ZAP/USDC"])
    filtered_gas = df_defi[df_defi["Pool"] == gas_pool]
    fig8 = px.histogram(filtered_gas, x="Gas_Cost_ETH", nbins=15, 
                        title="Gas Cost Spread", color_discrete_sequence=["#f72585"])
    fig8.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)

col9, col10 = st.columns(2)

with col9:
    st.subheader("Haul Value by Truck")
    truck_choice = st.selectbox("Select Truck", df_truck["Truck_ID"].unique())
    filtered_truck = df_truck[df_truck["Truck_ID"] == truck_choice]
    fig9 = px.bar(filtered_truck, x="Date", y="Haul_Value_USD", 
                  title="Haul Value by Truck", color_discrete_sequence=["#00b4d8"])
    fig9.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

with col10:
    st.subheader("ETH Gas Cost Distribution")
    truck_gas = st.selectbox("Truck for Gas Costs", df_truck["Truck_ID"].unique())
    filtered_gas = df_truck[df_truck["Truck_ID"] == truck_gas]
    fig10 = px.histogram(filtered_gas, x="ETH_Gas_Cost", nbins=15, 
                         title="ETH Gas Cost Distribution", color_discrete_sequence=["#7209b7"])
    fig10.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig10, use_container_width=True)

col11, col12 = st.columns(2)

with col11:
    st.subheader("ETH Gas vs. BTC Tx Fees")
    play_fees = st.button("Animate Fee Comparison")
    fig11 = go.Figure(data=[
        go.Bar(x=df_truck["Date"], y=df_truck["ETH_Gas_Cost"], name="ETH Gas", marker_color="#00b4d8"),
        go.Bar(x=df_truck["Date"], y=df_truck["BTC_Tx_Fee"], name="BTC Tx Fee", marker_color="#f72585")
    ])
    if play_fees:
        frames = [go.Frame(data=[
            go.Bar(x=df_truck["Date"], y=df_truck["ETH_Gas_Cost"] * (k/5)),
            go.Bar(x=df_truck["Date"], y=df_truck["BTC_Tx_Fee"] * (k/5))
        ]) for k in range(1, 6)]
        fig11.frames = frames
        fig11.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                              method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig11.update_layout(template="plotly_dark", title="ETH Gas vs. BTC Tx Fees", title_x=0.5, barmode="group")
    st.plotly_chart(fig11, use_container_width=True)

with col12:
    st.subheader("Driver Payout Spread")
    truck_payout = st.selectbox("Truck for Payouts", df_truck["Truck_ID"].unique())
    filtered_payout = df_truck[df_truck["Truck_ID"] == truck_payout]
    fig12 = px.histogram(filtered_payout, x="Driver_Payout_ETH", nbins=15, 
                         title="Driver Payout Spread", color_discrete_sequence=["#f72585"])
    fig12.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig12, use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    st.subheader("Whale Trade Swarms")
    pool_filter = st.multiselect("Filter Pools", df_defi["Pool"].unique(), default=df_defi["Pool"].unique())
    filtered_df = df_defi[df_defi["Pool"].isin(pool_filter)]
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
