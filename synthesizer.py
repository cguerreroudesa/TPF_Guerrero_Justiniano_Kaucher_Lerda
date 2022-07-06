import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from note import Note

class Synthesizer(Note):
  def __init__(self, harm_dict: dict, filename:str, sps: float): # recibe un instrumento y una partitura
    super().__init__(filename)
    self.harm_dict=harm_dict #lista de largo n, compuesta por los n armónicos del instrumento recibido
    self.sps = int(sps)
    
  def zero_array(self, song_len: float):
    """
    Receives a song leght
    Returns an aray of zeros with the same lenght as the song has.

    Returns
    -------
    a: numpy.ndarray
    """
    a = np.zeros(int(self.sps*song_len))
    return a

  def array_sum (self, start:float, dur:float, waveform, zero_array):
    '''
      Adds the sine to its respective space on the x-axis

      Returns
      -------
        zero_array : numpy.ndarray
    '''
    end = start + dur
    if int(self.sps*start) - int(self.sps*end) != len(waveform):
        waveform = waveform[:+1]
    zero_array[int(self.sps*start) : int(self.sps*end)] += waveform # Waveform es la senoidal final de la nota
    return zero_array

  def sine_wave(self, harm: int, amplitude: float, dur:float, freq: float):
    """Creates the sine wave of a note
    harm: the number that multiplies the frequency of the base note, to get the frequency of the overtone
    amplitude: the intensity of the overtone. Must be between 0 and 1
    freq: the frequency of the base note

    Returns
    -------
      y : numpy.ndarray
      """
    y = amplitude * np.sin(2* np.pi * freq * harm * np.arange(self.sps*dur)/self.sps)
    return y

  def harm_sum (self, duration, freq):
    '''Suma de los armonicos a cada nota'''
    harm_sum = 0
    for harm in self.harm_dict.keys():
      sen = self.sine_wave(harm, self.harm_dict[harm], duration, freq)
      harm_sum += sen
    return harm_sum

  def signal_generator (self):
    """
      This function calls to the function read_notes, get_song_len and returns the song's signal

      Returns
      -------
        wave : numpy.ndarray
    """
    read = self.read_notes()
    song_len = self.get_song_len()
    zero_array = self.zero_array(song_len)
    array_list = []
    count = 0
    for a in read:
      start = a[0]
      note = a[1]
      duration = a[2]

      freq = self.frequency (note)
      harm_sum = self.harm_sum(duration, freq) #ESTO ES Y(T)
      t = np.arange(self.sps * song_len)

      #mod_sine = self.mod (t, start, duration)
      temp_array = self.array_sum(start, duration, harm_sum, zero_array) #En vez de harm_sum deberia ser mod_sine
      array_list.append(temp_array)
      count += 1
    final_array = sum(array_list)
    wave = final_array * 1 / np.max( np.abs(final_array) )
    return wave

  def make_wav(self, name):
      """Creates and saves the .wav file
      final_sine: the function made from the sum of all of the notes in the song, with the respective amplitude modifiers.
      name: the name"""
      signal = self.signal_generator()
      #signal = self.normalize (signal)
      waveform_ints = np.int16(signal * (32767 / np.max(np.abs(signal))))
      if ".wav" not in name:
          name += ".wav"
      write(name, self.sps, waveform_ints)


