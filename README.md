# House Price Prediction

A machine learning project to predict house prices using features like location, size, and amenities. This project includes a Flask web interface, a CLI tool, and scripts for data generation and model training.

## Features

*   **Prediction Model**: Uses Random Forest Regression (and Linear Regression for comparison) to predict house prices.
*   **Web Interface**: A user-friendly Flask web application for interactive predictions.
*   **CLI Tool**: A command-line interface for quick predictions.
*   **Currency Conversion**: Supports price display in USD and INR.
*   **Visualizations**: Generates plots comparing actual vs. predicted prices.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd House_Price_Prediction
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Data Generation (Optional)
If you don't have the `house_prices.csv` dataset, generate it using:
```bash
python generate_data.py
```
This script creates a synthetic dataset with various features and a target price.

### 2. Model Training
Train the machine learning models:
```bash
python model.py
```
This script:
*   Loads and preprocesses the data.
*   Trains Linear Regression and Random Forest models.
*   Evaluates the models (RMSE, R2 Score).
*   Saves the best model (`rf_model.pkl`) and column names (`model_columns.pkl`).
*   Generates evaluation plots (`lr_results.png`, `rf_results.png`).

### 3. Run the Web Application
Start the Flask server:
```bash
python app.py
```
*   Open your browser and navigate to `http://127.0.0.1:5000`.
*   Enter the house details (bedrooms, bathrooms, sqft, etc.) and click "Predict".

### 4. CLI Prediction
Run predictions directly from the terminal:
```bash
python predict.py
```
Follow the prompts to enter house details and get a price estimate.

## Project Structure

*   `app.py`: Flask application for the web interface.
*   `model.py`: Script for training and evaluating the ML models.
*   `predict.py`: CLI script for user input and prediction.
*   `generate_data.py`: Script to generate synthetic training data.
*   `templates/index.html`: HTML template for the web interface.
*   `static/`: Contains CSS and JavaScript files.
*   `rf_model.pkl`: key file containing the trained Random Forest model.
*   `model_columns.pkl`: key file containing the columns used during training.
