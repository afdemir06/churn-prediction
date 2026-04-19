from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib

def train_and_save_model(data,model_path):
    x=data.drop(columns=["Churn"])
    y=data["Churn"]

    rf=RandomForestClassifier(random_state=42)

    param_grid={
        "max_depth":[2,5,7,10,13,None],
        "min_samples_split":[2,5,7],
        "n_estimators":[50,100,150]
    }

    grid=GridSearchCV(rf,param_grid=param_grid,cv=5)
    grid.fit(x,y)

    try:
        joblib.dump(grid.best_estimator_,model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found on {model_path}")