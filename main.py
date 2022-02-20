import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *


import mne
from mne.channels import read_layout

# use synthetic board for demo
params = BrainFlowInputParams()

real_board = True
if real_board:
    params.serial_port = 'COM3'
    board_id = BoardIds.CYTON_BOARD.value
else:
    board_id = BoardIds.SYNTHETIC_BOARD.value

# Start Stream
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream()
time.sleep(10)
data = board.get_board_data()
board.stop_stream()
board.release_session()

eeg_channels = BoardShim.get_eeg_channels(board_id)
eeg_data = data[eeg_channels, :]

time.sleep(5)  # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
data = board.get_board_data()
board.stop_stream()
board.release_session()

eeg_channels = BoardShim.get_eeg_channels(board_id)
bands = DataFilter.get_avg_band_powers(data, eeg_channels, 128, True)
feature_vector = np.concatenate((bands[0], bands[1]))
print(feature_vector)

# calc concentration
concentration_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.KNN.value)
concentration = MLModel(concentration_params)
concentration.prepare()
print('Concentration: %f' % concentration.predict(feature_vector))
concentration.release()

# calc relaxation
relaxation_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value, BrainFlowClassifiers.REGRESSION.value)
relaxation = MLModel(relaxation_params)
relaxation.prepare()
print('Relaxation: %f' % relaxation.predict(feature_vector))
relaxation.release()

