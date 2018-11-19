from music21 import *
import random
import pickle

markov = {}


for i in range(1, 372):

    if i == 150:
        continue

    name = 'chor' + '{0:0=3d}'.format(i)
    full_name = 'pickles/' + name + '.p'

    sequence = pickle.load(open(full_name, 'rb'))

    if str(sequence[0]) in markov:
        markov[str(sequence[0])].append(sequence[1])
    else:
        markov[str(sequence[0])] = [sequence[1]]

    if str(sequence[0]) + ' ' + str(sequence[1]) in markov:
        markov[str(sequence[0])].append(sequence[2])
    else:
        markov[str(sequence[0]) + ' ' + str(sequence[1])] = [sequence[2]]

    for s in range(len(sequence)-3):

        key = str(sequence[s]) + ' ' + str(sequence[s+1]) + ' ' + str(sequence[s+2])

        if key in markov:
            markov[key].append(sequence[s+3])
        else:
            markov[key] = [sequence[s+3]]


pickle.dump(markov, open('pickles/markov.p', 'wb'))


generated_chords = [0]
next = random.choice(markov['0'])
generated_chords.append(next)

key = str(generated_chords[-2]) + ' ' + str(generated_chords[-1])
next = random.choice(markov[key])
generated_chords.append(next)


while next != 1:

    key = str(generated_chords[-3]) + ' ' + str(generated_chords[-2]) + ' ' + str(generated_chords[-1])
    next = random.choice(markov[key])
    generated_chords.append(next)


pickle.dump(generated_chords, open('pickles/new_chords.p', 'wb'))


