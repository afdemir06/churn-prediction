from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pandas as pd
from src import model,utils
import joblib
import json
import os

app=FastAPI()

class TrainRequest(BaseModel):
    raw_train_data_path:str
    target_column:str

class PredictionRequest(BaseModel):
    model_name:str
    raw_prediction_data_path:str

@app.post("/train-model")
async def train_model(request: TrainRequest):
    if request.raw_train_data_path.endswith(".csv"):
        raw_train_df=pd.read_csv(request.raw_train_data_path)
    else:
        raw_train_df=pd.read_excel(request.raw_train_data_path)
    x=raw_train_df.drop(columns=[request.target_column])
    y=raw_train_df[request.target_column]
    pipeline=model.create_pipeline()
    pipeline.fit(x,y)
    feature_names=x.columns.tolist()
    version=utils.save_model(pipeline,feature_names)
    return {"status":"success","version":f"v{version}"}

@app.post("/predict")
async def predict_proba(request: PredictionRequest):
    if request.raw_prediction_data_path.endswith(".csv"):
        raw_prediction_data=pd.read_csv(request.raw_prediction_data_path)
    else:
        raw_prediction_data=pd.read_excel(request.raw_prediction_data_path)
    model_metadata_file=f"models/{request.model_name.replace('.joblib','_metadata.json')}"
    if not os.path.exists(model_metadata_file):
        raise HTTPException(status_code=404,detail="Metadata file doesn't exist")
    else:
        with open(model_metadata_file,"r") as f:
            models_metadata=json.load(f)
        if set(raw_prediction_data.columns)!=set(models_metadata["features"]):
            raise HTTPException(status_code=400,detail="Data columns don't match")
        else:
            model_=joblib.load(f"models/{request.model_name}")

            raw_prediction_data=raw_prediction_data.reindex(columns=models_metadata["features"])
            prediction_result=model_.predict_proba(raw_prediction_data)[:,1].tolist()
            return {"status":"success","prediction":prediction_result}