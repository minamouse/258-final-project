from music21 import *
import pickle
import math


chord_sequences = []
melodies = []

for i in range(1, 372):

    if i == 150:
        continue

    name = 'chor' + '{0:0=3d}'.format(i)
    print(name)
    full_name = 'chorales/' + name + '.mid'

    piece = converter.parse(full_name)

    chord_sequence = [[],[],[],[],[],[],[],[],[],[],[],[]]
    melody = [[],[],[],[],[],[],[],[],[],[],[],[]]

    first = None

    highest = 0
    highest_note = 0

    for p, part in enumerate(piece):
        inc = 0
        thing = False
        while not thing:
            if type(part[inc]) == note.Note:
                thing = True
                n = part[inc].pitch.midi
                if n > highest_note:
                    highest_note = n
                    highest = p
            inc += 1


    for n in piece[highest]:
        if type(n) == note.Note:
            if n.offset % 0.5 == 0:
                times = math.ceil(n.duration.quarterLength/0.5)
                pitch = n.pitch.midi - 6
                for intvl in range(12):
                    pitch += 1
                    for t in range(int(times)):
                        if t == 0:
                            melody[intvl].append(str(pitch) + ' b')
                        elif t == times-1:
                            melody[intvl].append(str(pitch) + ' e')
                        else:
                            melody[intvl].append(str(pitch) + ' c')

    chords = piece.chordify()

    for c in chords:
        if type(c) == chord.Chord:
            if c.offset % 0.5 == 0:
                times = math.ceil(c.duration.quarterLength/0.5)
                pitches = [p.midi - 6 for p in c.pitches]
                for intvl in range(12):
                    for t in range(int(times)):
                        if t == 0:
                            chord_sequence[intvl].append(' '.join([str(p + intvl) for p in pitches]) + ' b')
                        elif t == times-1:
                            chord_sequence[intvl].append(' '.join([str(p + intvl) for p in pitches]) + ' e')
                        else:
                            chord_sequence[intvl].append(' '.join([str(p + intvl) for p in pitches]) + ' c')

    melodies.extend(melody)
    chord_sequences.extend(chord_sequence)

pickle.dump(melodies, open("melodies.p", "wb"))
pickle.dump(chord_sequences, open("chords.p", "wb"))
