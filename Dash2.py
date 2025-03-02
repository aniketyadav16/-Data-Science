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

st.subheader("Blockchain Pipeline Pressure")

np.random.seed(42)
dates = pd.date_range("2025-03-01", periods=30, freq="D")
df = pd.DataFrame({
    "Date": dates,
    "ETH_Gas_Cost": np.random.uniform(1.2, 4, 30),  
    "BTC_Mempool_Size_MB": np.random.uniform(50, 150, 30),  
    "Pipeline_Latency_Sec": np.random.uniform(0.5, 2.0, 30)  
})
df["Day"] = df.index + 1

fig = go.Figure()

fig.add_trace(go.Bar(x=df["Date"], y=df["ETH_Gas_Cost"], 
                     name="ETH Gas Cost", marker_color="mistyrose"))
fig.add_trace(go.Bar(x=df["Date"], y=df["BTC_Mempool_Size_MB"], 
                     name="BTC Mempool Size", marker_color="#7209b7"))
fig.add_trace(go.Bar(x=df["Date"], y=df["Pipeline_Latency_Sec"], 
                     name="Pipeline Latency", marker_color="#f72585"))

frames = [go.Frame(data=[
    go.Bar(x=df["Date"], y=df["ETH_Gas_Cost"][:k+1]),
    go.Bar(x=df["Date"], y=df["BTC_Mempool_Size_MB"][:k+1]),
    go.Bar(x=df["Date"], y=df["Pipeline_Latency_Sec"][:k+1])
]) for k in range(len(df))]
fig.frames = frames

fig.update_layout(
    template="plotly_dark",
    title = "Blockahin Pipeline Pressure",
    xaxis_title="Date",
    yaxis_title="Value",
    barmode="stack",
    height=700,
    margin=dict(l=0, r=0, t=50, b=0),
    paper_bgcolor="#1a1a1a",
    plot_bgcolor="#1a1a1a",
    legend=dict(x=0.9, y=0.99, bgcolor="rgba(0,0,0,0)")
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



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
    "Truck_ID": np.random.choice(["Truck_A", "Truck_B", "Truck_C"], 30),
    "ETH_Price_USD": 3000 + np.random.randn(30) * 100,
    "BTC_Price_USD": 60000 + np.random.randn(30) * 2000,
    "ETH_Wallet_Count": np.random.randint(20, 100, 30),
    "BTC_Mempool_Size_MB": np.random.uniform(50, 150, 30)
})
df_truck["Day"] = df_truck.index + 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("Yield Farming Breakdown")
    st.markdown("Tip: Click on Farming") 
    filtered_df = df_defi 
    fig1 = px.sunburst(filtered_df, path=["Pool", "Yield_Type", "Date"], values="APR_Size",
                       color="Yield_APR", color_continuous_scale="Viridis_r",
                       title="Yield Farming Breakdown")
    fig1.update_layout(template="plotly_dark", title_x=0.5, margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Gas vs. Trading Metrics")
    fig2 = px.parallel_coordinates(df_defi, color="Gas_Cost_ETH",
                                   dimensions=["Swap_Volume_USD", "Liquidity_USD", "Active_Users", "Gas_Cost_ETH"],
                                   color_continuous_scale="Plasma",
                                   title="Gas vs. Trading Metrics")
    fig2.update_layout(template="plotly_dark", title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Swap Volume VS Liquidity")
df_defi["Day"] = df.index + 1 
filtered_df = df_defi
    
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Swap_Volume_USD"], 
                             fill="tozeroy", name="Swap Volume ($)", mode="lines"))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Liquidity_USD"], 
                             fill="tozeroy", name="Liquidity ($)", mode="lines", opacity=0.5))
    
frames = [go.Frame(data=[
        go.Scatter(x=filtered_df["Date"][:k], y=filtered_df["Swap_Volume_USD"][:k], fill="tozeroy"),
        go.Scatter(x=filtered_df["Date"][:k], y=filtered_df["Liquidity_USD"][:k], fill="tozeroy")
        ]) for k in range(1, len(filtered_df)+1)]
fig.update_layout(title="Swap Volume VS Liquidity", title_x=0.5, height=500)
fig.frames = frames
st.plotly_chart(fig)
        

col3, col4 = st.columns(2)

with col3:
    st.subheader("Whale Trade Distribution")
    pool_filter = st.multiselect("Filter Pools", df_defi["Pool"].unique(), default=df_defi["Pool"].unique())
    filtered_df = df_defi[df_defi["Pool"].isin(pool_filter)]
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#1a1a1a")
    sns.violinplot(x="Pool", y="Whale_Trades", data=filtered_df, ax=ax, palette=["#00b4d8", "#7209b7"])
    ax.set_title("Whale Trade Distribution", color="white")
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
    st.plotly_chart(fig4)

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
    st.subheader("Haul Value by Truck (USD)")
    truck_choice = st.selectbox("Select Truck", df_truck["Truck_ID"].unique())
    filtered_truck = df_truck[df_truck["Truck_ID"] == truck_choice]
    fig9 = px.bar(filtered_truck, x="Date", y="Haul_Value_USD", 
                  title="Haul Value by Truck (USD)", color_discrete_sequence=["#00b4d8"])
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

col13, col14 = st.columns(2)

