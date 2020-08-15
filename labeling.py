# -*- coding: utf-8 -*-
"""Labeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GzbD6d27RDbym0n7jJ3BdqyP_O0ufVdB
"""

#import the necessary libraries
import pandas as pd
import os

#For these datasets, the emotions will be classified as 0, 1, 2 for postive, neutral and negative emotions respectively
#Let's write a function to do this
def label_emo (row):
  if row['labels'] == "happy":
    return 0
  elif row['labels'] == "neutral":
    return 1
  elif row['labels'] == "surprise" :
    return 1
  else:
    return 2

#Due to the strong accents in the SAVEE dataset, the SpeechRecognizer couldn't determine the correct audio2text
def SAVEE_data(SAVEE="SAVEE"):
  """
  Labeling for the SAVEE dataset
  Input: SAVEE: the path of the directory list of the files for the SAVEE dataset
  Output: label_df: dataframe with the emotions, gender, source, and path to .wav file
  """
  #Get the directory of the SAVEE dataset
  data = os.listdir(SAVEE)
  #Get labels for the emotions and gender based off of the labels
  #Note: SAVEE is a only male dataset
  emotion=[]
  emo_class=[]
  path=[]
  for i in data:
    if i[-8:-6]=='_a':
      emotion.append('angry')
      emo_class.append(2)
    elif i[-8:-6]=='_d':
      emotion.append('disgust')
      emo_class.append(2)
    elif i[-8:-6]=='_f':
      emotion.append('fear')
      emo_class.append(2)
    elif i[-8:-6]=='_h':
      emotion.append('happy')
      emo_class.append(0)
    elif i[-8:-6]=='_n':
      emotion.append('neutral')
      emo_class.append(1)
    elif i[-8:-6]=='sa':
      emotion.append('sad')
      emo_class.append(2)
    elif i[-8:-6]=='su':
      emotion.append('surprise')
      emo_class.append(1)
    else:
      emotion.append('unknown')
    #SAVEE path is amended based on the file in the folder
    path.append(SAVEE + '/' + i)
  
  #Create the database
  label_df = pd.DataFrame(emotion, columns=['labels'])
  df['emo_class'] = label_df.apply (lambda row: label_emo(row), axis=1)
  label_df['gender'] = 'male'
  label_df['source'] = 'SAVEE'
  label_df = pd.concat([label_df, pd.DataFrame(path, columns=['path'])], axis='1')
  return label_df

def RAV_data(RAV='RAVDESS'):
  """
  Labeling for the RAVDESS dataset
  Input: RAV: the path of the directory list of the files for the RAVDESS dataset
  Output: label_df: dataframe with the emotions, gender, source, and path to .wav file
  """
  #Get the directory of the RAVDESS dataset and sort - to ensure speakers in correct order
  data = os.listdir(RAV)
  data.sort()
  #Get labels for the emotions and gender based off of the labels
  emotion=[]
  gender=[]
  path=[]
  for i in data:
    fname = (RAV + '/' + i)
    part = i.split('.')[0].split('-')
    emotion.append(int(part[2]))
    temp = int(part[6])
    if temp%2 == 0:
      temp = 'female'
    else:
      temp = 'male'
    gender.append(temp)
    path.append(fname)
  
  #Create the database
  label_df = pd.DataFrame(emotion)
  #2 is calm but for the purpose of this assignment it will be classified as neutral
  label_df = label_df.replace({1:'neutral', 2:'neutral', 3:'happy', 4:'sad', 5:'angry', 6:'fear', 7:'disgust', 8:'surprise'})
  label_df = pd.concat([pd.DataFrame(gender), label_df], axis=1)
  label_df.columns = ['gender', 'labels']
  label_df['source'] = 'RAVDESS'
  label_df = pd.concat([label_df, pd.DataFrame(path, columns=['path'])], axis=1)
  label_df['emo_class'] = label_df.apply (label_emo, axis=1)
  return label_df

def TESS_data(TESS='TESS'):
  """
  Labeling for the TESS dataset
  Input: TESS: the path of the directory list of the files for the TESS dataset
  Output: label_df: dataframe with the emotions, gender, source, and path to .wav file
  """
  #Get the directory of the TESS dataset and sort it alphabetically (just to be sure)
  data = os.listdir(TESS)
  #Get labels for the emotions and gender based off of the labels
  #Note TESS has just female speakers
  emotion=[]
  path=[]
  for i in data:
    fname = (TESS + '/' + i)
    part = i.split('.')[0].split('_')
    if part[2] == 'ps':
      emotion.append('surprise')
    else:
      emotion.append(part[2])
    path.append(fname)
  
  #Create the database
  label_df = pd.DataFrame(emotion, columns=['labels'])
  label_df['gender'] = 'female'
  label_df['source'] = 'TESS'
  label_df = pd.concat([label_df, pd.DataFrame(path, columns=['path'])], axis=1)
  label_df['emo_class'] = label_df.apply(label_emo, axis=1)
  return label_df

def CD_data(CD='CREMA-D'):
  """
  Labeling for the CREMA-D dataset
  Input: CD: the path of the directory list of the files for the CREMA-D dataset
  Output: label_df: dataframe with the emotions, gender, source, and path to .wav file
  """
  #Get the directory of the CREMA-D dataset and sort it alphabetically (just to be sure)
  data = os.listdir(CD)
  #Get labels for the emotions and gender based off of the labels
  emotion=[]
  gender=[]
  path=[]
  fmale = [1002,1003,1004,1006,1007,1008,1009,1010,1012,1013,1018,1020,1021,1024,
           1025,1028,1029,1030,1037,1043,1046,1047,1049,1052,1053,1054,1055,1056,
           1058,1060,1061,1063,1072,1073,1074,1075,1076,1078,1079,1082,1084,1089,1091]
  for i in data:
    fname = (CD + '/' + i)
    part = i.split('.')[0].split('_')
    if int(part[0]) in fmale:
      temp = 'female'
    else:
      temp = 'male'
    gender.append(temp)
    if part[2] == 'SAD':
        emotion.append('sad')
    elif part[2] == 'ANG':
        emotion.append('angry')
    elif part[2] == 'DIS':
        emotion.append('disgust')
    elif part[2] == 'FEA':
        emotion.append('fear')
    elif part[2] == 'HAP':
        emotion.append('happy')
    elif part[2] == 'NEU':
        emotion.append('neutral')
    path.append(CD + '/' + i)
    
  
  #Create the database
  label_df = pd.DataFrame(emotion, gender, columns=['labels', 'gender'])
  label_df['source'] = 'CREMA-D'
  label_df = pd.concat([label_df, pd.DataFrame(path, columns=['path'])], axis=1)
  label_df['emo_class'] = label_df.apply(label_emo, axis=1)
  return label_df