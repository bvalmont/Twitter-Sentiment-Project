from sklearn.metrics import confusion_matrix, precision_score
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.regularizers import l2
import pandas as pd
import numpy as np

file = "movie_reviews.csv"

df = pd.read_csv(file)
print(df.head())
print(df.columns)

x = df.drop(columns=['label', 'text'])
y = df['label']

df['neg'] = df['neg'].astype(float)
df['pos'] = df['pos'].astype(float)
df['neu'] = df['neu'].astype(float)
df['compound'] = df['compound'].astype(float)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, random_state=0)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
print(x_train)

model = Sequential()

model.add(Dense(100, activation='relu', input_dim=4, kernel_regularizer=l2(0.01)))
model.add(Dropout(0.1, seed=None))

model.add(Dense(50, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.1, seed=None))

model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Train the model
model_output = model.fit(x_train, y_train, epochs=20, batch_size=1, verbose=1, validation_data=(x_test, y_test),)
print('Training Accuracy : ', np.mean(model_output.history['accuracy']))
print('Validation Accuracy : ', np.mean(model_output.history['val_accuracy']))


y_pred = model.predict(x_test)
rounded = [round(x[0]) for x in y_pred]
y_pred1 = np.array(rounded, dtype='int64')

confusion_matrix(y_test,y_pred1)

precision_score(y_test, y_pred1)

model.save("sentiment_classifier.h5")  