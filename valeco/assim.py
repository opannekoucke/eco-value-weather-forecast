import numpy as np
class EnKF(object):
    '''
        Algorithme d'assimilation de données
    '''
    def __init__(self,model,observation):
        self.model=model
        self.observation = observation
    
    def analysis(self, time, Xf):
        '''
        description
        -----------
            Etape d'analyse
            ef  : ensemble of forecasts
            Xb  :   type Ensemble
            yo  :   type Observation
        ref.
        ---
            Burgers, G.; van Leeuwen, P. J. & Evensen, G. 
            Analysis Scheme in the Ensemble Kalman Filter 
            Monthly Weather Review, 1998, 126, 1719-1724
        '''
        # Computation of gain matrix K at 'time'
        obs = self.observation
        H = obs.H
        Be = EnKF.make_Be(Xf)
        R = obs.R
        Ke=Be * H * (H * Be * H.T + R)**-1
        # Analysis update + random error observation.
        yo = np.asmatrix(observations[time]).T
        Xa = []
        for xf in Xf:
            xf = np.asmatrix(xf).T
            eo = obs.generate_error(vector=True)
            d = yo+eo - H*xf
            xa = xf + Ke * d
            Xa.append( np.asarray( xa.T ).flatten() )
        return Xa
    
    def forecast(self, forecast_window, Xa):
        time_start = forecast_window[0]
        Xf=self.model.forecast(forecast_window,Xa[time_start])
        return Xf
    
    @staticmethod
    def make_Mean(X):
        Ne,n=len(X), len(X[0])
        # Compute the mean
        mean=0.0
        for k in range(Ne):
            mean += X[k]
        mean=mean/ float( Ne)
        return mean
    
    @staticmethod
    def make_Be(X):
        '''
        Description
        -----------
            Compute the empirical covariance matrix associated with the ensemble
            contained in the list X.
        Input
        -----
            X : list of model state vector.
        Output
        ------
            Be: empirical covariance matrix.
        '''
        Ne,n=len(X), len(X[0])
        # Compute the mean
        mean=EnKF.make_Mean(X)
        # Compute the errors
        Be = 0.0
        for k in range(Ne):
            err = X[k]-mean
            err = np.asmatrix(err).T
            Be += err * err.T  # Invers the e*e.T since compute with array
        Be=Be/float(Ne-1.)
        return Be