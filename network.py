import numpy as np
import pandas as pd
import tensorflow
from tensorflow.keras import Sequential, Model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, GlobalAveragePooling1D, Dropout, Dense
from tensorflow.keras.optimizers import Adam
import json

MAX_FEATURES = 25000
MAX_LEN = 150
EMBEDDING_SIZE = 300


class Tokenizer:
    def __init__(self):
        with open("./tokenizer.json") as f:
            self.tokenizer = tokenizer_from_json(json.load(f))

    def tokenize(self, text):
        tokenized_text = self.tokenizer.texts_to_sequences(text)
        return pad_sequences(tokenized_text, maxlen=MAX_LEN)


class Network:
    def __init__(self):
        embedding_matrix = self.load_embedding()
        self.model = Sequential()
        self.model.add(Embedding(MAX_FEATURES, EMBEDDING_SIZE,
                       name="embedding", input_shape=(MAX_LEN, ), trainable=False))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(GlobalAveragePooling1D())
        self.model.add(Dense(32, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(16, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(6, activation='sigmoid'))

        self.model.get_layer("embedding").set_weights([embedding_matrix])

        self.model.compile(loss='binary_crossentropy', optimizer=Adam(
            learning_rate=1e-3), metrics=['accuracy'])

        self.model.load_weights("./model.weights.h5", skip_mismatch=True)

    def load_embedding(self):
        embedding_matrix = np.load('./embedding_matrix.npy')
        return embedding_matrix

    def predict(self, tokenized_text):
        return self.model.predict(tokenized_text)
