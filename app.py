import streamlit as st
import pandas as pd
import plotly.express as px
from src import data_cleaner,data_loader,db_commands,feature_engineering,model_trainer,predictor
import os
import numpy as np
import datetime

page=st.sidebar.radio("Choose Page",["Dataset Owerview","Churn Prediction","Old Predictions"])

@st.cache_data
def process_data(df):
    df=data_cleaner.clean_data(df)
    df=feature_engineering.apply_features(df)
    if not os.path.exists(os.path.join(os.path.dirname(__file__),"models","model.joblib")):
        model_trainer.train_and_save_model(df,os.path.join(os.path.dirname(__file__),"models","model.joblib"))
    return df

if page=="Dataset Owerview":
    data=st.file_uploader("Upload Your File",type=["csv","xlsx"])
    if data is not None:
        if data.name.endswith(".csv"):
            df=pd.read_csv(data)
        else:
            df=pd.read_excel(data)
        st.session_state["data"]=df

        fig1=px.pie(df,names="Churn",title="Churn Distribution")
        st.plotly_chart(fig1)
        col1,col2=st.columns(2)
        col1.metric("Row",df.shape[0])
        col2.metric("Column",df.shape[1])

        fig2=px.histogram(df,x="tenure",title="Customer Tenure")
        st.plotly_chart(fig2)

        fig3=px.histogram(df,x="MonthlyCharges",title="Monthly Charges")
        st.plotly_chart(fig3)

        fig4=px.histogram(df,x="Contract",title="Customer Contract")
        st.plotly_chart(fig4)

        fig5=px.box(df,x="Churn",y="MonthlyCharges",title="Monthly Charges by Churn")
        st.plotly_chart(fig5)

        fig6=px.box(df,x="Churn",y="tenure",title="Tenure by Churn")
        st.plotly_chart(fig6)

elif page=="Churn Prediction":
    if "data" not in st.session_state:
        st.info("Please upload your file at Dataset Owerview page")
    else:
        df=st.session_state["data"]
        customer_id=df["customerID"]

        processed_data=process_data(df)

        model=predictor.load_model(os.path.join(os.path.dirname(__file__),"models","model.joblib"))

        prediction=predictor.predict(processed_data.drop(columns=["Churn"]),model)

        risk=np.where(prediction*100<50,"Low Risk","High Risk")

        result_dict={
            "Risk":risk,
            "Probability":prediction*100
        }
        st.write(pd.DataFrame(result_dict))

        DB_PATH=os.path.join(os.path.dirname(__file__),"database","churn.db")
        db_commands.create_table(DB_PATH)
        for i in range(len(customer_id)):
            db_commands.save_prediction(
                DB_PATH,
                (
                    customer_id[i],
                    prediction[i]*100,
                    datetime.datetime.now()
                )
            )

else:
    DB_PATH=os.path.join(os.path.dirname(__file__),"database","churn.db")
    predicted_df=db_commands.get_prediction(DB_PATH)
    if predicted_df.empty:
        st.error("No data found at database")
    else:
        risk_level=st.selectbox("Select Risk Level",options=["High Risk","Low Risk"])
        if risk_level=="High Risk":
            st.write(predicted_df[predicted_df["churn_probability"]>50])
        else:
            st.write(predicted_df[predicted_df["churn_probability"]<=50])
