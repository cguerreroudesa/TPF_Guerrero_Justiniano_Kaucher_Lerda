from modulatorfunctions import ModulatorFunctions

class Modulator():
    def __init__(self, amplitude_mod):
        self.functions = list(amplitude_mod.keys()) # [0] es la funcion de attack, [1] la de sustain y [2] la de decay
        self.parameters = list(amplitude_mod.values()) # [0] son parametros de attack, [1] de sustain y [2] de decay

    def time_mod (self):
        """
        Stablishes the decay and sustain times.

        Returns
        -------
          ta : float
          td : float
        """
        ta = self.parameters[0][0]
        td = self.parameters[2][0]
        return ta, td

    def mod(self, t, t0,d):
        """
        fa, fs, fd are the amplitude modulating functions (a: attack, s: sustain, d:decay)
        ta is attack time, td is decay time, t0 is the instant in wich beggings, d is the duration
        Returns
        -------
            result : numpy.ndarray
        """
        ta, td = self.time_mod()
        if t0 < t and t < (t0+ta):
            result = self.amp_mod('attack', (t-t0))
        elif (t0+ta) < t and t < (t0+d):
            result = self.amp_mod('sustain', (t-(t0+ta)))
        elif (t0+d) < t and t < (t0+d+td):
            result = self.amp_mod('sustain', (t0+d))*self.amp_mod("decay", (t-(t0+d)))
        else:
            result = 0
        return result
        
    def amp_mod(self, types:str, t):
        """
        This function receives a type of amplitude modulator (attack, sustain, or decay) and calculates the respective function.
        Returns
        -------
            result : numpy.ndarray
        """
        if types=="attack":
            i=0
        elif types=="sustain":
            i=1
        elif types=="decay":
            i=2
        function, parameter = self.functions[i], self.parameters[i]
        result= ModulatorFunctions(function, parameter, types, t)
        return result

  