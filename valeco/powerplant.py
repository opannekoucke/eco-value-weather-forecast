import numpy as np

class WindPowerPlant(object):
    
    @staticmethod
    def FF2PE(FF):
        '''
        Transfert function that give the eolien production versus the wind 
        force.
    
        Description
        -----------
            Old form:   spline
            New form:   0.5(1+tanh(-5+10 FF))
    
        Note
        ----
            This corresponds to simple spline curve.
        spl(0)= dx spl(0) = dx spl(1) = 0
        spl(1)= 1
        v=x.^2*(-2*x+3);
        '''
        if type(FF)==list:
            return [ EolianPowerPlant.FF2PE(locFF) for locFF in FF ]
        else:
            return 0.5*(1.0+np.tanh(-5.+10.*FF))