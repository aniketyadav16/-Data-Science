import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from joblib import load

linear_mod = load('Model/linear_model.joblib')
logistic_mod = load('Model/logistic_model.joblib')

poly = PolynomialFeatures(degree=4)
st.header("Input Features")
feature_1 = st.slider("Select Carat", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
feature_2 = st.slider("Select Length Of The Diamond", min_value=0, max_value=40, value=0, step=1)
feature_3 = st.slider("Select Width Of The Diamond", min_value=0, max_value=40, value=0, step=1)
feature_4 = st.slider("Select Depth Of The Diamond", min_value=0, max_value=40, value=0, step=1)
Price = st.number_input("Enter The Price:")

if feature_2 == 0 and feature_3 == 0:
    st.warning("Please enter non-zero values for Length and Width.")
    feature_5 = 0
else:
    feature_5 = ((feature_4 / ((feature_2 + feature_3)/2)) * 100)
feature_5 = round(feature_5,1)
st.write(f"feature 5: {feature_5}")

if st.button("Predict Price"):
    if feature_5 != 0:
        input_data = np.array([[feature_1, feature_5, feature_2, feature_3, feature_4]])
        linear_pred = linear_mod.predict(input_data)
        if linear_pred < 0:
            linear_pred = (-1)*(linear_pred)
        else:
            linear_pred = linear_pred
        st.subheader(f"Predicted Price Is: ${linear_pred[0].round()}")
    else:
        st.error("Cannot predict due to invalid input values.")
        

if st.button("Recommendation"):
    if feature_5 != 0:
        input_data2 = np.array([[Price, feature_1, feature_5, feature_2, feature_3, feature_4]])
        logistic_pred = logistic_mod.predict(input_data2)
        if logistic_pred == [1]:
            logistic_pred = "It is Recommended To BUY this DIAMOND!!"
        else:
            logistic_pred = "Do NOT Buy This DIAMOND"
        st.subheader(logistic_pred)
    else:
        st.error("Cannot provide a recommendation due to invalid input values.")
