import streamlit as st
import numpy as np
import joblib 
import requests
from sklearn.preprocessing import PolynomialFeatures

def download_model(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        with open(filename, "wb") as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading model from {url}: {e}")
        return None
    return filename

url_poly_model = "https://github.com/aniketyadav16/-Data-Science/raw/main/Model/polynomial_model.joblib"
url_logistic_model = "https://github.com/aniketyadav16/-Data-Science/raw/main/Model/logistic_model.joblib"

poly_model_file = download_model(url_poly_model, "poly_model.joblib")
logistic_model_file = download_model(url_logistic_model, "log_model.joblib")

if poly_model_file:
    linear_mod = joblib.load(poly_model_file)
else:
    st.error("Polynomial model could not be loaded. Exiting...")

if logistic_model_file:
    logistic_mod = joblib.load(logistic_model_file)
else:
    st.error("Logistic model could not be loaded. Exiting...")

poly = PolynomialFeatures(degree=4)

st.header("Input Features")
feature_1 = st.number_input("Enter Carat")
feature_2 = st.number_input("Enter Length Of The Diamond")
feature_3 = st.number_input("Enter Width Of The Diamond")
feature_4 = st.number_input("Enter Depth Of The Diamond")

if feature_2 == 0 and feature_3 == 0:
    st.warning("Please enter non-zero values for Length and Width.")
    feature_5 = 0
else:
    feature_5 = feature_4 / ((feature_2 + feature_3) / 2) if (feature_2 + feature_3) != 0 else 0


if st.button("Predict"):
    if feature_5 != 0:
        input_data = np.array([[feature_1, feature_5, feature_2, feature_3, feature_4]])
        input_data = poly.fit_transform(input_data)
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
