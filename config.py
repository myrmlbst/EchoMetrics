MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'random_state': 42,
        'max_depth': None,
        'min_samples_split': 2
    },
    'linear_regression': {
        'fit_intercept': True
    }
}

DATA_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'age_bins': [0, 25, 35, 50, 100],
    'age_labels': ['Young', 'Adult', 'Middle', 'Senior'],
    'price_bins': 5
}

BEHAVIOR_WEIGHTS = {
    'purchase_frequency': 0.4,
    'customer_satisfaction': 0.3,
    'purchase_intent': 0.3
}

VIZ_CONFIG = {
    'figure_size': (15, 12),
    'color_palette': 'viridis',
    'alpha': 0.6,
    'grid_alpha': 0.3
}

DATASET_CONFIG = {
    'kaggle_dataset': "rabieelkharoua/consumer-electronics-sales-dataset",
    'target_variable': 'sales_potential',
    'prediction_scenarios': 10
}
