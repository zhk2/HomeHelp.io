from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import joblib
import tensorflow as tf

# Import our custom model functions
import sys
sys.path.append('.')
from homeanalyzer.zillow_ai_model import predict_house_price, load_trained_model

app = Flask(__name__)
CORS(app)

# ================================
# ZILLOW SCRAPER (Free - no API needed)
# ================================

class ZillowScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_property_details(self, zillow_url):
        """Extract property details from Zillow URL - completely free"""
        try:
            response = requests.get(zillow_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            property_data = {
                'price': self.extract_price(soup),
                'sqft': self.extract_sqft(soup),
                'bedrooms': self.extract_bedrooms(soup),
                'bathrooms': self.extract_bathrooms(soup),
                'address': self.extract_address(soup),
                'lot_size': self.extract_lot_size(soup),
                'year_built': self.extract_year_built(soup),
                'property_type': self.extract_property_type(soup)
            }
            
            return property_data
        except Exception as e:
            print(f"Error scraping Zillow: {e}")
            return None
    
    def extract_price(self, soup):
        # Try multiple selectors for price
        price_selectors = [
            'span[data-testid="price"]',
            '.notranslate',
            'span.Text-c11n-8-84-3__sc-aiai24-0'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem and '$' in price_elem.text:
                price_text = price_elem.text.replace('$', '').replace(',', '').replace('+', '')
                try:
                    return int(''.join(filter(str.isdigit, price_text)))
                except:
                    continue
        return 400000  # Default fallback
    
    def extract_sqft(self, soup):
        sqft_elem = soup.find(text=lambda x: x and 'sqft' in x.lower())
        if sqft_elem:
            numbers = ''.join(filter(str.isdigit, sqft_elem))
            return int(numbers) if numbers else 1800
        return 1800  # Default
    
    def extract_bedrooms(self, soup):
        bed_elem = soup.find(text=lambda x: x and 'bed' in x.lower())
        if bed_elem:
            numbers = ''.join(filter(str.isdigit, bed_elem))
            return int(numbers[0]) if numbers else 3
        return 3  # Default
    
    def extract_bathrooms(self, soup):
        bath_elem = soup.find(text=lambda x: x and 'bath' in x.lower())
        if bath_elem:
            numbers = ''.join(filter(str.isdigit, bath_elem.replace('.', '')))
            return float(numbers[0] + '.' + numbers[1]) if len(numbers) >= 2 else 2
        return 2  # Default
    
    def extract_address(self, soup):
        addr_elem = soup.find('h1')
        return addr_elem.text if addr_elem else "Unknown Address"
    
    def extract_lot_size(self, soup):
        lot_elem = soup.find(text=lambda x: x and 'acre' in x.lower())
        if lot_elem:
            try:
                acres = float(''.join(filter(lambda x: x.isdigit() or x == '.', lot_elem)))
                return int(acres * 43560)  # Convert acres to sqft
            except:
                pass
        return 8000  # Default lot size in sqft
    
    def extract_year_built(self, soup):
        year_elem = soup.find(text=lambda x: x and 'built' in x.lower())
        if year_elem:
            years = ''.join(filter(str.isdigit, year_elem))
            if len(years) >= 4:
                return int(years[-4:])
        return 1990  # Default
    
    def extract_property_type(self, soup):
        type_keywords = ['house', 'condo', 'townhouse', 'single family']
        page_text = soup.get_text().lower()
        
        for keyword in type_keywords:
            if keyword in page_text:
                return keyword.title()
        return 'House'  # Default

# ================================
# AI ANALYZER (Uses our custom model)
# ================================

class CustomAIAnalyzer:
    def __init__(self):
        try:
            self.model, self.scaler, self.le = load_trained_model()
            self.model_loaded = True
        except:
            print("Model not found. Please train the model first.")
            self.model_loaded = False
    
    def analyze_property(self, property_data):
        """Analyze property using our custom ML model"""
        
        if not self.model_loaded:
            return self.fallback_analysis(property_data)
        
        try:
            # Extract features
            sqft = float(property_data.get('sqft', 1800))
            bedrooms = float(property_data.get('bedrooms', 3))
            bathrooms = float(property_data.get('bathrooms', 2))
            
            # Calculate age
            current_year = 2024
            year_built = int(property_data.get('year_built', 1990))
            age = current_year - year_built
            
            lot_size = float(property_data.get('lot_size', 8000))
            garage = 2  # Default - could be extracted from description
            property_type = property_data.get('property_type', 'House')
            location_score = self.estimate_location_score(property_data.get('address', ''))
            
            # Get AI prediction
            predicted_value = predict_house_price(
                sqft=sqft,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                age=age,
                lot_size=lot_size,
                garage=garage,
                property_type=property_type,
                location_score=location_score
            )
            
            # Compare with listing price
            listing_price = float(property_data.get('price', 400000))
            price_diff_pct = ((predicted_value - listing_price) / listing_price) * 100
            
            # Calculate deal score
            if price_diff_pct > 15:
                deal_score = 9.5
                pricing_assessment = "significantly_underpriced"
            elif price_diff_pct > 5:
                deal_score = 8.0
                pricing_assessment = "underpriced"
            elif price_diff_pct > -5:
                deal_score = 6.5
                pricing_assessment = "fairly_priced"
            elif price_diff_pct > -15:
                deal_score = 4.0
                pricing_assessment = "overpriced"
            else:
                deal_score = 2.0
                pricing_assessment = "significantly_overpriced"
            
            # Generate explanation
            explanation = self.generate_explanation(property_data, predicted_value, listing_price, price_diff_pct)
            
            return {
                "predicted_value": int(predicted_value),
                "deal_score": deal_score,
                "value_drivers": {
                    "location": 40,
                    "size": 30,
                    "condition": 20,
                    "market_timing": 10
                },
                "explanation": explanation,
                "pricing_assessment": pricing_assessment,
                "key_factors": self.identify_key_factors(property_data, price_diff_pct),
                "price_per_sqft": int(listing_price / sqft) if sqft > 0 else 0,
                "predicted_price_per_sqft": int(predicted_value / sqft) if sqft > 0 else 0
            }
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self.fallback_analysis(property_data)
    
    def estimate_location_score(self, address):
        """Estimate location quality - could be enhanced with real data"""
        # Simple heuristic based on common location indicators
        address_lower = address.lower()
        
        if any(word in address_lower for word in ['downtown', 'center', 'main st']):
            return 1.5
        elif any(word in address_lower for word in ['lake', 'park', 'hill', 'view']):
            return 1.3
        elif any(word in address_lower for word in ['suburb', 'residential']):
            return 1.1
        else:
            return 1.0
    
    def generate_explanation(self, property_data, predicted_value, listing_price, price_diff_pct):
        """Generate human-readable explanation"""
        
        if price_diff_pct > 10:
            return f"This property appears to be a great deal! Our AI predicts it's worth ${predicted_value:,.0f}, which is {price_diff_pct:.1f}% above the listing price. The size and location factors suggest strong value potential."
        elif price_diff_pct > 0:
            return f"This property seems fairly priced with slight upside. Our AI estimates a value of ${predicted_value:,.0f}, indicating {price_diff_pct:.1f}% potential appreciation from current pricing."
        elif price_diff_pct > -10:
            return f"This property is priced close to market value. Our AI predicts a fair value of ${predicted_value:,.0f}, suggesting the current price is reasonable for the area and features."
        else:
            return f"This property appears overpriced. Our AI estimates a fair value of ${predicted_value:,.0f}, which is {abs(price_diff_pct):.1f}% below the current listing price. Consider negotiating or looking for better deals."
    
    def identify_key_factors(self, property_data, price_diff_pct):
        """Identify key value factors"""
        factors = []
        
        sqft = int(property_data.get('sqft', 1800))
        if sqft > 2500:
            factors.append("Large living space")
        elif sqft < 1200:
            factors.append("Compact size may limit value")
        
        bedrooms = int(property_data.get('bedrooms', 3))
        if bedrooms >= 4:
            factors.append("Family-friendly bedroom count")
        
        year_built = int(property_data.get('year_built', 1990))
        if year_built > 2010:
            factors.append("Modern construction")
        elif year_built < 1980:
            factors.append("Older home may need updates")
        
        if price_diff_pct > 10:
            factors.append("Potentially undervalued opportunity")
        
        return factors[:3]  # Limit to top 3 factors
    
    def fallback_analysis(self, property_data):
        """Simple analysis when AI model isn't available"""
        price = int(property_data.get('price', 0))
        sqft = int(property_data.get('sqft', 1))
        
        price_per_sqft = price / sqft if sqft > 0 else 0
        
        return {
            "predicted_value": price * 0.98,
            "deal_score": 5.0,
            "value_drivers": {
                "location": 40,
                "size": 30,
                "condition": 20,
                "market_timing": 10
            },
            "explanation": "Basic analysis - custom AI model not loaded",
            "pricing_assessment": "unknown",
            "key_factors": ["Analysis limited without AI model"],
            "price_per_sqft": price_per_sqft,
            "predicted_price_per_sqft": price_per_sqft
        }

# ================================
# FLASK API ROUTES
# ================================

scraper = ZillowScraper()
analyzer = CustomAIAnalyzer()

@app.route('/api/analyze-property', methods=['POST'])
def analyze_property():
    """Analyze property using custom AI model"""
    data = request.get_json()
    
    if 'zillow_url' in data:
        property_data = scraper.get_property_details(data['zillow_url'])
    elif 'address' in data:
        property_data = {
            'address': data['address'],
            'price': data.get('price', 0),
            'sqft': data.get('sqft', 0),
            'bedrooms': data.get('bedrooms', 0),
            'bathrooms': data.get('bathrooms', 0),
            'year_built': data.get('year_built', 1990),
            'property_type': data.get('property_type', 'House')
        }
    else:
        return jsonify({'error': 'Please provide zillow_url or property details'}), 400
    
    if not property_data:
        return jsonify({'error': 'Could not fetch property data'}), 404
    
    # Analyze with custom AI
    analysis = analyzer.analyze_property(property_data)
    
    # Mock comparable sales
    comparables = [
        {
            "address": "Similar property nearby",
            "sale_price": int(property_data.get('price', 400000) * 0.95),
            "sale_date": "2024-01-15",
            "sqft": property_data.get('sqft', 1800),
            "bedrooms": property_data.get('bedrooms', 3),
            "bathrooms": property_data.get('bathrooms', 2)
        }
    ]
    
    result = {
        'property': property_data,
        'analysis': analysis,
        'comparables': comparables
    }
    
    return jsonify(result)

@app.route('/api/neighborhood-trends', methods=['POST'])
def neighborhood_trends():
    """Get neighborhood trends"""
    data = request.get_json()
    
    # Mock trend data - in real app, this could use additional data sources
    trends = {
        'average_price': 475000,
        'price_trend_6mo': 8.5,
        'days_on_market': 25,
        'price_per_sqft': 285,
        'market_status': 'seller_market',
        'monthly_data': [
            {'month': '2024-01', 'avg_price': 450000, 'sales_count': 15},
            {'month': '2024-02', 'avg_price': 455000, 'sales_count': 18},
            {'month': '2024-03', 'avg_price': 465000, 'sales_count': 22},
            {'month': '2024-04', 'avg_price': 475000, 'sales_count': 19},
        ]
    }
    
    return jsonify(trends)

@app.route('/api/train-model', methods=['POST'])
def train_model():
    """Endpoint to train/retrain the model"""
    try:
        from homeanalyzer.zillow_ai_model import train_model
        model, scaler, le, history = train_model()
        return jsonify({'success': True, 'message': 'Model trained successfully'})
    except Exception as e:
        return jsonify({'error': f'Training failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting HomeAnalyzer API with custom AI model...")
    print("Make sure to train the model first by running: python zillow_ai_model.py")
    app.run(debug=True, port=5000)
