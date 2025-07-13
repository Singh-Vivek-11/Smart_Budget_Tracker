import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

def preprocess_data(df):
    """Clean and preprocess transaction data"""
    required_cols = ['Date', 'Description', 'Amount']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("DataFrame must contain Date, Description, and Amount columns")
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    df['Days_Since_Last'] = df['Date'].diff().dt.days.fillna(0)
    df['Day_of_Week'] = df['Date'].dt.dayofweek
    df['Day_of_Month'] = df['Date'].dt.day
    
    df['Rolling_Amount_Mean'] = df['Amount'].rolling(window=5, min_periods=1).mean()
    df['Rolling_Amount_Std'] = df['Amount'].rolling(window=5, min_periods=1).std()
    
    df.fillna({'Rolling_Amount_Mean': df['Amount'].mean(),
              'Rolling_Amount_Std': df['Amount'].std()}, 
              inplace=True)
    
    return df

def train_fraud_model(df):
    """Train Isolation Forest model for fraud detection"""
    df = preprocess_data(df)
    
    features = ['Amount', 'Days_Since_Last', 'Day_of_Week',
               'Rolling_Amount_Mean', 'Rolling_Amount_Std']
    
    model = IsolationForest(n_estimators=100, 
                          contamination=0.01, 
                          random_state=42)
    model.fit(df[features])
    
    with open('budget_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    return model

def detect_fraud(df):
    """Detect fraudulent transactions"""
    try:
        df = preprocess_data(df)
        
        try:
            with open('budget_model.pkl', 'rb') as f:
                model = pickle.load(f)
        except:
            model = train_fraud_model(df)
        
        features = ['Amount', 'Days_Since_Last', 'Day_of_Week',
                   'Rolling_Amount_Mean', 'Rolling_Amount_Std']
        
        df['Is_Fraud'] = model.predict(df[features])
        df['Is_Fraud'] = df['Is_Fraud'].apply(lambda x: 1 if x == -1 else 0)
        
        return df
    
    except Exception as e:
        raise ValueError(f"Error in fraud detection: {str(e)}")

def categorize_transactions(df):
    """Categorize transactions based on description"""
    categories = {
        'food': ['grocery', 'market', 'restaurant', 'starbucks', 'whole foods', 'coffee'],
        'health': ['pharmacy', 'dentist', 'doctor', 'cvs', 'clinic', 'hospital'],
        'utilities': ['at&t', 'verizon', 'bill', 'electric', 'water', 'internet'],
        'transport': ['gas', 'petrol', 'uber', 'lyft', 'shell', 'taxi'],
        'shopping': ['amazon', 'best buy', 'target', 'walmart', 'store'],
        'housing': ['rent', 'apartment', 'mortgage', 'lease'],
        'entertainment': ['netflix', 'spotify', 'hulu', 'movie', 'concert']
    }
    
    df['Category'] = 'other'
    for category, keywords in categories.items():
        for keyword in keywords:
            mask = df['Description'].str.contains(keyword, case=False, na=False)
            df.loc[mask, 'Category'] = category
            
    return df

def analyze_budget(df, budget_limits):
    """Analyze spending against budget limits"""
    safe_budget = budget_limits.copy()
    safe_budget.setdefault('other', 0)
    
    spending = df.groupby('Category')['Amount'].sum().to_dict()
    
    alerts = []
    for category, amount in spending.items():
        limit = safe_budget.get(category, safe_budget.get('other', 0))
        if amount > limit:
            alerts.append(f"Budget exceeded for {category}: ${amount:.2f} (Limit: ${limit:.2f})")
    
    return spending, alerts