from aiohttp import web 
import socketio 
import io
import scipy.io.wavfile as wavf
import numpy as np
import struct
import requests
import json
import time 
from settings import * 

sio = socketio.AsyncServer() 
app = web.Application() 
# bind socket io to webapp 
sio.attach(app)

# global - fake memdb
redis = {}  

def append_and_save_wav_data(filename, data):
    prev_wav = wavf.read(filename, mmap=False)
    prev_data = list(prev_wav[1])
    prev_data.extend(list(data))
    wavf.write(filename, sample_rate, np.array(prev_data, dtype=np.int16))
               
@sio.on("fromClient")
async def from_client(sid, data): 
    print("Connection Successful... from client: ", data)


@sio.on("mic_on")
async def start_message(sid, data): 
    print(sid)
    if data == 1: 
        redis[sid] = {} 
        redis[sid]['result'] = []
    else:
        if len(redis[sid]['result']) > 0:
            t1 = time.time()
            headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
            result = requests.post("http://35.221.251.166:8000/predict",\
                data=json.dumps({'data':redis[sid]['result']}), headers=headers)
            dt = time.time() - t1
            print("Sentiment Analysis time: %0.02f seconds" % (dt))
            if result:
                print(result.text)
                redis['nonspeech_num'] = 0
                await sio.emit('fromSerer', result.text)
        redis.pop(sid)

# 0: angry, 1, happy, 2 neutral, 3 sad 
@sio.on('mic')
async def print_message(sid, *data):
    redis[sid]['result'].extend(list(data))

if __name__ == '__main__':
    web.run_app(app, port = 8080)
