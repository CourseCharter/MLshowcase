# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')

#cleaning the data
data.replace('?', np.nan, inplace= True)
data.replace({'male': 1, 'female': 0}, inplace=True)
data = data.astype({"age": np.float64, "fare": np.float64})

#combining siblings and parents into relatives
data['relatives'] = data.apply (lambda row: int((row['sibsp'] + row['parch']) > 0), axis=1)

#see relations on various charts
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import path

fig, axs = plt.subplots(ncols=5, figsize=(30,5))
sns.violinplot(x="survived", y="age", hue="sex", data=data, ax=axs[0])
sns.pointplot(x="sibsp", y="survived", hue="sex", data=data, ax=axs[1])
sns.pointplot(x="parch", y="survived", hue="sex", data=data, ax=axs[2])
sns.pointplot(x="pclass", y="survived", hue="sex", data=data, ax=axs[3])
sns.violinplot(x="survived", y="fare", hue="sex", data=data, ax=axs[4])

parent = path.parent
fig.savefig(parent + 'static/titanic/titanic_test_model.png')

#look at each features' correlation to survival
corr_table = data.corr().abs()[["survived"]]

#drop insignifant
data = data[['sex', 'pclass','age','relatives','fare','survived']].dropna()

#split the train and test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data[['sex','pclass','age','relatives','fare']], data.survived, test_size=0.2, random_state=0)

#normalizing
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

#classifying
import keras
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()

model.add(Dense(5, kernel_initializer = 'uniform', activation = 'relu', input_dim = 5))
model.add(Dense(5, kernel_initializer = 'uniform', activation = 'relu'))
model.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid'))

nn_summary = model.summary()

#complining
model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=32, epochs=50)

#evaluate
from sklearn import metrics
y_pred = model.predict_classes(X_test)
nn_results = metrics.accuracy_score(y_test, y_pred)



