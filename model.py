import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)
    
    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['Location'], drop_first=True)
    
    # Features and Target
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    return X, y

def train_and_evaluate(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    
    print("Linear Regression Results:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr))}")
    print(f"R2 Score: {r2_score(y_test, y_pred_lr)}")
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train) # Tree-based models don't strictly need scaling, but it's fine
    y_pred_rf = rf.predict(X_test)
    
    print("\nRandom Forest Results:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf))}")
    print(f"R2 Score: {r2_score(y_test, y_pred_rf)}")
    
    print(f"R2 Score: {r2_score(y_test, y_pred_rf)}")
    
    return y_test, y_pred_lr, y_pred_rf, lr, rf

def plot_results(y_test, y_pred, title, filename):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title(title)
    plt.savefig(filename)
    print(f"Saved plot to {filename}")

if __name__ == "__main__":
    data_path = 'house_prices.csv'
    
    # Check if data exists
    import os
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run generate_data.py first.")
    else:
        print("Loading data...")
        X, y = load_and_preprocess_data(data_path)
        
        print("Training models...")
        y_test, y_pred_lr, y_pred_rf, lr, rf = train_and_evaluate(X, y)
        
        print("Plotting results...")
        plot_results(y_test, y_pred_lr, 'Linear Regression: Actual vs Predicted', 'lr_results.png')
        plot_results(y_test, y_pred_rf, 'Random Forest: Actual vs Predicted', 'rf_results.png')
        
        # Save model and columns
        import joblib
        print("Saving model and columns...")
        joblib.dump(rf, 'rf_model.pkl')
        joblib.dump(X.columns, 'model_columns.pkl')
        print("Model saved to rf_model.pkl")
        print("Model columns saved to model_columns.pkl")
