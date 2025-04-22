from data import PreProcessor
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot

def predict(text):
    preproc = PreProcessor()
    text = preproc.forward(text)
    text = one_hot(text, 10000)
    print(text)
    embedded_docs = pad_sequences([text], padding='pre', maxlen = 20)
    print(embedded_docs)

    classifier = tf.keras.models.load_model('LSTMModel')
    pred = classifier.predict(embedded_docs)
    print(pred)

    return tf.math.argmax(pred[0])

if __name__ == '__main__':
    text = input()
    prediction = predict(text)
    print(prediction)