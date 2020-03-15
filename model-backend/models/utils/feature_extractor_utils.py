import numpy as np
import librosa

def load_wav(wav_file_dir, sampling_rate):
    """
    sampling_rate=None일 경우, 해당 음성파일의 sr 그대로 사용
    """
    y, sr = librosa.core.load(path=wav_file_dir, sr=sampling_rate) #sr=16000
    return y, sr

def get_wav_mfcc(y, sr, n_fft_rate, hop_length_rate):
    # extract mfcc
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    mfcc = librosa.feature.mfcc(y, sr, n_mfcc=13, n_fft=n_fft, hop_length=hop_length)
    return mfcc

def get_wav_chroma(y, sr, n_fft_rate, hop_length_rate):
    # extract chroma
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    chroma = librosa.feature.chroma_stft(y, sr, n_fft=n_fft, hop_length=hop_length)
    return chroma

def get_spectral_centroid(y, sr, n_fft_rate, hop_length_rate):
    # extract spectral_centroid
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    spectral_centroid = librosa.feature.spectral_centroid(y, sr, n_fft=n_fft, hop_length=hop_length)
    return spectral_centroid

def get_spectral_rolloff(y, sr, n_fft_rate, hop_length_rate):
    # extract spectral_rolloff
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    spectral_rolloff = librosa.feature.spectral_rolloff(y, sr, n_fft=n_fft, hop_length=hop_length)
    return spectral_rolloff

def get_spectral_flux(y, sr, n_fft_rate, hop_length_rate):
    # extract spectral_flux
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    spectral_flux = librosa.onset.onset_strength(y, sr, n_fft=n_fft, hop_length=hop_length)
    spectral_flux = np.expand_dims(spectral_flux, 0)
    return spectral_flux

# returns complex number. not in use
def get_spectrum(y, sr, n_fft_rate, hop_length_rate):
    # extract spectrum
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    spectrum = librosa.core.stft(y, n_fft=n_fft, hop_length=hop_length)
    return spectrum

def get_spectral_entropy(mfcc):
    P_w = mfccs**2 / mfccs.shape[0]
    p_i = (P_w/P_w.sum(axis=0))
    entropy = -(p_i * np.log(p_i)).sum(axis=0)
    return entropy

def get_spectral_bandwidth(y, sr, n_fft_rate, hop_length_rate):
    # extract spectral_bandwidth
    n_fft = int(sr * n_fft_rate)
    hop_length = int(sr * hop_length_rate)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y, sr, n_fft=n_fft, hop_length=hop_length)
    return spectral_bandwidth

def feature_generator(wav_file_dir, sampling_rate=16000, n_fft_rate=0.2, hop_length_rate=0.1, max_length=78):
    # load
    y, sr = load_wav(wav_file_dir, sampling_rate)
    
    # get features
    mfccs = get_wav_mfcc(y, sr, n_fft_rate, hop_length_rate)
    chromas = get_wav_chroma(y, sr, n_fft_rate, hop_length_rate)
    chroma_stds = np.expand_dims(np.std(chromas, axis=0), 0)
    spectral_centroids = get_spectral_centroid(y, sr, n_fft_rate, hop_length_rate)
    spectral_rolloffs = get_spectral_rolloff(y, sr, n_fft_rate, hop_length_rate)
    spectral_fluxs = get_spectral_flux(y, sr, n_fft_rate, hop_length_rate)
    spectral_bandwidths = get_spectral_bandwidth(y, sr, n_fft_rate, hop_length_rate)
    
    # concat features
    list_to_concat = [mfccs, chromas, chroma_stds, spectral_centroids, spectral_rolloffs, 
                     spectral_fluxs, spectral_bandwidths]
    concatted_feature = np.concatenate(list_to_concat)
    
    # padding of drop
    difference = max_length-concatted_feature.shape[1]
    if difference <= 0:
        final_feature = concatted_feature[:, :max_length]
    else:
        pad_array = np.zeros([concatted_feature.shape[0], difference])
        final_feature = np.concatenate([concatted_feature, pad_array], axis=1)
    
    return final_feature