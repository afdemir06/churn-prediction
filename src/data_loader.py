import pandas as pd

def load_data(data_path):
    if data_path.endswith(".csv"):
        try:
            data=pd.read_csv(data_path)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Data not found on {data_path}")
    try:
        data=pd.read_excel(data_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Data not found on {data_path}")