with col13:
    st.subheader("ETH Price Volatility vs. Haul Value")
    truck_vol = st.selectbox("Truck for Volatility", df_truck["Truck_ID"].unique())
    filtered_vol = df_truck[df_truck["Truck_ID"] == truck_vol]
    fig13 = go.Figure()
    fig13.add_trace(go.Bar(x=filtered_vol["Date"], y=filtered_vol["ETH_Price_USD"], 
                           name="ETH Price (USD)", marker_color="#00b4d8", yaxis="y1"))
    fig13.add_trace(go.Bar(x=filtered_vol["Date"], y=filtered_vol["Haul_Value_USD"], 
                           name="Haul Value (USD)", marker_color="#7209b7", yaxis="y2"))
    fig13.update_layout(template="plotly_dark", title="ETH Price Volatility vs. Haul Value", title_x=0.5,
                        yaxis=dict(title="ETH Price"), yaxis2=dict(title="Haul Value", overlaying="y", side="right"))
    st.plotly_chart(fig13, use_container_width=True)

with col14:
    st.subheader("BTC Transaction Fee Spread")
    truck_btc = st.selectbox("Truck for BTC Fees", df_truck["Truck_ID"].unique())
    filtered_btc = df_truck[df_truck["Truck_ID"] == truck_btc]
    fig14 = px.histogram(filtered_btc, x="BTC_Tx_Fee", nbins=15, 
                         title="BTC Transaction Fee Spread", color_discrete_sequence=["#f72585"])
    fig14.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig14, use_container_width=True)

col15, col16 = st.columns(2)

with col15:
    st.subheader("ETH Wallet Activity by Truck")
    play_wallets = st.button("Animate Wallet Activity")
    fig15 = go.Figure(data=[
        go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_A"]["Date"], 
               y=df_truck[df_truck["Truck_ID"] == "Truck_A"]["ETH_Wallet_Count"], 
               name="Truck_A", marker_color="#00b4d8"),
        go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_B"]["Date"], 
               y=df_truck[df_truck["Truck_ID"] == "Truck_B"]["ETH_Wallet_Count"], 
               name="Truck_B", marker_color="#7209b7"),
        go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_C"]["Date"], 
               y=df_truck[df_truck["Truck_ID"] == "Truck_C"]["ETH_Wallet_Count"], 
               name="Truck_C", marker_color="#f72585")
    ])
    if play_wallets:
        frames = [go.Frame(data=[
            go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_A"]["Date"], 
                   y=df_truck[df_truck["Truck_ID"] == "Truck_A"]["ETH_Wallet_Count"] * (k/5)),
            go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_B"]["Date"], 
                   y=df_truck[df_truck["Truck_ID"] == "Truck_B"]["ETH_Wallet_Count"] * (k/5)),
            go.Bar(x=df_truck[df_truck["Truck_ID"] == "Truck_C"]["Date"], 
                   y=df_truck[df_truck["Truck_ID"] == "Truck_C"]["ETH_Wallet_Count"] * (k/5))
        ]) for k in range(1, 6)]
        fig15.frames = frames
        fig15.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play",
                              method="animate", args=[None, {"frame": {"duration": 500}}])])])
    fig15.update_layout(template="plotly_dark", title="ETH Wallet Activity by Truck", title_x=0.5, barmode="group")
    st.plotly_chart(fig15, use_container_width=True)

with col16:
    st.subheader("BTC Mempool Congestion")
    truck_mempool = st.selectbox("Truck for Mempool", df_truck["Truck_ID"].unique())
    filtered_mempool = df_truck[df_truck["Truck_ID"] == truck_mempool]
    fig16 = px.histogram(filtered_mempool, x="BTC_Mempool_Size_MB", nbins=15, 
                         title="BTC Mempool Congestion", color_discrete_sequence=["#7209b7"])
    fig16.update_layout(template="plotly_dark", title_x=0.5, showlegend=False)
    st.plotly_chart(fig16, use_container_width=True)

st.title(" Trading Volume ")
x = np.linspace(0, 10, 50)
y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) * np.random.rand(50, 50) * 100

fig121 = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Earth")])

fig121.update_layout(title="DeFi Trading Volume Heatmap", title_x=0.4,
                  width=900, height=600, template="plotly_dark")

st.plotly_chart(fig121)


st.title("Crypto Nebula Flux")
st.markdown("A 3D journey through Ethereum and Bitcoin dynamics.")

np.random.seed(42)
dates = pd.date_range("2025-03-01", periods=30, freq="D")
metrics = ["ETH_Price", "BTC_Price", "ETH_TVL", "BTC_TVL", "ETH_Volume", "BTC_Volume"]
df = pd.DataFrame({
    "Date": dates,
    "ETH_Price": 3000 + np.random.randn(30) * 100,
    "BTC_Price": 60000 + np.random.randn(30) * 2000,
    "ETH_TVL": np.random.uniform(5000000, 15000000, 30),
    "BTC_TVL": np.random.uniform(2000000, 8000000, 30),
    "ETH_Volume": np.random.uniform(1000000, 5000000, 30),
    "BTC_Volume": np.random.uniform(800000, 3000000, 30)
})
df["Day"] = df.index + 1

x = metrics
y = dates
z = df[metrics].values.T

fig = go.Figure(data=[go.Surface(
    x=x, y=y, z=z,
    colorscale=[[0, "#2a2a72"], [0.5, "#00d4ff"], [1, "#ff00ff"]],
    showscale=False
)])

frames = [go.Frame(data=[go.Surface(z=df[metrics].iloc[:k+1].values.T)]) for k in range(len(df))]
fig.frames = frames

fig.update_layout(
    template="plotly_dark",
    scene=dict(
        xaxis_title="Metrics",
        yaxis_title="Date",
        zaxis_title="Value",
        bgcolor="#1a1a1a",
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        zaxis=dict(color="white")
    ),
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, {"frame": {"duration": 300, "redraw": True},
                                   "fromcurrent": True, "mode": "immediate"}])]
    )],
    height=700,
    margin=dict(l=0, r=0, t=50, b=0),
    plot_bgcolor="#1a1a1a"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("More Insights Coming...")
