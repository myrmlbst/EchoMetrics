import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import MODEL_CONFIG, DATA_CONFIG


class SalesPredictor:
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = []
        self.results = {}
    
    def initialize_models(self):
        self.models = {
            'Random Forest': RandomForestRegressor(**MODEL_CONFIG['random_forest']),
            'Linear Regression': LinearRegression(**MODEL_CONFIG['linear_regression'])
        }
    
    def train_models(self, df, feature_columns):
        print("\n=== Training Models ===")
        
        self.feature_columns = feature_columns
        
        # prepare features and target
        X = df[feature_columns]
        y = df['sales_potential']
        
        print(f"Training data shape: {X.shape}")
        print(f"Using features: {feature_columns}")
        
        # split data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=DATA_CONFIG['test_size'], 
            random_state=DATA_CONFIG['random_state']
        )
        
        self.initialize_models()
        
        # train and evaluate each model
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            # train model
            model.fit(X_train, y_train)
            
            # make predictions
            y_pred = model.predict(X_test)
            
            # calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.results[name] = {
                'model': model,
                'MAE': mae,
                'MSE': mse,
                'R2': r2,
                'predictions': y_pred,
                'y_test': y_test
            }
            
            print(f"{name} Results:")
            print(f"  MAE: {mae:.2f}")
            print(f"  MSE: {mse:.2f}")
            print(f"  R²: {r2:.3f}")
        
        # select best model
        self.best_model_name = max(self.results.keys(), key=lambda x: self.results[x]['R2'])
        self.best_model = self.results[self.best_model_name]['model']
        
        print(f"\nBest model: {self.best_model_name} (R² = {self.results[self.best_model_name]['R2']:.3f})")
        return self.best_model
    
    def get_feature_importance(self):
        if self.best_model is None or not hasattr(self.best_model, 'feature_importances_'):
            return None
            
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def predict(self, X):
        if self.best_model is None:
            raise ValueError("No trained model available. Train models first.")
        return self.best_model.predict(X)
    
    def get_model_performance(self):
        return self.results
