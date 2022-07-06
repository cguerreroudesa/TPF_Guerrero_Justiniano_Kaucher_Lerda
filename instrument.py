class Instrument(object):
    def __init__(self, filename):
        if '.txt' not in filename:
            filename = 'instruments/' + filename + '.txt'
        self.filename = filename

    def read_instrument(self):
        with open(self.filename, 'r') as f:
            num_harmonics = f.readline().strip()

            amp_mod={} #modulador de amplitud
            harm_dict = {}
            
            #Tiene multiplicador y la intensida de los armonicos
            for n in range(int(num_harmonics)):
                mult_harm =  f.readline()
                mult_harm = mult_harm.split(' ')
                harm_dict[float(mult_harm[0])] = float(mult_harm[1].strip('\n'))

            for amp in range(3): # 3 = len(filename) - num_armonics - 1
                line = f.readline().split(" ")
                name_funct = line[0].strip()
                if len(line) > 1:
                    del line[0] #Eliminamos funcion de la lista
                    line[len(line)-1] = line[len(line)-1].strip() #Eliminamos \n
                    line = [float(num) for num in line] #Pasamos los elementos de la lista a float
                    amp_mod[name_funct] = line
                elif len(line) == 1:
                    amp_mod[name_funct] = 0
            return harm_dict, amp_mod

