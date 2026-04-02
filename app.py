import streamlit as st
import pickle
import pandas as pd

# Load saved model and features
model = pickle.load(open('models/model.pkl', 'rb'))
features = pickle.load(open('models/features.pkl', 'rb'))

# App title and description
st.title("📧 Email Fraud Detection System")
st.write(
    "This project detects whether an email is Spam/Fraud or Safe using Machine Learning."
)

# User input
email_text = st.text_area("Enter Email Text")

# Prediction
if st.button("Predict"):

    if email_text.strip() == "":
        st.warning("Please enter some email text.")
    else:
        # Create input dictionary with all features = 0
        input_data = {word: 0 for word in features}

        # Count words from user input
        for word in email_text.lower().split():
            if word in input_data:
                input_data[word] += 1

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])

        # Predict
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)

        # Show result
        if prediction[0] == 1:
            st.error(
                f"🚨 Fraud / Spam Email ({probability[0][1] * 100:.2f}% confidence)"
            )
        else:
            st.success(
                f"✅ Safe / Genuine Email ({probability[0][0] * 100:.2f}% confidence)"
            )