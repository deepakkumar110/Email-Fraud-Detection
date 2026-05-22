import streamlit as st
import requests

# =========================
# PAGE TITLE
# =========================

st.title("📧 Email Fraud Detection System")

st.write(
    "This project detects whether an email is Spam/Fraud or Safe using Machine Learning."
)

# =========================
# USER INPUT
# =========================

email_text = st.text_area("Enter Email Text")

# =========================
# PREDICTION BUTTON
# =========================

if st.button("Predict"):

    if email_text.strip() == "":

        st.warning("Please enter email text.")

    else:

        data = {

            "email_text": email_text
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=data
            )

            result = response.json()

            if result["prediction"] == "Spam":

                st.error(
                    f"🚨 Spam / Fraud Email "
                    f"({result['confidence']}% confidence)"
                )

            else:

                st.success(
                    f"✅ Safe / Genuine Email "
                    f"({result['confidence']}% confidence)"
                )

        except:

            st.error("❌ FastAPI Backend Not Running")