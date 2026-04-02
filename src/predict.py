import pickle

model = pickle.load(open('../models/model.pkl', 'rb'))
features = pickle.load(open('../models/features.pkl', 'rb'))

email_text = input("Enter Email Text: ").lower()

import pandas as pd

input_data = {word: 0 for word in features}

for word in email_text.split():
    if word in input_data:
        input_data[word] += 1

input_df = pd.DataFrame([input_data])

prediction = model.predict(input_df)

if prediction[0] == 1:
    print("Fraud / Spam Email")
else:
    print("Safe / Genuine Email")