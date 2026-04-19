**Churn Prediction App**

*What does this app do?*
    It is an end-to-end project that predicts whether the customer will churn or not by training a Random Forest model with uploaded CSV or excel data.

    -Firstly, user upload a CSV or excel data at first page named Dataset Owerview and the app processes it to train model.
    -The model gets trained and gets ready to predict.
    -Prediction is made based on the given data at second page named Churn Prediction and the results are saved to database as probability.
    -User is able to see the old predictions at third page named Old Predictions.

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Technologies
    -Python
    -Streamlit
    -Scikit-learn
    -Plotly
    -SQLite