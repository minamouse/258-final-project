from music21 import *
import pickle
import math


def accidentals_to_tonic(mode, sharps):

    root = sharps * 7
    if mode == "minor":
        root -= 3

    return root % 12



chord_to_n = {}

inc = 2

chord_to_n['start'] = 0
chord_to_n['end'] = 1

melodies = []
bass_lines = []
sequences = []


for i in range(1, 372):

    if i == 150:
        continue

    name = 'chor' + '{0:0=3d}'.format(i)
    print(name)
    full_name = 'chorales/' + name + '.mid'

    piece = converter.parse(full_name)

    chords = piece.chordify()

    sequence = []
    melody = []
    bass_line = []

    first = None
    st = stream.Stream()

    for c in chords:

        if type(c) == chord.Chord:

            if (c.offset % 1 == 0):
                c.duration.quarterLength = math.ceil(c.duration.quarterLength)

                pitches = [p.midi for p in c.pitches]

                bass_line.append(min(pitches))
                melody.append(max(pitches))

                bass = min(pitches)

                if first == None:
                    first = bass

                bass -= first
                
                figured = [str(p) for p in sorted(list(set([(p-bass)%12 for p in pitches]))) if p != 0]
                
                my_chord = str(bass) + ' ' + ' '.join(figured)

                if my_chord not in chord_to_n:
                    chord_to_n[my_chord] = inc
                    sequence.append(inc)
                    inc += 1
                else:
                    sequence.append(chord_to_n[my_chord])

    melodies.append(melody)
    bass_lines.append(bass_line)
    sequences.append(sequence)

pickle.dump(chord_to_n, open("pickles/dict.p", "wb"))
pickle.dump(melodies, open("pickles/melodies.p", "wb"))
pickle.dump(melodies, open("pickles/bass_lines.p", "wb"))
pickle.dump(melodies, open("pickles/sequences.p", "wb"))

