import os
import pandas as pd
import kagglehub
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import DATASET_CONFIG


class DataLoader:
    
    def __init__(self):
        self.dataset_path = None
        
    def download_dataset(self):
        try:
            self.dataset_path = kagglehub.dataset_download(DATASET_CONFIG['kaggle_dataset'])
            print(f"Dataset downloaded to: {self.dataset_path}")
            return self.dataset_path
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            return None
    
    def find_csv_files(self):
        if not self.dataset_path:
            return []
            
        csv_files = []
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
        return csv_files
    
    def load_data(self):
        if not self.dataset_path:
            self.download_dataset()
            
        csv_files = self.find_csv_files()
        
        if not csv_files:
            print("No CSV files found in dataset")
            return None
            
        try:
            df = pd.read_csv(csv_files[0])
            print(f"Loaded dataset with shape: {df.shape}")
            return df
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None
    
    def explore_data(self, df):
        if df is None:
            return
            
        print(f"\n=== Dataset Overview ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        print(f"\nDataset info:")
        print(df.info())
        print(f"\nBasic statistics:")
        print(df.describe())
