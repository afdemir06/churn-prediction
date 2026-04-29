from sklearn.base import BaseEstimator,TransformerMixin

class FeatureEngineer(BaseEstimator,TransformerMixin):
    def fit(self,x,y=None):
        return self
    
    def transform(self,x):
        X=x.copy()
        return X