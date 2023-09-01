import os

from music21 import stream

from utils import MidiUtils as mu

MIDI_ROOT = "./data/game_midi"


def prepare_midi_file(path, filename):
    if not os.path.exists(path) or not path.endswith(".mid"):
        return
    print(f"Opening: {path}")
    midi = mu.get_midi_stream(path)
    instruments = mu.get_instruments(midi)

    print(f"Instruments in file are: {instruments}")
    melody = mu.get_melody_part(midi)
    key = melody.analyze("key")

    mu.save_midi_stream(melody, midi, filename)




if __name__ == '__main__':
    dir_content = os.listdir(MIDI_ROOT)
    counter = 0
    for content in dir_content:
        if os.path.isdir(content):
            new_dir_content = os.listdir(content)
            for new_content in new_dir_content:
                dir_content.append(os.path.join(content, new_content))
            continue
        prepare_midi_file(os.path.join(MIDI_ROOT, content), os.path.join(MIDI_ROOT, f"{counter}.mid"))
        counter += 1
        #break

