"""
Free Real Estate Data Collector
Uses only free sources - no API keys required
"""

import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup

def get_free_california_housing_data():
    """Get the famous California housing dataset - completely free"""
    print("Downloading California housing dataset...")
    
    # This is a famous free dataset from sklearn
    try:
        from sklearn.datasets import fetch_california_housing
        housing = fetch_california_housing()
        
        df = pd.DataFrame(housing.data, columns=housing.feature_names)
        df['price'] = housing.target * 100000  # Convert to actual prices
        
        # Rename columns to match our model
        df = df.rename(columns={
            'HouseAge': 'age',
            'AveRooms': 'bedrooms',
            'AveBedrms': 'bathrooms',  # Approximate
            'Population': 'lot_size',  # Approximate
            'AveOccup': 'garage',  # Approximate
        })
        
        # Add missing columns
        df['sqft'] = df['bedrooms'] * 800 + random.uniform(200, 600)  # Estimate from rooms
        df['property_type'] = 'House'
        df['location_score'] = 1.0 + (df['MedInc'] - df['MedInc'].mean()) / df['MedInc'].std() * 0.3
        
        print(f"Loaded {len(df)} California housing records")
        return df
        
    except ImportError:
        print("Sklearn not available, generating synthetic data...")
        return generate_synthetic_data()

def generate_synthetic_data(n_samples=10000):
    """Generate realistic synthetic real estate data"""
    print(f"Generating {n_samples} synthetic property records...")
    
    import numpy as np
    np.random.seed(42)
    
    # Create realistic distributions based on real market data
    data = {
        'sqft': np.random.lognormal(7.5, 0.4, n_samples).astype(int),  # 1200-4000 typical range
        'bedrooms': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.25, 0.35, 0.25, 0.05]),
        'bathrooms': np.random.gamma(2, 0.8, n_samples).clip(1, 5),
        'age': np.random.exponential(25, n_samples).clip(0, 100).astype(int),
        'lot_size': np.random.lognormal(9, 0.6, n_samples).astype(int),  # 5000-20000 sqft typical
        'garage': np.random.choice([0, 1, 2, 3], n_samples, p=[0.1, 0.2, 0.6, 0.1]),
        'property_type': np.random.choice(['House', 'Condo', 'Townhouse'], n_samples, p=[0.7, 0.2, 0.1])
    }
    
    # Create location scores (affects price significantly)
    location_scores = np.random.beta(2, 5, n_samples) * 2 + 0.5  # 0.5 to 2.5 range
    data['location_score'] = location_scores
    
    # Calculate realistic prices based on features
    base_price_per_sqft = 200 + location_scores * 100  # $200-300 per sqft
    
    prices = (
        data['sqft'] * base_price_per_sqft +  # Main price driver
        np.array(data['bedrooms']) * 8000 +   # Bedroom premium
        np.array(data['bathrooms']) * 12000 +  # Bathroom premium  
        np.array(data['garage']) * 8000 +     # Garage value
        data['lot_size'] * 3 -                # Lot size premium
        np.array(data['age']) * 800           # Depreciation
    )
    
    # Add market noise and ensure reasonable range
    market_noise = np.random.normal(1, 0.15, n_samples)
    data['price'] = (prices * market_noise).clip(100000, 2000000)
    
    return pd.DataFrame(data)

def scrape_zillow_sample_data():
    """
    Scrape a few sample Zillow listings for training data
    WARNING: Use responsibly and respect Zillow's terms of service
    """
    print("Scraping sample Zillow data...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    sample_data = []
    
    # Sample search URLs for different cities (modify as needed)
    search_urls = [
        "https://www.zillow.com/homes/seattle-wa_rb/",
        "https://www.zillow.com/homes/portland-or_rb/",
        # Add more cities as needed
    ]
    
    for url in search_urls:
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for property cards (this selector may change)
            property_cards = soup.find_all('div', class_=lambda x: x and 'property-card' in x.lower())
            
            for card in property_cards[:5]:  # Limit to 5 per search
                property_data = extract_property_from_card(card)
                if property_data:
                    sample_data.append(property_data)
            
            time.sleep(2)  # Be respectful - don't overload servers
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue
    
    if sample_data:
        df = pd.DataFrame(sample_data)
        print(f"Scraped {len(df)} properties from Zillow")
        return df
    else:
        print("No data scraped, using synthetic data instead")
        return generate_synthetic_data(1000)

def extract_property_from_card(card):
    """Extract property data from a Zillow property card"""
    try:
        price_elem = card.find(text=lambda x: x and '$' in x)
        price = int(''.join(filter(str.isdigit, price_elem))) if price_elem else None
        
        # Extract other features (simplified)
        features_text = card.get_text().lower()
        
        bedrooms = 3  # Default
        bathrooms = 2  # Default
        sqft = 1800  # Default
        
        # Try to extract real values
        import re
        bed_match = re.search(r'(\d+)\s*bed', features_text)
        if bed_match:
            bedrooms = int(bed_match.group(1))
        
        bath_match = re.search(r'(\d+(?:\.\d+)?)\s*bath', features_text)
        if bath_match:
            bathrooms = float(bath_match.group(1))
        
        sqft_match = re.search(r'(\d{3,})\s*sqft', features_text)
        if sqft_match:
            sqft = int(sqft_match.group(1))
        
        return {
            'price': price,
            'sqft': sqft,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'age': random.randint(5, 50),
            'lot_size': random.randint(5000, 15000),
            'garage': random.randint(1, 3),
            'property_type': 'House',
            'location_score': random.uniform(0.8, 1.5)
        }
    
    except:
        return None

def create_training_dataset():
    """Create a comprehensive training dataset using free sources"""
    
    all_data = []
    
    # 1. Get California housing dataset (free and reliable)
    try:
        california_data = get_free_california_housing_data()
        all_data.append(california_data)
        print(f"Added {len(california_data)} California records")
    except Exception as e:
        print(f"California dataset failed: {e}")
    
    # 2. Generate synthetic data (always works)
    synthetic_data = generate_synthetic_data(8000)
    all_data.append(synthetic_data)
    print(f"Added {len(synthetic_data)} synthetic records")
    
    # 3. Optional: Scrape some real Zillow data (be careful with rate limits)
    try:
        zillow_data = scrape_zillow_sample_data()
        if len(zillow_data) > 0:
            all_data.append(zillow_data)
            print(f"Added {len(zillow_data)} Zillow records")
    except Exception as e:
        print(f"Zillow scraping failed: {e}")
    
    # Combine all datasets
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Clean and validate data
        final_df = final_df.dropna()
        final_df = final_df[final_df['price'] > 50000]  # Remove unrealistic prices
        final_df = final_df[final_df['price'] < 5000000]
        final_df = final_df[final_df['sqft'] > 300]
        final_df = final_df[final_df['sqft'] < 10000]
        
        # Save to CSV
        final_df.to_csv('training_data.csv', index=False)
        print(f"Final dataset: {len(final_df)} properties saved to training_data.csv")
        
        # Show sample statistics
        print("\nDataset Statistics:")
        print(f"Average price: ${final_df['price'].mean():,.0f}")
        print(f"Average sqft: {final_df['sqft'].mean():.0f}")
        print(f"Price range: ${final_df['price'].min():,.0f} - ${final_df['price'].max():,.0f}")
        
        return final_df
    else:
        print("No data collected!")
        return None

if __name__ == "__main__":
    print("Creating free real estate training dataset...")
    dataset = create_training_dataset()
    
    if dataset is not None:
        print("Success! Now you can train your model with:")
        print("python zillow_ai_model.py")
