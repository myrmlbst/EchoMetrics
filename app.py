#!/usr/bin/env python3

import sys
import os
import json
import pickle
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

from data.loader import DataLoader
from data.processor import DataProcessor
from models.predictor import SalesPredictor
from models.scenario_generator import ScenarioGenerator

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

# global vars to store trained model and data
trained_model = None
data_processor = None
processed_data = None
feature_columns = []

def initialize_system():
    global trained_model, data_processor, processed_data, feature_columns
    
    print("Initializing EchoMetrics system...")
    
    data_loader = DataLoader()
    raw_data = data_loader.load_data()
    
    if raw_data is None:
        raise ValueError("Failed to load dataset")
    
    # process data
    data_processor = DataProcessor()
    processed_data, feature_columns = data_processor.process_data(raw_data)
    # train model
    predictor = SalesPredictor()
    trained_model = predictor.train_models(processed_data, feature_columns)
    
    print("System initialized successfully!")
    return predictor

@app.route('/')
def index(): # main dashboard page
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_sales(): # api endpoint for sales prediction
    try:
        data = request.json
        
        # create input dataframe
        input_data = pd.DataFrame([{
            'ProductPrice': float(data['price']),
            'CustomerAge': int(data['age']),
            'CustomerGender': int(data['gender']),
            'PurchaseFrequency': int(data['frequency']),
            'CustomerSatisfaction': int(data['satisfaction']),
            'PurchaseIntent': int(data['intent'])
        }])
        
        # feature engineering
        input_data = data_processor.create_sales_target(input_data)
        
        # for categorical features, use mode values from training data
        input_data['category_encoded'] = 0  # default category
        input_data['brand_encoded'] = 0     # default brand
        
        input_data = data_processor.encode_categorical_features(input_data)
        input_data = data_processor.create_behavioral_features(input_data)
        
        # make prediction
        X_input = input_data[feature_columns]
        prediction = trained_model.predict(X_input)[0]
        
        return jsonify({
            'prediction': round(prediction, 2),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/api/scenarios')
def get_scenarios(): # get top sales scenarios
    try:
        scenario_generator = ScenarioGenerator()
        scenarios = scenario_generator.generate_predictions(
            trained_model, processed_data, feature_columns
        )
        
        return jsonify({
            'scenarios': scenarios.to_dict('records'),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/api/analytics')
def get_analytics(): # get analytics for the dashboard
    try:
        analytics = {
            'total_records': len(processed_data),
            'avg_sales_potential': round(processed_data['sales_potential'].mean(), 2),
            'max_sales_potential': round(processed_data['sales_potential'].max(), 2),
            'categories': processed_data['ProductCategory'].value_counts().to_dict(),
            'price_range': {
                'min': round(processed_data['ProductPrice'].min(), 2),
                'max': round(processed_data['ProductPrice'].max(), 2),
                'avg': round(processed_data['ProductPrice'].mean(), 2)
            }
        }
        
        return jsonify({
            'analytics': analytics,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/api/chart/<chart_type>')
def generate_chart(chart_type): # base64 imgs
    try:
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'price_vs_sales':
            plt.scatter(processed_data['ProductPrice'], processed_data['sales_potential'], 
                       alpha=0.6, c=processed_data['CustomerSatisfaction'], cmap='viridis')
            plt.xlabel('Product Price ($)')
            plt.ylabel('Sales Potential ($)')
            plt.title('Price vs Sales Potential')
            plt.colorbar(label='Customer Satisfaction')
            
        elif chart_type == 'category_distribution':
            category_sales = processed_data.groupby('ProductCategory')['sales_potential'].mean()
            plt.bar(category_sales.index, category_sales.values)
            plt.xlabel('Product Category')
            plt.ylabel('Average Sales Potential ($)')
            plt.title('Sales Potential by Category')
            plt.xticks(rotation=45)
            
        elif chart_type == 'age_behavior':
            plt.scatter(processed_data['CustomerAge'], processed_data['behavior_score'], 
                       alpha=0.6, c=processed_data['PurchaseIntent'], cmap='coolwarm')
            plt.xlabel('Customer Age')
            plt.ylabel('Behavior Score')
            plt.title('Age vs Purchase Behavior')
            plt.colorbar(label='Purchase Intent')
        
        plt.tight_layout()
        
        # convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'chart': f"data:image/png;base64,{img_base64}",
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    # init system
    predictor = initialize_system()
    
    print("Starting Flask web application...")
    app.run(debug=True, host='0.0.0.0', port=8080)
