from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load model and columns
MODEL_PATH = 'rf_model.pkl'
COLUMNS_PATH = 'model_columns.pkl'

if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)
    print("Model and columns loaded successfully.")
else:
    print("Error: Model files not found. Please run model.py first.")
    model = None
    model_columns = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or model_columns is None:
        return jsonify({'error': 'Model not loaded properly.'}), 500

    try:
        data = request.json
        
        # Prepare input data
        input_data = {
            'Bedrooms': int(data['bedrooms']),
            'Bathrooms': int(data['bathrooms']),
            'SquareFeet': int(data['sqft']),
            'Floors': float(data['floors']),
            'Age': int(data['age']),
            'Waterfront': 1 if data['waterfront'] else 0,
            'Garage': 1 if data['garage'] else 0,
            'Garden': 1 if data['garden'] else 0,
            'Location': data['location']
        }
        
        # Create DataFrame
        input_df = pd.DataFrame([input_data])
        
        # One-hot encode
        input_df_encoded = pd.get_dummies(input_df, columns=['Location'])
        
        # Align with model columns
        input_df_encoded = input_df_encoded.reindex(columns=model_columns, fill_value=0)
        
        # Predict
        prediction = model.predict(input_df_encoded)[0]
        
        # Currency Conversion
        currency = data.get('currency', 'USD')
        if currency == 'INR':
            # Approximation: 1 USD = 84 INR
            prediction = prediction * 84
            formatted_prediction = f"₹{prediction:,.2f}"
        else:
            formatted_prediction = f"${prediction:,.2f}"
        
        return jsonify({'prediction': formatted_prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
