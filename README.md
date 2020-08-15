# Emotional_AI_Audio_ChatBot
A ChatBot implemented using reinforcement learning. Trained off audio files with emotion labels, the ChatBot attempts to respond to the phrases in an emotionally sensitive manner.

There were two datasets used for this project, TESS and RAVDESS. Both can be found on Kaggle.
The labelled emotions were classified as "positive", "negative", or "neutral". Because of the ambiguity with the emotion "suprise" it was classified as neutral.

DQN and Tabular Q-Learning were implemented and their results were compared. This was due to the fact that the action-space is very discrete and well-define; hence, tabular methods should be able to outperform approximation methods.
