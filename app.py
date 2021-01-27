import numpy as np
# Flask + Request für handling der anfragen, render_template für darstellung der templates, jsonify für webausgabe
from flask import Flask, request, render_template, jsonify
from gevent.pywsgi import WSGIServer

# TensorFlow + tf.keras
import tensorflow as tf

# Helfer
from helfer import base64_to_pil

# flask app
app = Flask(__name__)


model_pfad = "/Users/lbn/datax-projekt/web/model/model.h5"

# Model laden
model = tf.keras.models.load_model(model_pfad)
print('Model geladen. http://127.0.0.1:5000')


def model_predict(img, model):
    # Resize, Model erwartet 100x100 input
    img = img.resize((100, 100))

    # Preprocessing
    # Bild zu array
    x = tf.keras.preprocessing.image.img_to_array(img)
    # Normalisieren -> 0-255 zu 0-1
    x = np.true_divide(x, 255)
    # Model erwartet [none, 100, 100, 3] daher expand_dims um tensor mit "batch" dimension zu erzeugen
    x = tf.expand_dims(x, 0)

    # prediction machen
    vorhersage = model.predict(x)
    # ergebnis zurückgeben
    return vorhersage

# Route -> / = Homepage, Index | GET REQUEST
@app.route('/', methods=['GET'])
def index():
    # Startseite laden (template->index)
    return render_template('index.html')

# Route (POST | GET requests) -> Bild aus request laden + prediction machen
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Bild aus POST request -> base64 zu PIL image
        img = base64_to_pil(request.json)

        # Bild speichern lokal
        # img.save("./uploads/image.png")

        # Klassenliste
        klassen = ['Apfel', 'Banane', 'Birne', 'Drachenfrucht', 'Granatapfel', 'Guave', 'Honigmelone', 'Kaki', 'Kiwi',
                   'Mango', 'Orange', 'Pfirsich', 'Pflaume', 'Sternfrucht', 'Tomate']

        # Prediction machen
        prediction = model_predict(img, model)

        # Ergebnis ausgeben
        wahrscheinlichkeit = "{:.3f}".format(np.amax(prediction))    # größte Wahrscheinlichkeit (amax gibt maximum zurück)
        # Index von ergebnis holen
        index = np.argmax(prediction[0])
        # Klassenname anhand von index holen
        ergebnis = klassen[index]

        # In Konsole ausgeben
        print(ergebnis)
        print(wahrscheinlichkeit)

        # Klassenname und Wahrscheinlichkeit zurückgeben
        # JSONIFY (flask jsonify) -> Webausgabe
        return jsonify(result=ergebnis, probability=wahrscheinlichkeit)

    return None


# FLASK APP
if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
