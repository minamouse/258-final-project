import pickle
import numpy as np
import pandas as pd
from keras.models import Model, Input
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional


state_name = "state/2/"

print("Loading Data...")
melodies = pickle.load(open("melodies.p", "rb"))
chord_sequences = pickle.load(open("chords.p", "rb"))

max_len = max([len(m) for m in melodies])

print("Number of Data Points: " + str(len(melodies)))

notes = []
for m in melodies:
    notes.extend(m)
notes = list(set(notes))
notes.append('r')

chords = []
for c in chord_sequences:
    chords.extend(c)
chords = list(set(chords))
chords.append('r')

note2idx = {w: i for i, w in enumerate(notes)}

chord2idx = {t: i for i, t in enumerate(chords)}

n_notes = len(notes)
n_chords = len(chords)

pickle.dump(notes, open(state_name + "notes.p", "wb"))
pickle.dump(chords, open(state_name + "chords.p", "wb"))

pickle.dump(note2idx, open(state_name + "note2idx.p", "wb"))
pickle.dump(chord2idx, open(state_name + "chord2idx.p", "wb"))

pickle.dump(max_len, open(state_name + "max_len.p", "wb"))


print("Processing Data...")

X = [[note2idx[w] for w in m] for m in melodies]
X = pad_sequences(maxlen=max_len, sequences=X, padding="post", value=n_notes-1)

y = [[chord2idx[w] for w in c] for c in chord_sequences]
y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=n_chords-1)


y = [to_categorical(i, num_classes=n_chords) for i in y]


X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.1)


print("Setting Up Model...")
input = Input(shape=(max_len,))
print('1')
model = Embedding(input_dim=n_notes, output_dim=50, input_length=max_len)(input)
print('2')
model = Dropout(0.1)(model)
print('3')
model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
print('4')
out = TimeDistributed(Dense(n_chords, activation="softmax"))(model)
print('5')
model = Model(input, out)
print('6')
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
print('7')
history = model.fit(X_tr, np.array(y_tr), batch_size=32, epochs=1, validation_split=0.1, verbose=1)
print('8')
model.save_weights(state_name + "model")


