# EchoMetrics
EchoMetrics is a machine learning model I developed, complimentary to my quantitative and qualitative data analytics internship at Beats by Dre, where I learned how to analyze data in a business setting and turn raw, unorganized data into insights that helps businesses know their current performance with customers and consumers, and plan how to exapnd and market themselves accordingly.

In this project, I use my knowledge (both from my internship and my personal development experience) to forecast sales of consumer electronics by having a machine learning model analyze historical sales datasets and make predictions based on it.

Unfortunately, considering the fact that the data provided by Beats by Dre cannot be shared here, I had to fix the project to use a different dataset that encompasses a broader demographic of consumer goods: general appliances, such as smartphones, laptops, headphones, etc.

## Tools and Technologies
- **Machine Learning Models:** Python, Matplotlib, Scikit-learn, Pandas, Kaggle (Dataset)
- **Webapp (Frontend/Backend):** Python, Flask, JavaScript, HTML, CSS 
- **Deployment:** Docker, Render.com

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
├── .gitignore
├── sales_predictions.csv
├── config.py                    # plot output configurations
├── requirements.txt             # external dependencies needed to run the models and webpage
├── app.py                       # flask webpage runs from here
└── main.py                      # ml models (in terminal) run from here
```

## Project Installation

### Option 1: Docker (Recommended)
**To run the project using Docker:**
```bash
# Clone the repository
git clone https://github.com/myrmlbst/EchoMetrics
cd EchoMetrics

# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t echometrics .
docker run -p 8080:8080 echometrics
```

### Option 2: Local Installation
**To run the project on your local machine:**
```bash
# Clone the repository
git clone https://github.com/myrmlbst/EchoMetrics
cd EchoMetrics

# Install dependencies
pip install -r requirements.txt

# Run the command-line version
python3 main.py

# Run the web application
python3 app.py
```

**To view the project:**
- **Web Interface:** Navigate to `http://localhost:8080` in your browser
- **Command Line:** Run `python3 main.py` for the prediction pipeline

## Dataset
The dataset I used is available on Kaggle through [this link](https://www.kaggle.com/datasets/rabieelkharoua/consumer-electronics-sales-dataset?resource=download).