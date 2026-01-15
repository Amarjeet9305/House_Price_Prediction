import pandas as pd
import numpy as np
import random

def generate_house_data(n_samples=1000):
    np.random.seed(42)
    
    # Features
    bedrooms = np.random.randint(1, 6, n_samples)
    bathrooms = np.random.randint(1, 4, n_samples)
    sqft_living = np.random.randint(500, 5000, n_samples)
    floors = np.random.choice([1, 1.5, 2, 2.5, 3], n_samples)
    age = np.random.randint(0, 100, n_samples)
    
    # Amenities (0 or 1)
    waterfront = np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
    garage = np.random.choice([0, 1], n_samples, p=[0.2, 0.8])
    garden = np.random.choice([0, 1], n_samples, p=[0.4, 0.6])
    
    # Locations: encode as dummy multiplier effect for price
    locations = ['Suburb', 'City Center', 'Rural']
    location_cat = np.random.choice(locations, n_samples)
    
    # Price Calculation (Base price + feature coefficients + random noise)
    base_price = 50000
    price = (
        base_price +
        (bedrooms * 20000) +
        (bathrooms * 15000) +
        (sqft_living * 200) +
        (floors * 5000) -
        (age * 500) +
        (waterfront * 150000) +
        (garage * 10000) +
        (garden * 5000)
    )
    
    # Add location effect
    location_multipliers = {'Suburb': 1.0, 'City Center': 1.5, 'Rural': 0.8}
    price = [p * location_multipliers[loc] for p, loc in zip(price, location_cat)]
    
    # Add some noise
    noise = np.random.normal(0, 25000, n_samples)
    price = price + noise
    
    # Create DataFrame
    data = pd.DataFrame({
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'SquareFeet': sqft_living,
        'Floors': floors,
        'Age': age,
        'Waterfront': waterfront,
        'Garage': garage,
        'Garden': garden,
        'Location': location_cat,
        'Price': price
    })
    
    return data

if __name__ == "__main__":
    df = generate_house_data()
    output_file = 'house_prices.csv'
    df.to_csv(output_file, index=False)
    print(f"Data generated and saved to {output_file}")
    print(df.head())
