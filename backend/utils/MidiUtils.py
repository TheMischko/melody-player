from collections import namedtuple

import music21
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import re
from music21 import converter, corpus, instrument, midi, note, chord, pitch, stream, meter


class MelodyCharacteristics:
    def __init__(self, stream, chordification, variety):
        self.stream = stream
        self.chordification = chordification
        self.variety = variety

    def __lt__(self, other):
        self_val = self.variety - self.chordification
        other_val = other.variety - other.chordification
        return self_val < other_val


def get_midi_stream(midi_file) -> music21.stream:
    mf = midi.MidiFile()
    mf.open(midi_file)
    mf.read()
    mf.close()
    return midi.translate.midiFileToStream(mf)


def save_midi_stream(melody:music21.stream.Score, midi_stream:music21.stream.Score, path):
    mf = midi.translate.streamToMidiFile(melody)
    mf.open(path, "wb")
    mf.write()
    mf.close()


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


def print_part_countour(part):
    FakeStream = namedtuple("FakeStream", "parts")
    print_parts_countour(FakeStream(parts=[part]))


def print_parts_countour(midi_stream):
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(1, 1, 1)
    minPitch = pitch.Pitch('C10').ps
    maxPitch = 0
    xMax = 0

    # Drawing notes.
    for i in range(len(midi_stream.parts)):
        top = midi_stream.parts[i].flat.notes
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


def get_instruments(midi_stream: stream) -> list:
    stream_parts = midi_stream.parts.stream()
    instruments = list()
    for part in stream_parts.parts.activeElementList:
        instruments.append(part.partName)
    return instruments


def get_melody_part(midi_stream: stream.Score) -> stream:
    melodies = list()
    for part in midi_stream.parts:
        if part.partName == None:
            continue
        melody = part
        top = part.flat.notes
        y, notes = extract_notes(top)
        chordification = get_chordification(notes)
        variety = get_notes_variety(notes)
        melodies.append(MelodyCharacteristics(part, chordification, variety))
    if len(melodies) == 0:
        return None
    melodies.sort()
    melody = melodies[0]
    return melody.stream


def get_chordification(notes: list[music21.note.Note]) -> float:
    if len(notes) == 0: return 0
    num_chords = 0
    for note in notes:
        if note.isChord:
            num_chords += 1
    return num_chords/len(notes)


def get_notes_variety(notes: list[music21.note.Note]) -> float:
    if len(notes) == 0: return 0
    notes_counts = dict()
    for note in notes:
        name = note.nameWithOctave
        if name not in notes_counts.keys():
            notes_counts[name] = 0
        notes_counts[name] = notes_counts[name] + 1

    uniqueness_list = list()
    for (key, val) in notes_counts.items():
        uniqueness_list.append(val/len(notes))
    return np.average(uniqueness_list)

