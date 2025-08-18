import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import VIZ_CONFIG


class SalesVisualizer:
    def __init__(self):
        plt.style.use('default')
        sns.set_palette(VIZ_CONFIG['color_palette'])
    
    def plot_sales_analysis(self, df, scenario_predictions, model_results=None):
        print("\n=== Creating Visualizations ===")
        
        fig, axes = plt.subplots(2, 3, figsize=VIZ_CONFIG['figure_size'])
        fig.suptitle('EchoMetrics Sales Prediction Analysis', fontsize=16, fontweight='bold')
        
        self._plot_category_boxplot(df, axes[0, 0])
        self._plot_price_vs_sales(df, axes[0, 1])

        if model_results:
            self._plot_model_performance(model_results, axes[0, 2])
        
        self._plot_customer_behavior(df, axes[1, 0])
        self._plot_top_predictions(scenario_predictions, axes[1, 1])
        self._plot_sales_distribution(df, axes[1, 2])
        
        plt.tight_layout()
        plt.show()
    
    def _plot_category_boxplot(self, df, ax):
        df.boxplot(column='sales_potential', by='ProductCategory', ax=ax)
        ax.set_title('Sales Potential by Category')
        ax.set_xlabel('Product Category')
        ax.set_ylabel('Sales Potential ($)')
        ax.tick_params(axis='x', rotation=45)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    def _plot_price_vs_sales(self, df, ax):
        scatter = ax.scatter(
            df['ProductPrice'], 
            df['sales_potential'], 
            alpha=VIZ_CONFIG['alpha'], 
            c=df['CustomerSatisfaction'], 
            cmap=VIZ_CONFIG['color_palette']
        )
        ax.set_xlabel('Product Price ($)')
        ax.set_ylabel('Sales Potential ($)')
        ax.set_title('Price vs Sales Potential')
        plt.colorbar(scatter, ax=ax, label='Customer Satisfaction')
        ax.grid(True, alpha=VIZ_CONFIG['grid_alpha'])
    
    def _plot_model_performance(self, model_results, ax):
        best_result = max(model_results.values(), key=lambda x: x['R2'])
        y_test = best_result['y_test']
        y_pred = best_result['predictions']
        
        ax.scatter(y_test, y_pred, alpha=VIZ_CONFIG['alpha'])
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        ax.set_xlabel('Actual Sales Potential ($)')
        ax.set_ylabel('Predicted Sales Potential ($)')
        ax.set_title(f'Model Performance (R² = {best_result["R2"]:.3f})')
        ax.grid(True, alpha=VIZ_CONFIG['grid_alpha'])
    
    def _plot_customer_behavior(self, df, ax):
        scatter = ax.scatter(
            df['CustomerAge'], 
            df['behavior_score'], 
            alpha=VIZ_CONFIG['alpha'], 
            c=df['PurchaseIntent'], 
            cmap='coolwarm'
        )
        ax.set_xlabel('Customer Age')
        ax.set_ylabel('Behavior Score')
        ax.set_title('Age vs Purchase Behavior')
        plt.colorbar(scatter, ax=ax, label='Purchase Intent')
        ax.grid(True, alpha=VIZ_CONFIG['grid_alpha'])
    
    def _plot_top_predictions(self, scenario_predictions, ax):
        top_scenarios = scenario_predictions.head(8)
        y_pos = range(len(top_scenarios))
        
        bars = ax.barh(y_pos, top_scenarios['predicted_sales'], color='skyblue', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([
            f"{row['ProductCategory'][:10]}\n{row['ProductBrand'][:8]}" 
            for _, row in top_scenarios.iterrows()
        ], fontsize=8)
        ax.set_xlabel('Predicted Sales Potential ($)')
        ax.set_title('Top Sales Predictions')
        ax.grid(True, alpha=VIZ_CONFIG['grid_alpha'], axis='x')
        
        # value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                   f'${width:.0f}', ha='left', va='center', fontsize=8)
    
    def _plot_sales_distribution(self, df, ax):
        ax.hist(df['sales_potential'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title('Sales Potential Distribution')
        ax.set_xlabel('Sales Potential ($)')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=VIZ_CONFIG['grid_alpha'])
    
    def print_summary(self, df, scenario_predictions):
        print(f"\n=== Prediction Summary ===")
        print(f"Sales potential range: ${df['sales_potential'].min():.2f} - ${df['sales_potential'].max():.2f}")
        print(f"Average sales potential: ${df['sales_potential'].mean():.2f}")
        print(f"Top predicted scenario: ${scenario_predictions.iloc[0]['predicted_sales']:.2f}")
        print(f"Best category: {scenario_predictions.iloc[0]['ProductCategory']}")
        print(f"Best brand: {scenario_predictions.iloc[0]['ProductBrand']}")
    
    def plot_feature_importance(self, feature_importance_df):
        if feature_importance_df is None:
            return
            
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(feature_importance_df)), feature_importance_df['importance'])
        plt.yticks(range(len(feature_importance_df)), feature_importance_df['feature'])
        plt.xlabel('Importance')
        plt.title('Feature Importance Analysis')
        plt.grid(True, alpha=VIZ_CONFIG['grid_alpha'], axis='x')
        plt.tight_layout()
        plt.show()
