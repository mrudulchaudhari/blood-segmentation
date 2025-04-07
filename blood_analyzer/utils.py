# Adhishree Shiledar
import numpy as np
import pandas as pd
import pickle
import os
import json
import hashlib
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Constants
# Constants
MODEL_PATH = 'static/models/'
CACHE_PATH = 'static/cache/'
RF_MODEL_FILE = os.path.join(MODEL_PATH, 'random_forest_model.pkl')
GB_MODEL_FILE = os.path.join(MODEL_PATH, 'gradient_boosting_model.pkl')
SVM_MODEL_FILE = os.path.join(MODEL_PATH, 'svm_model.pkl')
NN_MODEL_FILE = os.path.join(MODEL_PATH, 'neural_network_model.h5')
SCALER_FILE = os.path.join(MODEL_PATH, 'scaler.pkl')
BEST_MODEL_FILE = os.path.join(MODEL_PATH, 'best_model.pkl')
BEST_MODEL_NAME_FILE = os.path.join(MODEL_PATH, 'best_model_name.txt')
PREDICTION_CACHE_FILE = os.path.join(CACHE_PATH, 'prediction_cache.json')
MODEL_METADATA_FILE = os.path.join(MODEL_PATH, 'model_metadata.json')