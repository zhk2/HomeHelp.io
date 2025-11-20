# -*- coding: utf-8 -*-
"""Real Estate Price Prediction Model - Adapted from X-ray CNN approach

Using the same TensorFlow structure but for tabular real estate data instead of images
"""

# Free installations - same as your X-ray model
# pip install tensorflow pandas scikit-learn matplotlib numpy

import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# ================================
# 1) GET FREE REAL ESTATE DATA
# ================================

def download_free_real_estate_data():
    """Download free real estate datasets - no API keys needed"""
    
    # Option 1: Use built-in sample data for testing
    print("Creating sample real estate dataset...")
    
    # Generate synthetic but realistic data based on real patterns
    np.random.seed(42)
    n_samples = 10000
    
    data = {
        'sqft': np.random.normal(2000, 800, n_samples).clip(500, 8000),
        'bedrooms': np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.1, 0.2, 0.3, 0.25, 0.1, 0.05]),
        'bathrooms': np.random.normal(2.5, 1, n_samples).clip(1, 6),
        'age': np.random.exponential(20, n_samples).clip(0, 100),
        'lot_size': np.random.lognormal(8, 0.5, n_samples).clip(1000, 50000),
        'garage': np.random.choice([0, 1, 2, 3], n_samples, p=[0.1, 0.3, 0.5, 0.1]),
    }
    
    # Create location-based price multipliers
    location_multipliers = np.random.choice([0.8, 1.0, 1.2, 1.5, 2.0], n_samples, p=[0.2, 0.3, 0.3, 0.15, 0.05])
    
    # Calculate price based on realistic factors
    base_price = (
        data['sqft'] * 150 +  # $150 per sqft base
        data['bedrooms'] * 10000 +  # $10k per bedroom
        data['bathrooms'] * 8000 +   # $8k per bathroom
        data['garage'] * 5000 +      # $5k per garage spot
        data['lot_size'] * 2 -       # $2 per sqft lot
        data['age'] * 1000           # -$1k per year old
    )
    
    # Add location multiplier and some noise
    data['price'] = (base_price * location_multipliers * 
                    np.random.normal(1, 0.1, n_samples)).clip(50000, 2000000)
    
    # Add categorical features
    data['property_type'] = np.random.choice(['House', 'Condo', 'Townhouse'], n_samples, p=[0.7, 0.2, 0.1])
    data['location_score'] = location_multipliers  # Use as numeric feature
    
    df = pd.DataFrame(data)
    
    # Save to CSV for reuse
    df.to_csv('real_estate_data.csv', index=False)
    print(f"Created dataset with {len(df)} properties")
    return df

# ================================
# 2) DATA PREPROCESSING 
# ================================

def prepare_real_estate_data(df):
    """Prepare data - similar to image preprocessing in X-ray model"""
    
    # Handle categorical variables (like image classes)
    le = LabelEncoder()
    df['property_type_encoded'] = le.fit_transform(df['property_type'])
    
    # Select features (like selecting image channels)
    feature_columns = [
        'sqft', 'bedrooms', 'bathrooms', 'age', 'lot_size', 
        'garage', 'property_type_encoded', 'location_score'
    ]
    
    X = df[feature_columns].values
    y = df['price'].values
    
    # Normalize features (like rescaling images to 0-1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data (like train/validation split in X-ray model)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test, scaler, le

# ================================
# 3) MODEL DEFINITION (Adapted from your CNN)
# ================================

def create_real_estate_model(input_shape):
    """Create neural network - adapted from your CNN architecture"""
    
    # Instead of Conv2D layers for images, use Dense layers for tabular data
    model = models.Sequential([
        # Input layer (like your Conv2D input)
        layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        layers.Dropout(0.3),
        
        # Hidden layers (similar to your Conv2D + MaxPooling pattern)
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.2),
        
        # Output layer - regression instead of binary classification
        layers.Dense(1, activation='linear')  # Linear for price prediction
    ])
    
    # Compile model - adapted for regression
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',  # Use full name for compatibility
        metrics=['mean_absolute_error']  # Use full name for compatibility
    )
    
    return model

# ================================
# 4) TRAINING (Same structure as X-ray model)
# ================================

