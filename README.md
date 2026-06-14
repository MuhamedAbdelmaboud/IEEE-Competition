# IEEE-Competition

#  Ice Cream Price Predictor

A simple app that predicts ice cream prices based on the current temperature in your city.

## The Idea

I noticed there's a relationship between temperature and ice cream sales, so I built a model that learns from real data and predicts the price automatically.

The user picks their city, the app fetches the current temperature from the internet, and tells them the expected ice cream price.

## Tools I Used

- **Streamlit** - to build the UI easily
- **scikit-learn** - to build the prediction model
- **pandas** - to read the data
- **Open-Meteo API** - to get the current temperature for free

## How to Run

First install the libraries:

```bash
pip install -r requirements.txt
```

Then run the app:

```bash
streamlit run app.py
```

## Project Files

```
├── app.py                              # main code
├── requirements.txt                    # required libraries
├── Ice_Cream_Sales_-_temperatures.csv  # the dataset
└── README.md                           # you're reading this right now
```

## How the Model Works

1. Reads the dataset which contains temperatures and ice cream prices
2. Learns the relationship between them using Linear Regression
3. When the user picks a city, it fetches the current temperature from Open-Meteo
4. Passes the temperature to the model and returns the predicted price
