import joblib

def load_model(model_path):
    return joblib.load(model_path)

def predict(data,model):
    return model.predict_proba(data)[:,1]