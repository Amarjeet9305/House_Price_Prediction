import pandas as pd
import joblib
import numpy as np

def get_user_input():
    print("\n--- House Price Prediction ---")
    print("Please enter the details of the house:")
    
    try:
        bedrooms = int(input("Number of Bedrooms (e.g., 3): "))
        bathrooms = int(input("Number of Bathrooms (e.g., 2): "))
        sqft_living = int(input("Square Feet Living Area (e.g., 1500): "))
        floors = float(input("Number of Floors (e.g., 1, 1.5, 2): "))
        age = int(input("Age of the house (years): "))
        
        waterfront_in = input("Waterfront View? (y/n): ").lower()
        waterfront = 1 if waterfront_in == 'y' else 0
        
        garage_in = input("Has Garage? (y/n): ").lower()
        garage = 1 if garage_in == 'y' else 0
        
        garden_in = input("Has Garden? (y/n): ").lower()
        garden = 1 if garden_in == 'y' else 0
        
        print("\nLocations: Suburb, City Center, Rural")
        location = input("Enter Location: ").strip()
        
    except ValueError:
        print("Invalid input for numerical values. Please try again.")
        return None

    return {
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'SquareFeet': sqft_living,
        'Floors': floors,
        'Age': age,
        'Waterfront': waterfront,
        'Garage': garage,
        'Garden': garden,
        'Location': location
    }

def predict_price():
    # Load model and columns
    try:
        model = joblib.load('rf_model.pkl')
        model_columns = joblib.load('model_columns.pkl')
    except FileNotFoundError:
        print("Error: Model files not found. Please run model.py first.")
        return

    # Get user input
    user_input = get_user_input()
    if user_input is None:
        return

    # Create DataFrame
    input_df = pd.DataFrame([user_input])
    
    # One-hot encode
    # Note: We need to handle the case where the user inputs a location that wasn't in training,
    # or ensure we encode it similarly. 
    # Since we used pd.get_dummies(drop_first=True) in training, we need to match that.
    
    input_df_encoded = pd.get_dummies(input_df, columns=['Location'])
    
    # Align with model columns
    # This ensures all columns from training exist, filling missing ones with 0
    # and removing any extra ones (if any)
    input_df_encoded = input_df_encoded.reindex(columns=model_columns, fill_value=0)
    
    # Predict
    predicted_price = model.predict(input_df_encoded)[0]
    
    print(f"\nPredicted House Price: ${predicted_price:,.2f}")

if __name__ == "__main__":
    predict_price()
