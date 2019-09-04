import os
import sys
import numpy as np
import json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding, Dropout
from keras.models import Model, model_from_json
from keras.initializers import Constant


MAX_SEQUENCE_LENGTH = 1000
MAX_NUM_WORDS = 200
EMBEDDING_DIM = 50
VALIDATION_SPLIT = 0.22
DIR_NAME = "Artykuły Baza"


def process_articles():
    # prepare text samples and their labels
    print('Processing articles dataset')
    articles_names = []
    articles = []  # list of text samples
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids
    try:
        for name in sorted(os.listdir(DIR_NAME)):
            art_num_in_cat = 0
            path = os.path.join(DIR_NAME, name)
            if os.path.isdir(path):
                label_id = len(labels_index)
                labels_index[name] = label_id
                for fname in sorted(os.listdir(path)):
                    fpath = os.path.join(path, fname)
                    args = {} if sys.version_info < (3,) else {'encoding': 'utf-8'}
                    with open(fpath, **args) as f:
                        try:
                            articles_names.append(fname)
                            articles.append(fname + f.read())
                        except:
                            print("Problem z kodowaniem w artykule")
                            continue
                    labels.append(label_id)
                    art_num_in_cat += 1
    except:
        print("Błąd przy czytaniu bazy danych dla nauki klasyfikatora! Czy pobrane zostały artykuły do bazy?")
        exit(0)

    print('Found %s articles.' % len(articles))
    return articles, labels, labels_index


def teach_model_or_not():
    while 1:
        corpus = input("Teach a new model? If not a already taught one will be used. [y/n] ")
        if corpus == 'y':
            return True
        elif corpus != 'n':
            continue
        else:
            return False


class KerasModel:
    def __init__(self, articles_to_predict, labels_to_predict, titles_pred):
        if teach_model_or_not():
            self.embeddings_index = self.get_vectors()
            self.articles, self.labels, self.labels_index = process_articles()
            self.data, self.word_index = self.vectorize_text()
            self.x_train, self.y_train, self.x_val, self.y_val = self.split_data()
            self.embedding_layer = self.create_embedding_matrix()
            self.model = self.train_model()
            self.save_model("model.json", "labels.json", "model.h5")
        else:
            self.model = self.load_model("model.json", "labels.json", "model.h5")

        self.predicted_categories = self.categorize_articles(articles_to_predict, labels_to_predict, titles_pred)

    def save_model(self, model_filename, labels_filename, weights_filename):
        # serialize model to JSON
        model_json = self.model.to_json()

        # open model
        with open(model_filename, "w") as json_file:
            json_file.write(model_json)

        # open dict of output labels
        with open(labels_filename, "w") as json_file:
            json.dump(self.labels_index, json_file)
        # serialize weights to HDF5
        self.model.save_weights(weights_filename)
        print("Saved model to disk")

    def load_model(self, model_filename, labels_filename, weights_filename):
        # load json and create model
        json_file = open(model_filename, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load labels dict
        with open(labels_filename, 'r') as file:
            self.labels_index = json.load(file)
        # load weights into new model
        loaded_model.load_weights(weights_filename)
        print("Loaded model from disk")

        return loaded_model

    def get_vectors(self):
        # first, build index mapping words in the embeddings set
        # to their embedding vector

        print('Indexing word vectors.')

        embeddings_index = {}
        with open("glove" + os.sep + "vectors.txt", 'r', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs

        print('Found %s word vectors.' % len(embeddings_index))
        return embeddings_index

    def vectorize_text(self):
        # vectorize the text samples into a 2D integer tensor
        tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
        tokenizer.fit_on_texts(self.articles)
        sequences = tokenizer.texts_to_sequences(self.articles)
        word_index = tokenizer.word_index

        print('Found %s unique tokens.' % len(word_index))

        data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
        self.labels = to_categorical(np.asarray(self.labels))

        print('Shape of data tensor:', data.shape)
        print('Shape of label tensor:', self.labels.shape)

        return data, word_index


    def split_data(self):
        # split the data into a training set and a validation set
        indices = np.arange(self.data.shape[0])
        np.random.shuffle(indices)
        self.data = self.data[indices]
        self.labels = self.labels[indices]
        num_validation_samples = int(VALIDATION_SPLIT * self.data.shape[0])

        x_train = self.data[:-num_validation_samples]
        y_train = self.labels[:-num_validation_samples]
        x_val = self.data[-num_validation_samples:]
        y_val = self.labels[-num_validation_samples:]

        return x_train, y_train, x_val, y_val

    def create_embedding_matrix(self):
        print('Preparing embedding matrix.')

        # prepare embedding matrix
        num_words = min(MAX_NUM_WORDS, len(self.word_index)) + 1
        embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
        for word, i in self.word_index.items():
            if i > MAX_NUM_WORDS:
                continue
            embedding_vector = self.embeddings_index.get(word)
            if embedding_vector is not None:
                # words not found in embedding index will be all-zeros.
                embedding_matrix[i] = embedding_vector

        # load pre-trained word embeddings into an Embedding layer
        # trainable = False so as to keep the embeddings fixed
        embedding_layer = Embedding(num_words,
                                    EMBEDDING_DIM,
                                    embeddings_initializer=Constant(embedding_matrix),
                                    input_length=MAX_SEQUENCE_LENGTH,
                                    trainable=False)

        return embedding_layer

    def train_model(self):
        print('Training model.')

        # train a 1D convnet with global maxpooling
        sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
        embedded_sequences = self.embedding_layer(sequence_input)
        x = Conv1D(128, 5, activation='relu')(embedded_sequences)
        x = MaxPooling1D(5)(x)
        x = Dropout(0.2)(x)
        x = Conv1D(128, 5, activation='relu')(x)
        x = MaxPooling1D(5)(x)
        x = Dropout(0.2)(x)
        x = Conv1D(128, 5, activation='relu')(x)
        x = GlobalMaxPooling1D()(x)
        x = Dropout(0.2)(x)
        x = Dense(128, activation='relu')(x)
        # x = Dropout(0.5)(x)
        preds = Dense(len(self.labels_index), activation='exponential')(x)

        model = Model(sequence_input, preds)
        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['acc'])

        model.fit(self.x_train, self.y_train,
                  batch_size=32,
                  epochs=11,
                  validation_data=(self.x_val, self.y_val))

        return model

    def prepare_articles_for_prediction(self, articles_predict):
        tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
        tokenizer.fit_on_texts(articles_predict)
        sequences = tokenizer.texts_to_sequences(articles_predict)
        data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

        return data

    def categorize_articles(self, articles, labels, titles):
        categories = []
        articles = [titles[i] + articles[i] for i in range(len(articles))]

        Xnew = self.prepare_articles_for_prediction(articles)
        ynew = self.model.predict(Xnew)

        for i in range(len(Xnew)):
            # get the index of a category which has maximum probability after prediction
            cat_index = np.where(ynew[i] == np.amax(ynew[i]))[0]
            # assign the index to dictionary of categories
            # print(ynew[i])
            predicted_category = list(self.labels_index.keys())[list(self.labels_index.values()).index(cat_index)]
            categories.append(predicted_category)
            # print("Title = %s" % predicted_category)
            # print(labels[i])
            # print(titles[i])

        return categories
