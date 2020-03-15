import numpy as np
import librosa

class MFCC_generator:
    def __init__(self):
        pass

    def get_wav_mfcc(self, wav_file_dir, start, duration):
        """
        Gets wav_file as input, return mfcc of speech between start & end
        ;param wav_file_dir: wav file of sound
        :param start: start time of speech(seconds)
        :param duration: duration time of speech(seconds)
        """
        self.wav_file_dir = wav_file_dir
        self.start = start
        self.duration = duration
        y, sr = librosa.core.load(path=self.wav_file_dir, offset=self.start, duration=self.duration)
        mfcc = librosa.feature.mfcc(y, sr)

        return mfcc