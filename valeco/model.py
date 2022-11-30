import numpy as np
import sympkf

__all__ = ["Nature", "Persistence", "Climate"]



class Nature(sympkf.Model):

    """
    Nature corresponds to the true dynamics of the atmosphere.
    Here the nature is assumed to be governed by the Lorenz 1963 equations.

    Reference
    ---------

    E. N. Lorenz, “Deterministic nonperiodic flow” 
    Journal Atmospheric Sciences, vol. 20, pp. 130–141, 1963, 
    doi: 10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2.
    https://doi.org/10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2
    """

    _dt_lorenz63 = 0.01
    def __init__(self, r=27, b=8/3, sigma=10 , f=0., dt = 0.25):
        super().__init__()
        self.n = 3
        self.set_dt(dt)
        self.epsilon = self._dt_lorenz63 / self.dt
        self.sigma = sigma
        self.b = b
        self.r = r
        self.f = f
        
    def trend(self, t, x):
        X, Y, Z = x
        dX = self.sigma*(Y-X) + self.f
        dY = -X*Z + self.r * X -Y + self.f
        dZ = X*Y - self.b*Z
        dx = self.epsilon * np.array([dX, dY, dZ])
        return dx
    
    def typical_state(self,randflag=False):
        """
        Creates a typical state of the dynamics from a 
        long-time integration starting from a given state 
        (and with/out initial perturbation)
        """
        x0 = np.array([1.,0.,0.])
        if randflag: x0 += np.random.normal(size=3)*0.1
        long_time_window = np.arange(3000) * self.dt
        end_time = long_time_window[-1]
        forecast = self.forecast( long_time_window, x0, [ end_time ])
        return forecast[end_time]
    
    @staticmethod
    def state2FF(xt):
        '''
        Description
        -----------
            Convert Lorenz 63's state into wind velocity
        '''
        if type(xt)==list:
            return [ Lorenz1963.state2FF(x) for x in xt ]
        else:
            FFt=float(0.3/25.*xt[2])
            FFt=FFt*(1.0 + (FFt/0.3)**4 *0.07)
            return FFt

class Persistence(sympkf.Model):
    
    def trend(self,t,x):
        return np.zeros(x.shape)
    
class Climate(Persistence):
    
    def __init__(self, climate_data):
        super().__init__()
        self._mean = climate_data.mean(axis=0)
    
    def predict(self, window, state, saved_times=None):
        return super().predict(window, self._mean, saved_times=saved_times)