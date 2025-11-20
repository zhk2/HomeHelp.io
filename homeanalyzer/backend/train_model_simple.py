#!/usr/bin/env python3
"""
Simple script to train the real estate model
Run this FIRST before using the main zillow_ai_model.py
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

def create_sample_data():
    """Create sample real estate data for training"""
    print("Creating sample training data...")
    
    np.random.seed(42)
    n_samples = 5000
    
    data = {
        'sqft': np.random.normal(2000, 800, n_samples).clip(500, 8000),
        'bedrooms': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.4, 0.25, 0.05]),
        'bathrooms': np.random.normal(2.5, 1, n_samples).clip(1, 5),
        'age': np.random.exponential(20, n_samples).clip(0, 100),
        'lot_size': np.random.lognormal(8, 0.5, n_samples).clip(1000, 50000),
        'garage': np.random.choice([0, 1, 2, 3], n_samples, p=[0.1, 0.3, 0.5, 0.1]),
        'property_type': np.random.choice(['House', 'Condo', 'Townhouse'], n_samples, p=[0.7, 0.2, 0.1])
    }
    
    # Create realistic location multipliers
    location_scores = np.random.choice([0.8, 1.0, 1.2, 1.5, 2.0], n_samples, p=[0.2, 0.3, 0.3, 0.15, 0.05])
    data['location_score'] = location_scores
    
    # Calculate realistic prices
    base_price = (
        data['sqft'] * 150 +
        np.array(data['bedrooms']) * 10000 +
        np.array(data['bathrooms']) * 8000 +
        np.array(data['garage']) * 5000 +
        data['lot_size'] * 2 -
        data['age'] * 1000
    )
    
    # Add location multiplier and noise
    data['price'] = (base_price * location_scores * 
                    np.random.normal(1, 0.1, n_samples)).clip(50000, 2000000)
    
    df = pd.DataFrame(data)
    return df

def train_simple_model():
    """Train a simple real estate model"""
    print("Starting model training...")
    
    # Create data
    df = create_sample_data()
    print(f"Created {len(df)} training samples")
    
    # Prepare features
    le = LabelEncoder()
    df['property_type_encoded'] = le.fit_transform(df['property_type'])
    
    feature_columns = [
        'sqft', 'bedrooms', 'bathrooms', 'age', 'lot_size', 
        'garage', 'property_type_encoded', 'location_score'
    ]
    
    X = df[feature_columns].values
    y = df['price'].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Create model
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='linear')
    ])
    
    # Compile with explicit names to avoid compatibility issues
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )
    
    print("Model created successfully!")
    model.summary()
    
    # Train model
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,  # Reduced for faster training
        batch_size=32,
        verbose=1,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
        ]
    )
    
    # Evaluate
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test MAE: ${test_mae:,.0f}")
    
    # Save everything
    print("Saving model and preprocessors...")
    model.save('real_estate_model.h5')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(le, 'label_encoder.pkl')
    
    print("✅ Training complete!")
    print("Files saved:")
    print("- real_estate_model.h5")
    print("- scaler.pkl") 
    print("- label_encoder.pkl")
    
    return model, scaler, le

def test_prediction():
    """Test a simple prediction"""
    try:
        # Load the model we just trained
        model = tf.keras.models.load_model('real_estate_model.h5')
        scaler = joblib.load('scaler.pkl')
        le = joblib.load('label_encoder.pkl')
        
        # Test prediction
        property_type_encoded = le.transform(['House'])[0]
        features = np.array([[2000, 3, 2, 10, 8000, 2, property_type_encoded, 1.2]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled, verbose=0)
        
        print(f"\n✅ Test prediction successful!")
        print(f"Sample house (2000 sqft, 3 bed, 2 bath): ${prediction[0][0]:,.0f}")
        
    except Exception as e:
        print(f"❌ Test prediction failed: {e}")

if __name__ == "__main__":
    print("=== Real Estate Model Training ===")
    print("This will create and train your AI model...")
    
    # Check if model already exists
    if os.path.exists('real_estate_model.h5'):
        response = input("Model already exists. Retrain? (y/n): ")
        if response.lower() != 'y':
            print("Using existing model.")
            test_prediction()
            exit()
    
    # Train the model
    try:
        model, scaler, le = train_simple_model()
        test_prediction()
        
        print("\n🎉 Success! Your model is ready.")
        print("Now you can run your main application!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        print("Please check the error and try again.")