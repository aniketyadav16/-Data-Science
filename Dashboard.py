import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Interactive Dashboard with Plotly")

st.markdown("## DeFi Pulse Explorer: Dashboard")
st.link_button("For The DeFi Data Dashboard CLICK HERE!", "https://vizzardd.streamlit.app")

st.subheader("Running Scatter Plot")


df = px.data.gapminder()

fig11 = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                 size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=60, title="GDP vs Life Expectancy Over Time",
                 template="plotly_dark") 
fig11.update_layout(yaxis=dict(range=[30, 100]), height=500)
st.plotly_chart(fig11)

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

st.subheader("Influencer Performance over 12 Months")

a3 = {
    "date": [
        "2023-01-31", "2023-02-28", "2023-03-31", "2023-04-30", "2023-05-31", "2023-06-30", "2023-07-31",
        "2023-08-31", "2023-09-30", "2023-10-31", "2023-11-30", "2023-12-31",
        "2023-01-31", "2023-02-28", "2023-03-31", "2023-04-30", "2023-05-31", "2023-06-30", "2023-07-31",
        "2023-08-31", "2023-09-30", "2023-10-31", "2023-11-30", "2023-12-31",
        "2023-01-31", "2023-02-28", "2023-03-31", "2023-04-30", "2023-05-31", "2023-06-30", "2023-07-31",
        "2023-08-31", "2023-09-30", "2023-10-31", "2023-11-30", "2023-12-31"
    ],
    "influencer": [
        "Influencer A"] * 12 + ["Influencer B"] * 12 + ["Influencer C"] * 12,
    "followers": [
        3732, 7339, 9992, 14256, 16091, 17854, 20585, 25016, 27049, 31844, 33121, 35899,
        3328, 7475, 12117, 17161, 21309, 26277, 30139, 32344, 37402, 41501, 45136, 48858,
        4872, 8969, 11870, 13607, 17700, 21020, 25045, 28185, 31548, 33724, 35679, 40660
    ]
}
a3 = pd.DataFrame(a3)
a3['date'] = pd.to_datetime(a3['date'])
a3['month'] = a3['date'].dt.month
fig8 = px.bar(
    a3,
    x='influencer',
    color='followers',
    y='followers',
    animation_frame='month',
    color_continuous_scale='tropic',
    width=10,
    template='plotly_dark'
)
fig8.update_layout(height=600, width=500, transition = {'duration':1000})
st.plotly_chart(fig8)



st.subheader("World Population Treemap (2007)")
df3 = px.data.gapminder().query("year == 2007")
fig3 = px.treemap(df3, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                   color='lifeExp', hover_data=['iso_alpha'],
                   title='Treemap of Population Distribution',
                   color_continuous_scale='tealrose',
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
                     color_discrete_map={'Online': 'mistyrose', 'In-Store': 'skyblue', 'Phone Support': 'salmon'})
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
fig6.update_layout(height=850, width=1200)
st.plotly_chart(fig6)



st.subheader('Crypto Performace Analysis')
plt.style.use('dark_background')
labels = ['Bitcoin', 'Ethereum', 'Ripple']
sizes = [45, 30, 25]
colors = ['gold', 'plum', 'burlywood']

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
fig, ax = plt.subplots(figsize=(2,2), subplot_kw=dict(polar=True))

ax.bar(angles, sizes, width=0.3, color=colors, align='edge')

ax.set_xticks(angles)
ax.set_xticklabels(labels)
ax.set_title("Polar Chart")
st.title("Polar Chart in Streamlit")
st.pyplot(fig)

plt.style.use('default')
st.subheader("Gapmider: 2007 GDP Analysis")
df00 = px.data.gapminder()
df_2007 = df00.query("year==2007")

for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
    fig9 = px.scatter(df_2007,
                     x="gdpPercap", y="lifeExp", size="pop", color="continent",
                     log_x=True, size_max=60,
                     template=template, title="Gapminder 2007 GDP")
    fig9.update_layout(height=550, width=1200)
    st.plotly_chart(fig9)

a7 = {
    'profession': ['Software Engineer', 'Software Engineer', 'Software Engineer', 
                   'Data Scientist', 'Data Scientist', 'Data Scientist', 
                   'UX Designer', 'UX Designer', 'UX Designer'],
    'annual_salary': [138268, 113567, 112613, 115891, 91243, 111993, 125026, 118600, 109512]
}
a7 = pd.DataFrame(a7)
st.subheader('Profession Vs Salary Analysis')
fig10 = px.box(a7, x='profession', y='annual_salary', color='profession', 
             color_discrete_map={'Software Engineer': 'cyan', 'Data Scientist': 'magenta', 'UX Designer': 'yellowgreen'}, 
             points='all', template='plotly_dark')
fig10.update_layout(height=550, width=1200)
st.plotly_chart(fig10)



years = np.array(['2012', '2013', '2014', '2015'])

sales_africa = np.array([127187.27, 144480.70, 229068.79, 283036.44])

sales_USCA = np.array([492756.60, 486629.30, 627634.98, 757108.13])

sales_LATAM = np.array([385098.15, 464733.29, 608140.77, 706632.93])

sales_Asia_Pacific = np.array([713658.22, 863983.97, 1092231.65, 1372784.40])

sales_Europe = np.array([540750.63, 717611.40, 848670.24, 1180303.95])

fig, ax = plt.subplots(ncols=4, sharey=True, figsize=(20.5, 5.5))
st.subheader('Multi-Region Sales')

europe, = ax[0].plot(years, sales_Europe, color="red", label="Europe")
ax[0].set_title('Sales in Europe')
ax[1].bar(years, sales_USCA, label="USCA")
ax[1].set_title('Sales in USCA')
ax[2].scatter(years, sales_africa, label="Africa")
ax[2].set_title('Sales in Africa')

asia = ax[3].bar(years, sales_Asia_Pacific, width=0.5, color='royalblue', label="Asia Pacific")
latam = ax[3].bar(years, sales_LATAM, width=0.5, color='seagreen', bottom=sales_Asia_Pacific, label="LATAM")

ax[3].set_title('Sales in Asia Pacific and LATAM')
ax[3].legend()

st.pyplot(fig)

