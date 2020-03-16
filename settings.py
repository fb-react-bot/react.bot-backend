#
HOST_URL = "http://35.221.251.166"
MODEL_PORT = "8000"
# global
TMP_DIR = '/wav_files'
redis = {}
sample_rate = 16000
frame_duration = 10 # ms
length_per_frame = int(sample_rate * frame_duration / 1000)
one_second = 10 #int(1000/frame_duration)