def train_model():
    """Main training function - same structure as your X-ray training"""
    
    print("Loading and preparing data...")
    df = download_free_real_estate_data()
    X_train, X_val, X_test, y_train, y_val, y_test, scaler, le = prepare_real_estate_data(df)
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Create model
    print("Creating model...")
    input_shape = X_train.shape[1]
    model = create_real_estate_model(input_shape)
    model.summary()
    
    # Train model - same callbacks as your X-ray model
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,  # More epochs since we have tabular data
        batch_size=32,
        callbacks=[
            tf.keras.callbacks.ReduceLROnPlateau(patience=5, factor=0.5),
            tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
        ],
        verbose=1
    )
    
    # Evaluate model
    print("Evaluating model...")
    test_predictions = model.predict(X_test)
    test_mae = mean_absolute_error(y_test, test_predictions)
    test_r2 = r2_score(y_test, test_predictions)
    
    print(f"Test MAE: ${test_mae:,.0f}")
    print(f"Test R²: {test_r2:.3f}")
    
    # Save model - same as your X-ray model
    print("Saving model...")
    model.save('real_estate_model.h5', save_format='h5')
    
    # Save preprocessors
    import joblib
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(le, 'label_encoder.pkl')
    
    # Plot training history
    plot_training_history(history)
    
    return model, scaler, le, history

def plot_training_history(history):
    """Plot training curves - similar to your X-ray model evaluation"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss curve
    ax1.plot(history.history['loss'], label='Training Loss')
    ax1.plot(history.history['val_loss'], label='Validation Loss')
    ax1.set_title('Model Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    
    # MAE curve
    ax2.plot(history.history['mean_absolute_error'], label='Training MAE')
    ax2.plot(history.history['val_mean_absolute_error'], label='Validation MAE')
    ax2.set_title('Model MAE')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('MAE')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

# ================================
# 5) PREDICTION FUNCTION FOR YOUR ZILLOW APP
# ================================

def load_trained_model():
    """Load the trained model for use in your Zillow app"""
    import joblib
    import os
    
    try:
        # Check if model files exist
        if not os.path.exists('real_estate_model.h5'):
            raise FileNotFoundError("Model file not found. Please train the model first.")
        
        if not os.path.exists('scaler.pkl'):
            raise FileNotFoundError("Scaler file not found. Please train the model first.")
            
        if not os.path.exists('label_encoder.pkl'):
            raise FileNotFoundError("Label encoder file not found. Please train the model first.")
        
        # Load model with custom objects if needed
        model = tf.keras.models.load_model(
            'real_estate_model.h5',
            custom_objects={
                'mse': 'mean_squared_error',
                'mae': 'mean_absolute_error'
            }
        )
        scaler = joblib.load('scaler.pkl')
        le = joblib.load('label_encoder.pkl')
        
        return model, scaler, le
        
    except Exception as e:
        print(f"Error loading trained model: {e}")
        print("Please train the model first by running the train_model() function")
        raise e

def predict_house_price(sqft, bedrooms, bathrooms, age, lot_size, garage, property_type, location_score):
    """Predict house price - use this in your Zillow app API"""
    
    # Load trained model
    model, scaler, le = load_trained_model()
    
    # Encode property type
    property_type_encoded = le.transform([property_type])[0]
    
    # Prepare features
    features = np.array([[sqft, bedrooms, bathrooms, age, lot_size, garage, property_type_encoded, location_score]])
    
    # Scale features
    features_scaled = scaler.transform(features)
    
    # Make prediction
    prediction = model.predict(features_scaled)
    
    return float(prediction[0][0])

# ================================
# 6) EXAMPLE USAGE
# ================================

if __name__ == "__main__":
    # Check if model files exist before training
    import os
    
    if not os.path.exists('real_estate_model.h5'):
        print("No trained model found.")
        print("Please run 'python train_model_simple.py' first to train the model.")
        print("Then you can use this script for advanced features.")
    else:
        print("Model found! Testing prediction...")
        
        try:
            # Test prediction
            predicted_price = predict_house_price(
                sqft=2000,
                bedrooms=3,
                bathrooms=2,
                age=10,
                lot_size=8000,
                garage=2,
                property_type='House',
                location_score=1.2
            )
            
            print(f"✅ Prediction successful: ${predicted_price:,.0f}")
            
            # Optionally retrain
            retrain = input("Do you want to retrain the model with more data? (y/n): ")
            if retrain.lower() == 'y':
                model, scaler, le, history = train_model()
                
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            print("The model might be corrupted. Please retrain by running:")
            print("python train_model_simple.py")