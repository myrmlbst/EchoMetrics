#!/usr/bin/env python3
import sys
import os
import warnings

from data.loader import DataLoader
from data.processor import DataProcessor
from models.predictor import SalesPredictor
from models.scenario_generator import ScenarioGenerator
from visualization.plotter import SalesVisualizer
from utils.logger import EchoLogger
import joblib
from pathlib import Path

warnings.filterwarnings('ignore')


class EchoMetrics:
    
    def __init__(self):
        self.logger = EchoLogger()
        self.data_loader = DataLoader()
        self.data_processor = DataProcessor()
        self.predictor = SalesPredictor()
        self.scenario_generator = ScenarioGenerator()
        self.visualizer = SalesVisualizer()
        
        self.raw_data = None
        self.processed_data = None
        self.feature_columns = []
    
    def run_prediction_pipeline(self):
        try:
            self.logger.info("Starting EchoMetrics Sales Prediction System")
            
            self._load_data()
            self._process_data()
            self._train_models()
            self._generate_predictions()
            self._create_visualizations()
            self._save_results()
            
            self.logger.info("Sales prediction pipeline completed successfully")
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def _load_data(self):
        print("=== EchoMetrics: Sales Prediction System ===\n")
        
        self.raw_data = self.data_loader.load_data()
        if self.raw_data is None:
            raise ValueError("Failed to load dataset")
        
        self.data_loader.explore_data(self.raw_data)
    
    def _process_data(self):
        self.processed_data, self.feature_columns = self.data_processor.process_data(self.raw_data)
        if self.processed_data is None or self.processed_data.empty:
            raise ValueError("Data processing failed")
    
    def _train_models(self):
        model = self.predictor.train_models(self.processed_data, self.feature_columns)
        if model is None:
            raise ValueError("Model training failed")
    
    def _generate_predictions(self):
        self.scenario_predictions = self.scenario_generator.generate_predictions(
            self.predictor.best_model, 
            self.processed_data, 
            self.feature_columns
        )
    
    def _create_visualizations(self):
        model_results = self.predictor.get_model_performance()
        
        # main analysis plots
        self.visualizer.plot_sales_analysis(
            self.processed_data, 
            self.scenario_predictions, 
            model_results
        )
        
        # feature importance plot
        feature_importance = self.predictor.get_feature_importance()
        if feature_importance is not None:
            self.visualizer.plot_feature_importance(feature_importance)
            print("\n=== Feature Importance ===")
            print(feature_importance)
        
        # summary
        self.visualizer.print_summary(self.processed_data, self.scenario_predictions)
    
    def _save_results(self):        
        self.scenario_predictions.to_csv('sales_predictions.csv', index=False)
        print(f"\nSales predictions saved to 'sales_predictions.csv'")
        
        # display top predictions
        print(f"\n=== Top 10 Sales Predictions ===")
        print(self.scenario_predictions)

        # persist best model and feature columns for reuse by the web app
        artifacts_dir = Path('artifacts')
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = artifacts_dir / 'model_bundle.joblib'
        bundle = {
            'model': self.predictor.best_model,
            'feature_columns': self.feature_columns,
            'best_model_name': self.predictor.best_model_name,
            'metrics': {k: {m: v for m, v in self.predictor.results[k].items() if m in ['MAE', 'MSE', 'R2']} for k in self.predictor.results}
        }
        joblib.dump(bundle, bundle_path)
        print(f"Model bundle saved to '{bundle_path}'")


def main():
    app = EchoMetrics()
    app.run_prediction_pipeline()


if __name__ == "__main__":
    main()