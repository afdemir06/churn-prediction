import pandas as pd

def drop_id_column(data):
    data=data.drop(columns=["customerID"])
    return data

def encode_churn_column(data):
    data["Churn"]=data["Churn"].map({"Yes":1,"No":0})
    return data

def convert_total_charges(data):
    data["TotalCharges"]=pd.to_numeric(data["TotalCharges"],errors="coerce")
    return data

def fill_total_charges_nan(data):
    data["TotalCharges"]=data["TotalCharges"].fillna(data["TotalCharges"].median())
    return data

def clean_data(data):
    data=drop_id_column(data)
    data=encode_churn_column(data)
    data=convert_total_charges(data)
    data=fill_total_charges_nan(data)

    return data