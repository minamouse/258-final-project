import math
import pickle
import numpy as np
from music21 import *
from keras.models import Model, Input
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional

state_name = "state/1/"

notes = pickle.load(open(state_name + "notes.p", "rb"))
chords = pickle.load(open(state_name + "chords.p", "rb"))

note2idx = pickle.load(open(state_name + "note2idx.p", "rb"))
chord2idx = pickle.load(open(state_name + "chord2idx.p", "rb"))

max_len = pickle.load(open(state_name + "max_len.p", "rb"))
n_notes = len(notes)
n_chords = len(chords)

input = Input(shape=(max_len,))
model = Embedding(input_dim=n_notes, output_dim=50, input_length=max_len)(input)
model = Dropout(0.1)(model)
model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
out = TimeDistributed(Dense(n_chords, activation="softmax"))(model)

model = Model(input, out)

model.load_weights("model")

# test = ['67 b', '67 c', '67 e', '67 b', '69 b', '69 c', '69 c', '69 e', '67 b', '67 c', '67 c', '67 e', '72 b', '72 c', '72 c', '72 e', '71 b', '71 c', '71 c', '71 c', '71 c', '71 c', '71 c', '71 e', '67 b', '67 c', '67 e', '67 b', '69 b', '69 c', '69 c', '69 e', '67 b', '67 c', '67 c', '67 e', '74 b', '74 c', '74 c', '74 e', '72 b', '72 c', '72 c', '72 c','72 c', '72 c', '72 c', '72 e']

piece = converter.parse("ode.mid")
notes1 = [n.pitch.midi for n in piece[0] if type(n) == note.Note]
offsets = [n.offset for n in piece[0] if type(n) == note.Note]

lengths = [offsets[i+1] - offsets[i] for i in range(len(offsets)-1)]
lengths.append(2.0)

new_notes = []
new_beginnings = []

for i in range(len(lengths)):
    for l in range(int(lengths[i]/0.5)):
        new_notes.append(notes1[i])
        if l == 0:
            new_beginnings.append('b')
        elif l == int(lengths[i]/0.5) - 1:
            new_beginnings.append('e')
        else:
            new_beginnings.append('c')

test = [str(i) + ' ' + c for i, c in zip(new_notes, new_beginnings)]

test = [note2idx[t] for t in test]

test = pad_sequences(maxlen=max_len, sequences=[test], padding="post", value=n_notes-1)


p = model.predict(np.array(test))
p = np.argmax(p, axis=-1)

melody_notes = [notes[w] for w in test[0]]
predicted_chords = [chords[pred] for pred in p[0]]


pickle.dump(melody_notes, open(state_name + "predictions/melody.p", "wb"))
pickle.dump(predicted_chords, open(state_name + "predictions/chords.p", "wb"))

