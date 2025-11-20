const API_BASE_URL = 'http://localhost:5000';

export interface PropertyData {
  address: string;
  price: number;
  sqft: number;
  bedrooms: number;
  bathrooms: number;
  year_built: number;
  property_type?: string;
}

export interface AnalysisResponse {
  analysis: {
    deal_score: number;
    predicted_value: number;
    pricing_assessment: string;
    explanation: string;
    key_factors: string[];
    price_per_sqft: number;
    predicted_price_per_sqft: number;
    value_drivers: {
      location: number;
      size: number;
      condition: number;
      market_timing: number;
    };
  };
  property: PropertyData;
  comparables: Array<{
    address: string;
    sale_price: number;
    sale_date: string;
    sqft: number;
    bedrooms: number;
    bathrooms: number;
  }>;
}

export interface TrendsResponse {
  location: string;
  average_price: number;
  price_trend: Array<{ month: string; price: number }>;
  days_on_market: number;
  price_per_sqft: number;
  market_status: string;
  total_sales: number;
}

export const analyzeProperty = async (propertyData: PropertyData): Promise<AnalysisResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/analyze-property`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(propertyData),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Network error' }));
    throw new Error(error.error || 'Failed to analyze property');
  }

  return await response.json();
};

export const getNeighborhoodTrends = async (address: string): Promise<TrendsResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/neighborhood-trends`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ address }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Network error' }));
    throw new Error(error.error || 'Failed to fetch neighborhood trends');
  }

  return await response.json();
};

export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US').format(value);
};
