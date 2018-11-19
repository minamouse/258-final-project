import tensorflow as tf
import numpy as np
import pickle


class Model(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, units):
        super(Model, self).__init__()
        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)

        if tf.test.is_gpu_available():
          self.gru = tf.keras.layers.CuDNNGRU(self.units, 
                                              return_sequences=True, 
                                              recurrent_initializer='glorot_uniform',
                                              stateful=True)
        else:
          self.gru = tf.keras.layers.GRU(self.units, 
                                         return_sequences=True, 
                                         recurrent_activation='sigmoid', 
                                         recurrent_initializer='glorot_uniform', 
                                         stateful=True)

        self.fc = tf.keras.layers.Dense(vocab_size)
        
    def call(self, x):
        embedding = self.embedding(x)

        # output at every time step
        # output shape == (batch_size, seq_length, hidden_size) 
        output = self.gru(embedding)

        # The dense layer will output predictions for every time_steps(seq_length)
        # output shape after the dense layer == (seq_length * batch_size, vocab_size)
        prediction = self.fc(output)

        # states will be used to pass at every step to the model while training
        return prediction



sequence = pickle.load(open("sequence.p", "rb"))

vocab = sorted(set(sequence))

vocab_size = len(vocab)

# The embedding dimension 
embedding_dim = 256

# Number of RNN units
units = 1024

checkpoint_dir = './training_checkpoints'

model = Model(vocab_size, embedding_dim, units)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))

char2idx = {u:i for i, u in enumerate(vocab)}

# Evaluation step (generating text using the learned model)

# Number of characters to generate
num_generate = 48

# You can change the start string to experiment
start_string = '0 4 7'

# Converting our start string to numbers (vectorizing) 
input_eval = [char2idx[start_string]]
input_eval = tf.expand_dims(input_eval, 0)

# Empty string to store our results
text_generated = []

# Low temperatures results in more predictable text.
# Higher temperatures results in more surprising text.
# Experiment to find the best setting.
temperature = 1.0


# Evaluation loop.

# Here batch size == 1
model.reset_states()
for i in range(num_generate):
    predictions = model(input_eval)
    # remove the batch dimension
    predictions = tf.squeeze(predictions, 0)

    # using a multinomial distribution to predict the word returned by the model
    predictions = predictions / temperature
    predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
    
    # We pass the predicted word as the next input to the model
    # along with the previous hidden state
    input_eval = tf.expand_dims([predicted_id], 0)
    
    text_generated.append(idx2char[predicted_id])

final = [start_string]
final.extend(text_generated)
pickle.dump(final, open("result.p", "wb"))
