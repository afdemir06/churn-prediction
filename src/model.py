from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import make_column_selector as selector
from src.data_cleaning import DataCleaner
from src.feature_engineering import FeatureEngineer
from sklearn.feature_selection import SelectFromModel

def create_pipeline(model=None):
    if model is None:
        model=RandomForestClassifier(n_estimators=100,class_weight="balanced",random_state=42)

    preprocessor=ColumnTransformer(
        transformers=[
            ("num","passthrough",selector(dtype_include=["number"])),
            ("cat",OneHotEncoder(handle_unknown="ignore"),selector(dtype_include=["object","category"]))
        ]
    )

    pipeline=ImbPipeline(
        steps=[
            ("cleaner",DataCleaner()),
            ("feature_engineer",FeatureEngineer()),
            ("preprocessor",preprocessor),
            ("feature_selector",SelectFromModel(RandomForestClassifier(n_estimators=50),threshold="mean")),
            ("model",model)
        ]
    )

    return pipeline