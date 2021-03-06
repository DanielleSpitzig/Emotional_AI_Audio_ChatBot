# -*- coding: utf-8 -*-
"""Preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wn3MDIyCnEpvUaW1zwZmw8hzfAXoQU2r
"""

#Python file with funtion to transcribe audio files and extract features

# Commented out IPython magic to ensure Python compatibility.
# %pip install SpeechRecognition
import speech_recognition as sr
import librosa
from librosa import feature
import pandas as pd
from sklearn.model_selection import train_test_split

def Audio2Text(audio_file):
  """
  Given a wav audio file, return the text transcript
  Uses the SpeechRecognition library
  Input
  audio_file: .wav audio
  Output
  text: string of the transcript
  """
  #From sm import the Recognizer and get the audio file
  r=sr.Recognizer()
  wav = sr.AudioFile(audio_file)
  #Use the inputted audio file as the source
  with wav as source:
    audio = r.record(source)
  #Recognizer uses google to generate the transcript as a string
  try:
    text = r.recognize_google(audio)
  except Exception as e:
    text = None
  return text

def get_signal(fname):
  """
  Using librosa library, extract the signal from the audio file - will be used for analysis
  Input
  fname: path to the .wav file
  Outputs
  data: the np.ndarray of signals from the audio file
  s_rate: the sampling rate calculated from librosa
  """
  data, s_rate = librosa.load(fname)
  return data, s_rate

def get_feature(data, s_rate, mfcc=True, chroma=True, mel=True):
  """
  Given a np.ndarray of audio time series data, return up to three different features
  Mel frequency cepstral coefficients, pitch classes, or Mel spectrogram frequency
  Uses librosa library
  Inputs
  data: np.ndarray of signals from an audio file
  s_rate: sampling rate
  mfcc, chroma, mel: boolean to determine which features to calculate
  Output
  results: np.array of features - each 
  """
  results = np.array([])
  if mfcc:
    cof = np.mean(librosa.feature.mcff(y=data, sr=s_rate, n_mfcc=40).T, axis=0)
    results = np.hstack((results, cof))
  if chroma:
    cof = np.mean(librosa.feature.chroma_stft(S=np.abs(librosa.stft(data)), sr=s_rate).T, axis=0)
    results = np.hstack((results, cof))
  if mel:
    cof = np.mean(librosa.feature.melspectrogram(data, sr=s_rate).T, axis=0)
    results = np.hstack((results, cof))
  return results

def data_split(df, test_size = 0.2):
  """
  Take the given dataframe from labeling, and 
  """
  #Get data and responses from dataframe
  y = df['emo_class']
  X = df.drop(columns=['emo_class','labels'])

  #Get the text transcript of the audio files
  transcript = [Audio2Text(x) for x in X['path']]
  X['text'] = [transcript]
  #Get the signals and sampling rates - add to dataframe
  results = [get_signal(x) for x in X['path']]
  X[['signal', 'samp rate']] = [results[0], results[1]]

  #Assume want all features - get the results and add to dataframe
  results = [get_feature(x,y) for x,y in zip(X['signal'], X['samp rate'])]
  X[['MFCC', 'chroma', 'MSpec']] = [results[:, 0], results[:, 1], results[:, 2]]

  #run train-test split and return those values
  x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = 4444)

  return x_train, x_test, y_train, y_test