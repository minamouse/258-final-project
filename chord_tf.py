import pickle
from music21 import *

sequence = []

for i in range(1, 372):

    if i == 150:
        continue

    name = 'chor' + '{0:0=3d}'.format(i)
    full_name = 'chorales/' + name + '.mid'
    print(full_name)

    piece = converter.parse(full_name)

    chords = piece.chordify()

    first = None

    for c in chords:

        if type(c) == chord.Chord:
            pitches = [p.midi for p in c.pitches]

            bass = min(pitches)

            if first == None:
                first = bass

            bass -= first
            
            figured = [str(p) for p in sorted(list(set([(p-bass)%12 for p in pitches]))) if p != 0]
            
            my_chord = str(bass) + ' ' + ' '.join(figured)

            sequence.append(my_chord)


pickle.dump(sequence, open("sequence.p", "wb"))

