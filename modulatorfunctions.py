import numpy as np

class ModulatorFunctions:
    def _init_(self, function, parameters, types, t):
        """
        This class receives a function name, that function's parameters, and the type of the modulator (it could be attack, sustain or decay).
        """
        self.types = types
        self.function=function
        self.parameters=parameters
        self.t=t

    def modulate(self):
        """
        This functions receives a function name and calls to that specific function, with its respectic arguments. 
        """
        if self.function in ("LINEAR", "INVLINEAR", "EXP", "INVEXP", "QUARTCOS", "QUARTSIN", "HALFCOS", "HALFSIN", "LOG", "INVLOG"):
            functions={"LINEAR": self.linear(self.parameters[0]), 
                   "INVLINEAR": self.invlinear(self.parameters[0]), 
                   "EXP": self.exp(self.parameters[0]),
                   "INVEXP": self.invexp(self.parameters[0]),
                   "QUARTCOS": self.quartcos(self.parameters[0]),
                   "QUARTSIN": self.quartsin(self.parameters[0]),
                   "HALFCOS": self.halfcos(self.parameters[0]),
                   "HALFSIN": self.halfsin(self.parameters[0]),
                   "LOG": self.log(self.parameters[0]),
                   "INVLOG": self.invlog(self.parameters[0])}

        elif self.function in ("sin"):
            functions={"SIN": self.sin(self.parameters[0], self.parameters[1])}

        elif self.function in ("tri", "pulses"):
            functions={"TRI": self.tri(self.parameters[0], self.parameters[1], self.parameters[2]),
                   "PULSES": self.pulses(self.parameters[0], self.parameters[1], self.parameters[2])}

        else:
            functions={"CONSTANT": self.constant()}

        return functions[self.function]
         
    def constant(self, t):
        if self.types == 'sustain':
            y = 0*t+1
            return y
        else: 
            self.raise_error()
        
    def linear(self, t, t0): 
       if self.types == 'attack':
           y = t/t0
           return y
       else: 
            self.raise_error()
        
    def invlinear(self, t, t0):  
        if self.types == 'sustain' or self.types == 'decay':
            if (1-(t/t0)) <= 0:
                y = 0
            elif (1-(t/t0)) > 0:
                y = 1-(t/t0)
            return y
        else: 
            self.raise_error()

    def sin(self, t, a, f):   
        if self.types == 'sustain':
            y = 1 + a*np.sin(2*np.pi*f*t)  
            return y
        else: 
            self.raise_error()

    def exp(self, t, t0): 
        if self.types == 'attack':
            y = np.exp((5*(t-t0))/t0)
            return y

        else: 
            self.raise_error()

    def invexp(self, t, t0): 
        if self.types == 'sustain' or self.types == 'decay':     
            y = np.exp((-5*t)/t0)
            return y
        else: 
            self.raise_error()
        
    def quartcos(self, t, t0): 
        if self.types == 'sustain' or self.types == 'decay':
            y = np.cos(((np.pi)*t)/(2*t0))
            return y
        else: 
            self.raise_error()
        
    def quartsin(self, t, t0): 
        if self.types == 'attack':
            y = np.sin(((np.pi)*t)/(2*t0))
            return y
        else: 
            self.raise_error()
        
    def halfcos(self, t, t0): 
        if self.types == 'sustain' or self.types == 'decay':
            y = (1 + np.cos((np.pi*t)/t0))/2
            return y
        else: 
            self.raise_error()

    def halfsin(self, t, t0):   
        if self.types == 'attack':
            y = (1 + np.cos((np.pi*t)/t0))/2
            return y
        else: 
            self.raise_error()

    def log(self, t, t0): 
        if self.types == 'attaack':
            y=  np.log10(((9*t)/t0) + 1)
            return y
        else: 
            self.raise_error()

    def invlog(self, t, t0): 
        if self.types == 'sustain' or self.types == 'decay':   
            if t.all() < t0:
                y = np.log10(((-9*t)/t0) + 10)
            elif t.all() >= t0:
                y = 0
            return y
        else: 
            self.raise_error()

    def tri(self, t, t0, t1, a1): 
        if self.types == 'attack':
            if t0 in t:
                ta=t[:(t.index(t0))]
                tb=t[(t.index(t0)+1):]
                
                y1=(ta*a1)/t1
                y2=((tb-t1)/(t1-t0))+a1
                y=y1+y2
            return y
        else:
            self.raise_error()
            


    def pulses(self, t, t0, t1, a1): 
        # sustain
        if self.types == 'sustain':
            t_prima = (t/t0)
        else: 
            raise ArithmeticError
     
        """ 
        t_prima = t/t0 - mod(t/t0)
        f(t_prima) = min{ mod(((1-a1)/t1)*(t_prima - t0 + t1)) + a1}
        """
    
    def raise_error(self):
        print("This type of function cannot be used with this amplitude modulator")
        return ()
