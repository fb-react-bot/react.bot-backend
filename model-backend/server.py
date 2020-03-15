# import libraries
from flask import Flask, request, jsonify
import logging
import random
import time
from models import bilstm
import scipy.io.wavfile as wavf
import numpy as np 

# import settings
from settings import * # import
# set flask params
app = Flask(__name__)

@app.route("/")
def hello():
    return "Classification example\n"

@app.route('/predict', methods=['POST'])
def predict():
    
    content = request.get_json()
    t = time.time() # get execution time
    vad_data = content['data'] # fix 
    print(len(vad_data))
    tmp_wav_filename = "test.wav"
    wavf.write(tmp_wav_filename, SAMPLE_RATE, np.array(vad_data, dtype=np.int16))
    label = bilstm.predict(tmp_wav_filename)
    dt = time.time() - t
    # #app.logger.info
    print("Execution time: %0.02f seconds" % (dt))
    print("%s classified as %s" % (len(content['data']), label))
    return jsonify(label)

if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=True, port=PORT)