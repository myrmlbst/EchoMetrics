import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import DATASET_CONFIG


class ScenarioGenerator:
    
    def __init__(self):
        self.scenarios = []
    
    def create_scenarios(self, df):
        scenarios = []
        
        # get unique categories and top brands
        categories = df['ProductCategory'].unique()
        brands = df['ProductBrand'].unique()[:5]  # top 5 brands
        
        for category in categories:
            category_data = df[df['ProductCategory'] == category]
            median_price = category_data['ProductPrice'].median()
            
            for brand in brands[:3]:  # top 3 brands per category
                scenario = {
                    'ProductCategory': category,
                    'ProductBrand': brand,
                    'ProductPrice': median_price,
                    'CustomerAge': 35,  # avg adult customer
                    'CustomerGender': 1,
                    'PurchaseFrequency': 3,  # moderate frequency
                    'CustomerSatisfaction': 4,  # high satisfaction
                    'PurchaseIntent': 1  # intent to purchase
                }
                scenarios.append(scenario)
        
        return pd.DataFrame(scenarios)
    
    def apply_feature_engineering(self, scenario_df, reference_df):
        from data.processor import DataProcessor
        
        processor = DataProcessor()
        
        # apply transformations
        scenario_df = processor.create_sales_target(scenario_df)
        
        # encode categories using reference data categories
        scenario_df['category_encoded'] = pd.Categorical(
            scenario_df['ProductCategory'], 
            categories=reference_df['ProductCategory'].unique()
        ).codes
        
        scenario_df['brand_encoded'] = pd.Categorical(
            scenario_df['ProductBrand'], 
            categories=reference_df['ProductBrand'].unique()
        ).codes
        
        # apply other feature engineering
        scenario_df = processor.encode_categorical_features(scenario_df)
        scenario_df = processor.create_behavioral_features(scenario_df)
        
        return scenario_df
    
    def generate_predictions(self, model, df, feature_columns):
        print(f"\n=== Generating Sales Scenarios ===")
        
        # create scenarios
        scenario_df = self.create_scenarios(df)
        
        # apply feature engineering
        scenario_df = self.apply_feature_engineering(scenario_df, df)
        
        # predictions
        X_scenarios = scenario_df[feature_columns]
        predictions = model.predict(X_scenarios)
        scenario_df['predicted_sales'] = predictions
        
        scenario_df = scenario_df.sort_values('predicted_sales', ascending=False)
        
        # return top scenarios
        top_scenarios = scenario_df[
            ['ProductCategory', 'ProductBrand', 'ProductPrice', 'predicted_sales']
        ].head(DATASET_CONFIG['prediction_scenarios'])
        
        return top_scenarios
