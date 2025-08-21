import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import DATA_CONFIG, BEHAVIOR_WEIGHTS


class DataProcessor:
    
    def __init__(self):
        self.feature_columns = []
        
    def create_sales_target(self, df): # webpage first prediction
        df = df.copy()
        df['sales_potential'] = (
            df['ProductPrice'] * 
            df['PurchaseIntent'] * 
            (df['CustomerSatisfaction'] / 5.0)
        )
        return df
    
    def encode_categorical_features(self, df):
        df = df.copy()
        
        # encode product categories and brands
        df['category_encoded'] = pd.Categorical(df['ProductCategory']).codes
        df['brand_encoded'] = pd.Categorical(df['ProductBrand']).codes
        
        # age segments
        df['age_segment'] = pd.cut(
            df['CustomerAge'], 
            bins=DATA_CONFIG['age_bins'], 
            labels=DATA_CONFIG['age_labels']
        )
        df['age_segment_encoded'] = pd.Categorical(df['age_segment']).codes
        
        return df
    
    def create_behavioral_features(self, df):
        df = df.copy()

        df['behavior_score'] = (
            df['PurchaseFrequency'] * BEHAVIOR_WEIGHTS['purchase_frequency'] + 
            df['CustomerSatisfaction'] * BEHAVIOR_WEIGHTS['customer_satisfaction'] + 
            df['PurchaseIntent'] * BEHAVIOR_WEIGHTS['purchase_intent']
        )

        df['price_tier'] = pd.cut(
            df['ProductPrice'], 
            bins=DATA_CONFIG['price_bins'], 
            labels=['Budget', 'Low', 'Mid', 'High', 'Premium']
        )

        df['price_tier_encoded'] = pd.Categorical(df['price_tier']).codes

        df['customer_value'] = (
            (df['CustomerAge'] / 100) * 
            df['behavior_score'] * 
            (df['ProductPrice'] / 1000)
        )

        df['price_satisfaction_interaction'] = df['ProductPrice'] * df['CustomerSatisfaction']

        df['age_frequency_interaction'] = df['CustomerAge'] * df['PurchaseFrequency']
        
        return df
    
    def get_feature_columns(self):
        return [
            'ProductPrice', 'CustomerAge', 'CustomerGender', 'PurchaseFrequency', 
            'CustomerSatisfaction', 'category_encoded', 'brand_encoded', 
            'age_segment_encoded', 'behavior_score', 'customer_value',
            'price_satisfaction_interaction', 'age_frequency_interaction', 'price_tier_encoded'
        ]
    
    def process_data(self, df):
        print("\n=== Processing Data ===")
        
        df = self.create_sales_target(df)
        print(f"Sales potential range: ${df['sales_potential'].min():.2f} - ${df['sales_potential'].max():.2f}")
        
        df = self.encode_categorical_features(df)
        
        df = self.create_behavioral_features(df)
        
        self.feature_columns = self.get_feature_columns()
        available_features = [col for col in self.feature_columns if col in df.columns]
        
        print(f"Created {len(available_features)} features for modeling")
        return df, available_features
