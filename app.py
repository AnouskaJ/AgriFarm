from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

model = pickle.load(open('best_model.sav', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    state = data['state']
    district = data['district']
    market = data['market']
    commodity = data['commodity']
    
    # Convert categorical data to numerical data using label encoder
    label_encoder = LabelEncoder()
    market = label_encoder.fit_transform(pd.Series(market))
    commodity = label_encoder.fit_transform(pd.Series(commodity))

    # Create a dataframe with the user input
    input_data = pd.DataFrame({
        'State': [state],
        'District': [district],
        'Market': [market],
        'Commodity': [commodity],
        'Min Price': [min_price],
        'Max Price': [max_price]
    })

    # Scale the input data using the StandardScaler that we fitted earlier
    ss=StandardScaler()
    input_data_scaled=ss.fit_transform(input_data)

    # Make a prediction using the loaded model
    prediction = model.predict(input_data_scaled)[0]

    # Render the prediction on the results page
    return render_template('results.html', prediction=prediction)

