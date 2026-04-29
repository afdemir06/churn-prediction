from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd

class DataCleaner(BaseEstimator,TransformerMixin):
    def fit(self,x,y=None):
        self.numeric_columns=x.select_dtypes(include=["number"]).columns.tolist()

        self.categoric_columns=x.select_dtypes(include=["object","category"]).columns.tolist()

        self.str_columns_to_numeric=[]
        for col in x.columns:
            if col not in self.numeric_columns:
                sample=x[col].dropna()
                if pd.to_numeric(sample,errors="coerce").notnull().all():
                    self.str_columns_to_numeric.append(col)

        self.new_categoric_columns=list(set(self.categoric_columns)-set(self.str_columns_to_numeric))
        
        all_numeric_columns=self.numeric_columns+self.str_columns_to_numeric

        self.medians=x[all_numeric_columns].median()
        return self
    
    def transform(self,x):
        X=x.copy()

        for col in self.str_columns_to_numeric:
            X[col]=pd.to_numeric(X[col],errors="coerce")

        all_numeric_columns=self.numeric_columns+self.str_columns_to_numeric

        X[all_numeric_columns]=X[all_numeric_columns].fillna(self.medians)

        columns_to_fill=[c for c in self.new_categoric_columns if c in X.columns]
        X[columns_to_fill]=X[columns_to_fill].fillna("Missing")

        return X