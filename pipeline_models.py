import numpy as np

class TeamEnsemblePipeline:
    def __init__(self, m_svr, m_lr, m_xgb, m_ridge, scaler):
        self.m_svr = m_svr
        self.m_lr = m_lr
        self.m_xgb = m_xgb
        self.m_ridge = m_ridge
        self.scaler = scaler
        
    def predict(self, X_raw):
        Xs = self.scaler.transform(X_raw)
        p1 = self.m_svr.predict(Xs)
        p2 = self.m_lr.predict(Xs)
        p3 = self.m_xgb.predict(Xs)
        meta = np.column_stack([p1, p2, p3])
        return self.m_ridge.predict(meta)
