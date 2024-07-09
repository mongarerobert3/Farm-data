#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[14]:


df = pd.read_csv("monthly_milk_production.csv", index_col ="Date", parse_dates = True)
df.index.freq = "MS"
#index_col is used to initialize the Date as index


# In[25]:


df


# In[21]:


df.plot(figsize=(15, 6))


# In[22]:


from statsmodels.tsa.seasonal import seasonal_decompose


# In[30]:


results = seasonal_decompose(df["Production"])
results.plot();
#the trend shows the abstract of a seasonal pattern
#the seasonal pattern shows the graph without the trend
#semi-colon shows only one view of the result
#resid is the unwanted stuff


# In[31]:


#converting your dat to stationary data makes it easier for prediction


# In[32]:


len(df)


# In[35]:


train = df.iloc[:156]
test = df.iloc[156:]
#the reason for this is to separate the last 12 months from the train dataset


# In[40]:


df.head(), df.tail()


# In[41]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
#MinMaxScaler convers a dataset from 0-1


# In[52]:


scaler.fit(train)
scaled_test = scaler.transform(test)
scaled_train = scaler.transform(train)


# In[55]:


scaled_train


# In[77]:


from keras.preprocessing.sequence import TimeseriesGenerator


# ## mini demo of what a generator can do

# In[81]:


#what does n_features do
n_input = 3
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length = n_input, batch_size =1)


# In[82]:


#Use of the generator
#if numpy arays cannot be used you flatten it out
x, y = generator[0]
print(f"Given the array: \n{x.flatten()}")
print(f"predicts this y: \n {y.flatten()}")


# In[83]:


x.shape


# In[84]:


y.shape


# ## continue

# In[85]:


n_input = 12
generator = TimeseriesGenerator(scaled_train, scaled_train, length = n_input, batch_size = 1)


# In[98]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model


# In[95]:


#defining the model
model = Sequential()
model.add(LSTM(100, activation = "relu", input_shape =(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer = "adam", loss= "mse")


# In[96]:


model.summary()


# In[99]:


model.fit(generator, epochs = 50)


# In[100]:


loss_per_epoch = model.history.history["loss"]
plt.plot(range(len(loss_per_epoch)), loss_per_epoch)


# In[101]:


last_train_batch = scaled_train[-12:]


# In[102]:


last_train_batch.shape


# In[104]:


last_train_batch = last_train_batch.reshape(1, n_input, n_features)


# In[105]:


last_train_batch.shape


# In[106]:


model.predict(last_train_batch)


# In[110]:


scaled_test


# ## Observation
# ##### as we can observe, we tried to predict the the very first value of the test dataset from the scaled_trained. and we were damn close

# In[120]:


test_predictions = []

first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape(1, n_input, n_features)
#we simply took the last 12 inputs of the training dataset and reshaped it

for i in range(len(test)):
    
    #getting the prediction vaue for the first batch
    current_pred = model.predict(current_batch)[0]
    #the code above made a prediction on the reshaped training dataset
    test_predictions.append(current_pred)
    #the code above appended the predicted values to the above list,
    #in theory the appended values is supposed to look like the test dataset
    # now what this whole drama means is that we used the last 12 values to make a single prediction in 12 places
    current_batch = np.append(current_batch[:,1:,:], [[current_pred]], axis = 1)
    #the above code modifies the training dataset by adding a reset, 
    #A beautiful code ngl
    


# In[125]:


test_predictions


# In[128]:


test.head()


# In[123]:


#we need to tranform our data
true_prediction = scaler.inverse_transform(test_predictions)


# In[124]:


true_prediction


# In[139]:


test["Predictions"] = true_prediction


# In[145]:


Production = np.array(test["Production"])


# In[149]:


Production.flatten()


# In[150]:


true_prediction


# In[132]:


test.plot(figsize=(12, 6))


# In[147]:


#I made a mistake here
print("Test set score: {:.2f}".format(np.mean(true_prediction == Production)))


# In[151]:


from sklearn.metrics import mean_squared_error
from math import sqrt
rsme = sqrt(mean_squared_error(test["Production"], test["Predictions"]))
print(rsme)


# # How to minimize error
# 

# In[163]:


y_pred = list(true_prediction.flatten())


# In[164]:


y_test =list(Production)


# In[166]:


y_pred


# In[167]:


y_test


# In[173]:


for value in y_pred:
    i


# In[ ]:




