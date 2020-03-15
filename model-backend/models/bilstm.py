import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from models.utils.feature_extractor_utils import *


state_dict_directory = "/models/data/bilstm_augmented_state_dict.pt"

class BiLSTM(nn.Module):
    def __init__(
        self,
        input_dim=30,
        hidden_dim=60,
        dense_dim=512,
        output_dim=4,
        num_layers=2,
        use_gpu=False,
        batch_size=1,
        is_training=False,
        dropout=0.2
    ):
        """
        Args:
            ;input_dim: 30
            ;hidden_dim: 60
            ;dense_dim: 512
            ;output_dim: 4
            ;num_layers: 2 #stack two bilstm layers
        """
        super(BiLSTM, self).__init__()
        # inti self values
        self.use_gpu = use_gpu
        self.batch_size = batch_size
        self.dropout = dropout
        self.num_layers = num_layers
        self.is_training = True

        # define layers
        self.bilstm = nn.LSTM(
            input_size=input_dim,
            num_layers=num_layers,
            hidden_size=hidden_dim,
            bidirectional=True,
        )
        self.dense_hidden = nn.Sequential(nn.Linear(hidden_dim*2, dense_dim),
                                         nn.ReLU(inplace=True))
        self.dense_out = nn.Linear(dense_dim, output_dim)


    def forward(self, audio_features):
        # audio_features = (seq_len, batch, input_size)
        lstm_output, (h_1, c_1) = self.bilstm(audio_features)

        # (seq_len, batch, input_size)  => (batch, input_size), only last output
        hidden_1 = self.dense_hidden(lstm_output[-1])
        y = self.dense_out(hidden_1)

        # for cross entropy loss
        if self.is_training:
            return y
        else:
            return F.softmax(y)


    def forward(self, audio_features):
        # audio_features = (seq_len, batch, input_size)
        lstm_output, (h_1, c_1) = self.bilstm(audio_features)

        # (seq_len, batch, input_size)  => (batch, input_size), only last output
        hidden_1 = self.dense_hidden(lstm_output[-1])
        y = self.dense_out(hidden_1)

        # for cross entropy loss
        if self.is_training:
            return y
        else:
            return F.softmax(y)

def predict(wav_file:str, use_gpu:bool=False):
    # load model
    bilstm = BiLSTM()
    bilstm.load_state_dict(torch.load(state_dict_directory, map_location='cpu'))
    # check gpu
    if use_gpu:
        bilstm.cuda()
        device = torch.device("cuda")
    else:
        device = None
    extracted_feature = feature_generator(wav_file)
    extracted_feature = np.expand_dims(extracted_feature, 0) # batch_dim
    
    # convert features array to tensor
    if use_gpu:
        feature_tensor = torch.tensor(extracted_feature).float().permute(2,0,1).to(device)
    else:
        feature_tensor = torch.tensor(extracted_feature).float().permute(2,0,1)
        
    # predict
    ###predicted_label = bilstm(feature_tensor).argmax(dim=1).cpu().numpy()[0]
    predicted_label = bilstm(feature_tensor).argmax(dim=1).item()
    return predicted_label