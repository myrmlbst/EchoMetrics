# EchoMetrics
EchoMetrics is a machine learning model I developed, complimentary to my quantitative and qualitative data analytics externship at Beats by Dre, where I learned how to analyze data in a business setting and turn raw, unorganized data into insights that helps businesses know their current performance with customers and consumers, and plan how to exapnd and market themselves accordingly.

In this project, I use my knowledge (both from my internship and my personal development experience) to forecast sales of consumer electronics by having a machine learning model analyze historical sales datasets and make predictions based on it.

Unfortunately, considering the fact that the data provided by Beats by Dre cannot be shared here, I had to fix the project to use a different dataset that encompasses a broader demographic of consumer goods: general appliances, such as smartphones, laptops, headphones, etc.

## Tools and Technologies
- **Machine Learning Models:** Python, Matplotlib, Scikit-learn, Pandas, Kaggle (Dataset)
- **Webapp (Frontend/Backend):** Python, Flask, JavaScript, HTML, CSS 
- **Deployment:** Docker, Render.com
<div align="center">
  <img
      src="https://skillicons.dev/icons?i=python,flask,javascript,html,css,docker,scikitlearn"
      class="h-14"
  />
</div>

## Directory Structure
```
EchoMetrics
├── data/
│   ├── loader.py                # kaggle data loading
│   └── processor.py             # feature engineering
├── models/
│   ├── predictor.py             # model training
│   └── scenario_generator.py    # sales scenarios
├── utils/
│   └── logger.py                # logging system
├── visualization/
│   └── plotter.py               # charts n graphs
├── web
│   ├── static                   # stylization tools and configs
│   └── templates                # main html page
│   └── processor.py             # feature engineering
│ 
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
│
├── LICENSE                      # feel free to contribute!
│ 
├── .gitignore
├── sales_predictions.csv
├── config.py                    # plot output configurations
├── requirements.txt             # external dependencies needed to run the models and webpage
├── app.py                       # flask webpage runs from here
├── main.py                      # ml models (in terminal) run from here
└── run.sh                       # convenience script to run the application
```

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Running the Application
1. Make the run script executable (only needed once):
   ```bash
   chmod +x run.sh
   ```

2. Run the application:
   ```bash
   ./run.sh
   ```

   This will:
   - Create a Python virtual environment (if it doesn't exist)
   - Install all required dependencies
   - Create necessary directories
   - Start the EchoMetrics application

3. Access the web interface at [http://localhost:8080](http://localhost:8080) once the application starts.

### Running with Docker (Alternative)
If you prefer using Docker, you can build and run the application using:
```bash
docker-compose up --build
```

## Dataset
The dataset I used is available on Kaggle through [this link](https://www.kaggle.com/datasets/rabieelkharoua/consumer-electronics-sales-dataset?resource=download).
