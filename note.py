from notes import notes_mapping

class Note ():
    def __init__ (self, filename):
        if '.txt' not in filename:
            filename = 'instruments/' + filename + '.txt'
        self.filename = filename

    def read_notes (self):
        """
        Receives a file with a partiture and returns a list with the informatin about each song.

        Returns
        -------
          info[0] is the time (in seconds) when the note beggins
          info[1] is the name of the note
          info[2] is the tiem that the note must last.
        """
        with open(self.filename, 'r') as f:
        #aca llamar a funcion que encuentre el largo de la funcion y cree el array de ceros con eso
            lines= f.readlines()
            if '\n' in lines:
                lines.remove('\n')
            ultra_info = []
            for line in lines:
                info = line.split()
                ultra_info.append ( (float(info[0]), info[1], float(info[2])) )
        return ultra_info

    def get_song_len (self):
        """
            This function calls to the function read_notes and returns the lenght of the song inserted.

            Returns
            -------
            song_len : int

        """
        read = self.read_notes()
        f_position = len(read) - 1
        f_note = read[f_position] #Los datos de la ultima nota
        song_len = f_note[0] + f_note [2]  #Start + duracion
        return song_len

    def note_freq (self, note):
        """
          Receives a note, and returns the frecuency of such note.
          Returns
          -------
            freq : float
        """
        for x in notes_mapping:
            if x[0] == note:
                freq = float(x[1])
            return freq

    def frequency (self, note):
        """
          Receives a note, and  if the note is sharp, it makes it flat. If not, the function does not change it.
          Returns
          -------
          freq : float
        
        """
        if 's' in note:
            note = note [0] + note [2] #Elimina s de la nota: As4 -> A4
            freq = self.note_freq(note)
            freq = freq * (1.0594623)
        else:
            freq = self.note_freq (note)
        return freq