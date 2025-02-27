import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")  

st.title("Interactive Dashboard with Streamlit & Plotly")


st.subheader("Polar Chart - Wind Data")
df44 = px.data.wind()
fig1 = px.bar_polar(df44, r="frequency", theta="direction", color="strength",
                    color_discrete_sequence=px.colors.sequential.Plasma_r,
                    title="Polar Chart",
                    template='plotly_dark')
fig1.update_layout(width=1000, height=800)
st.plotly_chart(fig1)


st.subheader("US Export of Plastic Scrap")
years = list(range(1995, 2013))
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=years,
                y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263, 350, 430, 474, 526, 488, 537, 500, 439],
                name='Rest of world',
                marker_color='rgb(55, 83, 109)'))
fig2.add_trace(go.Bar(x=years,
                y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270, 299, 340, 403, 549, 499],
                name='China',
                marker_color='rgb(26, 118, 255)'))
fig2.update_layout(title="US Export of Plastic Scrap",
                   xaxis_tickfont_size=14,
                   yaxis=dict(title="USD (millions)", tickfont_size=14),
                   legend=dict(x=0, y=1.0, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
                   barmode='group', bargap=0.15, bargroupgap=0.1,
                   height=500, width=1400)
st.plotly_chart(fig2)


st.subheader("World Population Treemap (2007)")
df3 = px.data.gapminder().query("year == 2007")
fig3 = px.treemap(df3, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                   color='lifeExp', hover_data=['iso_alpha'],
                   title='Treemap of Population Distribution',
                   color_continuous_scale='tropic',
                   color_continuous_midpoint=np.average(df3['lifeExp'], weights=df3['pop']))
fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig3)


st.subheader("Stock Performance Analysis")
df4 = px.data.stocks(indexed=True, datetimes=True)
fig4 = px.scatter(df4, trendline="rolling", trendline_options=dict(window=5),
                  title="Stock Performance")
fig4.data = [t for t in fig4.data if t.mode == "lines"]
fig4.update_traces(showlegend=True)
fig4.update_layout(width=1300, height=500)
st.plotly_chart(fig4)


st.subheader("Customer Satisfaction Across Service Channels")
data222 = {
    'ease_of_use': [80, 70, 65],
    'responsiveness': [75, 85, 90],
    'quality_of_service': [85, 80, 75],
    'overall_satisfaction': [78, 83, 82]
}
df5 = pd.DataFrame(data222)
df5['Row'] = ['Online', 'In-Store', 'Phone support']
df_melted = df5.melt(id_vars='Row', value_vars=df5.columns[:-1], var_name='Category', value_name='Value')

fig5 = px.line_polar(df_melted, r='Value', theta='Category', color='Row', line_close=True, 
                     template='plotly_dark', markers='X',
                     title="Customer Satisfaction Levels Across Different Service Channels",
                     color_discrete_map={'Online': 'mediumorchid', 'In-Store': 'skyblue', 'Phone Support': 'sandybrown'})
fig5.update_layout(height=850, width=1200)
st.plotly_chart(fig5)

st.subheader("Environmental Impact of Energy Sources")
grp1 = {
    "metric": ["Carbon Emissions", "Land Use", "Water Use", "Air Pollution", "Waste Generation"],
    "solar": [2, 4, 3, 1, 2],
    "coal": [10, 3, 8, 10, 9],
    "nuclear": [3, 2, 5, 3, 7]
}
grp1 = pd.DataFrame(grp1)
grp1 = grp1.melt(id_vars='metric', var_name='Type', value_name='Num')

fig6 = px.line_polar(grp1, r='Num', theta='metric', color='Type', line_close=True, 
                     line_shape='spline', markers='o',
                     color_discrete_map={'solar': 'lightpink', 'coal': 'burlywood', 'nuclear': 'skyblue'},
                     template='plotly_dark')
st.plotly_chart(fig6)