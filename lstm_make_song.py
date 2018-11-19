from music21 import *
import pickle

state_name = "state/1/"
melody = pickle.load(open(state_name + "predictions/melody.p", "rb"))
chords = pickle.load(open(state_name + "predictions/chords.p", "rb"))

notes = []
n_durations = []
inc = -1
for m in melody:
    if m != 'r':
        mid, pos = m.split(' ')

        if pos == 'b':
            inc += 1
            n_durations.append(0.5)
            notes.append(mid)
        else:
            n_durations[inc] += 0.5

            


accompaniment = []
a_durations = []
inc = -1
for c in chords:
    if c != 'r':
        n = c.split(' ')
        pos = n[-1]

        if pos == 'b':
            inc += 1
            a_durations.append(0.5)
            accompaniment.append(' '.join(n[:-1]))
        else:
            a_durations[inc] += 0.5


st = stream.Stream()

p = stream.Part()

for i, n in enumerate(notes):
    nn = note.Note(int(n))
    nn.duration.quarterLength = n_durations[i]
    p.append(nn)

st.append(p)

pp = stream.Part()

for i, c in enumerate(accompaniment):
    cc = chord.Chord([int(n) for n in c.split(' ')])
    cc.duration.quarterLength = a_durations[i]
    pp.append(cc)

st.append(pp)
sp = midi.realtime.StreamPlayer(st)
sp.play()
# fp = st.write('midi', fp='lstm50e2.mid')
