# ./sintetizador [-f <frecuencia>] -i <instrumento> -p <partitura> -o <
# audio.wav>
# sintetizador [-f <frecuencia>] [-i <instrumento>] -p <partitura> -o <
# audio.wav>

import argparse
from instrument import Instrument
from synthesizer import Synthesizer
from note import Note
from mod import Modulator

parser = argparse.ArgumentParser(description = "Generar un archivo wav dada una partitura y un instrumento")
parser.add_argument("-f", "--frecuencia", type=int, required=True, help="Frecuencia de muestreo de las notas")
parser.add_argument("-i", "--instrumento", type=str, required=True, help="El instrumento de la libreria que se quiere utilizar para el sintetizador")
parser.add_argument("-p", "--partitura", type=str, required=True, help="La partitura que se quiere sintetizar")
parser.add_argument("-o", "--wavname", type=str, required=True, help="El nombre con el que se desea guardar el archivo de la cancion sintetizada")
args = parser.parse_args()

def main (frecuencia, instrumento, partitura, audio):
    instrument = Instrument(instrumento)

    harm_dict, amp_dict = instrument.read_instrument()

    score = Note(partitura)

    mod = Modulator(amp_dict)

    synth = Synthesizer(harm_dict, frecuencia)

    synth.make_wav(audio)

if __name__ == "__main__":
    main(args.frecuencia, args.instrumento, args.partitura, args.wavname)