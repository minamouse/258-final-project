from music21 import *
import pickle

reverse_dict = {}
normal_dict = pickle.load(open('pickles/dict.p', 'rb'))

for k in normal_dict.keys():
    reverse_dict[normal_dict[k]] = k

new_piece = pickle.load(open('result.p', 'rb'))

starting_note = 48

s = stream.Stream()

for i, p in enumerate(new_piece):

    # notes = reverse_dict[p]
    notes = p.split(' ')
    bass = starting_note + int(notes[0])
    others = [bass + int(n) for n in notes[1:]]
    all_notes = [bass]
    all_notes.extend(others)
    c = chord.Chord(all_notes)
    if (i+1) % 8 == 0:
        c.duration.quarterLength = 3
    else:
        c.duration.quarterLength = 1
    s.append(c)

# sp = midi.realtime.StreamPlayer(s)
# sp.play()

fp = s.write('midi', fp='rnn200e1.mid')
