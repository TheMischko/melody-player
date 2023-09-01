import music21
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import re
from music21 import converter, corpus, instrument, midi, note, chord, pitch


INDEX_FILES = ["./data/maestro/maestro.csv"]


def extract_notes(midi_part):
    parent_element = []
    ret = []
    for nt in midi_part.flat.notes:
        if isinstance(nt, note.Note):
            ret.append(max(0.0, nt.pitch.ps))
            parent_element.append(nt)
        elif isinstance(nt, chord.Chord):
            for pitch in nt.pitches:
                ret.append(max(0.0, pitch.ps))
                parent_element.append(nt)

    return ret, parent_element


def print_parts_countour(midi):
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(1, 1, 1)
    minPitch = pitch.Pitch('C10').ps
    maxPitch = 0
    xMax = 0

    # Drawing notes.
    for i in range(len(midi.parts)):
        top = midi.parts[i].flat.notes
        y, parent_element = extract_notes(top)
        if (len(y) < 1): continue

        x = [n.offset for n in parent_element]
        ax.scatter(x, y, alpha=0.6, s=7)

        aux = min(y)
        if (aux < minPitch): minPitch = aux

        aux = max(y)
        if (aux > maxPitch): maxPitch = aux

        aux = max(x)
        if (aux > xMax): xMax = aux

    for i in range(1, 10):
        linePitch = pitch.Pitch('C{0}'.format(i)).ps
        if (linePitch > minPitch and linePitch < maxPitch):
            ax.add_line(mlines.Line2D([0, xMax], [linePitch, linePitch], color='red', alpha=0.1))

    plt.ylabel("Note index (each octave has 12 notes)")
    plt.xlabel("Number of quarter notes (beats)")
    plt.title('Voices motion approximation, each color is a different instrument, red lines show each octave')
    plt.show()


def list_instruments(midi):
    partStream = midi.parts.stream()
    print("List of instruments found on MIDI file:")
    for p in partStream:
        aux = p
        print (p.partName)


def handle_midi_file(midi_file):
    mf = midi.MidiFile()
    mf.open(midi_file)
    mf.read()
    mf.close()
    base_midi = midi.translate.midiFileToStream(mf)

    list_instruments(base_midi)
    #base_midi.plot('histogram', 'pitchClass', 'count')



if __name__ == '__main__':
    melody_data = list()
    for index in INDEX_FILES:
        path_prefix = "/maestro-v3.0.0" if index.__contains__("maestro") else ""
        index_content = pd.read_csv(index, delimiter=',')
        for midi_row in index_content.iloc[2:10].itertuples():
            midi_path = re.sub(r"\/[^\/]*$", f"{path_prefix}/{midi_row.filename}", index)
            handle_midi_file(midi_path)
