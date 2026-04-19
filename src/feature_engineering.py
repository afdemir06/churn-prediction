import pandas as pd

def label_encode(data):
    columns_to_labeled=[]
    for col in data.select_dtypes(include="str").columns:
        if data[col].nunique()==2:
            columns_to_labeled.append(col)
    for i in columns_to_labeled:
        unique_values=data[i].unique()
        data[i]=data[i].map({unique_values[0]:0,unique_values[1]:1})
    return data

def one_hot_encode(data):
    df=data.copy()
    colums_to_one_hot=[]
    for col in data.select_dtypes(include="str").columns:
        if data[col].nunique()>2:
            colums_to_one_hot.append(col)
    df=pd.get_dummies(df,columns=colums_to_one_hot,drop_first=True)
    return df

def apply_features(data):
    df=data.copy()
    df=label_encode(df)
    df=one_hot_encode(df)

    return df