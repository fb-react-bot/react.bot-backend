import argparse
from MFCC_generator import MFCC_generator
import numpy as np

if __name__=="__main__":
    # get args
    parser = argparse.ArgumentParser(description="enter filename")
    parser.add_argument("--wavfile_directory", required=True)
    args = parser.parse_args()

    # get mfcc
    generator = MFCC_generator()
    arr = generator.get_wav_mfcc(args.wavfile_directory, start=0, duration=10)
    np.save("data/sample_mfcc.npy", arr)