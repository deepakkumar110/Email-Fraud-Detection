from fastapi import FastAPI
from pydantic import BaseModel
from backend.database import conn, cursor

import pickle
import pandas as pd

# =========================
# LOAD MODEL
# =========================

model = pickle.load(open('models/model.pkl', 'rb'))
features = pickle.load(open('models/features.pkl', 'rb'))

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# INPUT SCHEMA
# =========================

class EmailInput(BaseModel):
    email_text: str

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "Email Fraud Detection API Running"
    }

# =========================
# PREDICTION ROUTE
# =========================

@app.post("/predict")
def predict(data: EmailInput):

    email_text = data.email_text.lower()

    input_data = {word: 0 for word in features}

    for word in email_text.split():

        if word in input_data:

            input_data[word] += 1

    input_df = pd.DataFrame([input_data])

    # =========================
    # MODEL PREDICTION
    # =========================

    prediction = model.predict(input_df)

    probability = model.predict_proba(input_df)

    # =========================
    # RESULT
    # =========================

    if prediction[0] == 1:

        result = "Spam"

        confidence = probability[0][1] * 100

    else:

        result = "Safe"

        confidence = probability[0][0] * 100

    # =========================
    # SAVE TO MYSQL
    # =========================

    query = """
    INSERT INTO predictions
    (email_text, prediction, confidence)
    VALUES (%s, %s, %s)
    """

    values = (
        email_text,
        result,
        confidence
    )

    cursor.execute(query, values)

    conn.commit()

    # =========================
    # RETURN RESPONSE
    # =========================

    return {

        "prediction": result,

        "confidence": round(confidence, 2)
    }