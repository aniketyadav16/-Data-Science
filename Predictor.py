import streamlit as st
import pickle
import numpy as np

from joblib import load

linear_mod = load('linear_model.joblib')
logistic_mod = load('logistic_model.joblib')

st.header("Input Features")
feature_1 = st.number_input("Enter Carat")
feature_2 = st.number_input("Enter Length Of The Diamond")
feature_3 = st.number_input("Enter Width Of The Diamond")
feature_4 = st.number_input("Enter Depth Of The Diamond")

# Calculate Feature 5 (Depth Ratio)
if feature_2 == 0 and feature_3 == 0:
    st.warning("Please enter non-zero values for Length and Width.")
    feature_5 = 0
else:
    feature_5 = feature_4 / ((feature_2 + feature_3) / 2) if (feature_2 + feature_3) != 0 else 0

st.write(f"Feature 5 (Depth Ratio): {feature_5}")

if feature_5 == 0:
    st.warning("Feature 5 is invalid. Please check your inputs.")

if st.button("Predict"):
    if feature_5 != 0:
        input_data = np.array([[feature_1, feature_5, feature_2, feature_3, feature_4]])
        linear_pred = linear_mod.predict(input_data)
        st.subheader(f"Predicted Price: ${linear_pred[0].round()}k")
    else:
        st.error("Cannot predict due to invalid input values.")

if st.button("Recommendation"):
    price = st.number_input("Enter Price:")
    if feature_5 != 0:
        input_data2 = np.array([[price, feature_1, feature_5, feature_2, feature_3, feature_4]])
        logistic_pred = logistic_mod.predict(input_data2)
        if logistic_pred == [1]:
            logistic_pred = "It is Recommended To BUY this DIAMOND!!"
        else:
            logistic_pred = "Do NOT Buy This DIAMOND"
        st.subheader(logistic_pred)
    else:
        st.error("Cannot provide a recommendation due to invalid input values.")
