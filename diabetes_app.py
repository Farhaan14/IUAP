import numpy as np
import pandas as pd
import pickle
import streamlit as st


# Load ML model
model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('diabetes.csv')

dataset_X = dataset.iloc[:,[1, 2, 5, 7]].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
dataset_scaled = sc.fit_transform(dataset_X)


def predict(Glucose,Insulin,BMI,Age):

    values=[Glucose,Insulin,BMI,Age]
    
    features = [float(i) for i in values]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(sc.transform(array_features)) 
    output = prediction    
    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        st.text("The patient is not likely to have diabetes!")
    else:
        st.text("The patient is likely to have diabetes!")

def main():
    Glucose = st.number_input('Glucose')
    Insulin = st.number_input('Insulin')
    BMI = st.number_input('BMI')
    Age = st.number_input('Age')

    if st.button("Predict"):
        predict(Glucose,Insulin,BMI,Age)

if __name__ == '__main__':
#Run the application
    main()
