import sqlite3
import pandas as pd

def create_table(db_path):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()

    query="""
        CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        churn_probability REAL,
        prediction_date TEXT
        )
        """
    cursor.execute(query)
    conn.commit()
    conn.close()

def save_prediction(db_path,values):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()

    query="""
        INSERT INTO predictions (
        customer_id, 
        churn_probability, 
        prediction_date
        )
        VALUES (?,?,?)
        """
    cursor.execute(query,values)
    conn.commit()
    conn.close()

def get_prediction(db_path):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()

    query="""
        SELECT *
        FROM predictions
        """
    cursor.execute(query)
    rows=cursor.fetchall()
    conn.close()

    df=pd.DataFrame(rows,columns=["id","customer_id","churn_probability","prediction_date"])
    return df