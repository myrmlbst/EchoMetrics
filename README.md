# EchoMetrics

EchoMetrics is a machine learning model I developed, complimentary to my quantitative and qualitative data analytics internship at Beats by Dre, where I learned

In this project, I use my knowledge (both from my internship and my personal development experience) to forecast sales of consumer electronics by having a machine learning model analyze historical sales datasets and make predictions based on it.

Unfortunately, considering the fact that the data provided by Beats by Dre cannot be shared here, I had to fix the project to use a different dataset that encompasses a broader demogrpahic of consumer goods: general appliances, such as smartphones, laptops, headphones, etc.

- Create time-based features (day, month, lag values)
- Apply regression models to forecast next period s sales
- Plot actual vs. predicted values over time

## Tools and Technologies
- **Backend and Machine Learning:** Python, Matplotlib, Scikit-learn, Pandas, Kaggle (Dataset)
- **Frontend:** Python, Flask, JavaScript, HTML
- **Deploymeny:** Docker, Render.com

## Directory Structure
```
src/
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
└── main.py                      # project runs from here
```

## Project Installation

### Option 1: Docker (Recommended)
**To run the project using Docker:**
```bash
# Clone the repository
git clone <repository-url>
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
git clone <repository-url>
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