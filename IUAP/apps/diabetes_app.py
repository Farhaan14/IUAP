import numpy as np
import pandas as pd
import pickle
import streamlit as st

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('didata.db',check_same_thread=False)
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


# Load ML model
model = pickle.load(open('model_2.pkl', 'rb'))

dataset = pd.read_csv('diabetes.csv')

dataset_X = dataset.iloc[:, [1, 2, 5, 7]].values

from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range=(0, 1))
dataset_scaled = sc.fit_transform(dataset_X)


def predict(Glucose, Insulin, BMI, Age):
    values = [Glucose, Insulin, BMI, Age]

    features = [float(i) for i in values]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(sc.transform(array_features))
    output = prediction
    # Check the output values and retrive the result with html tag based on the value
    if output == 0:
        st.text("The patient is not likely to have diabetes!")
    else:
        st.text("The patient is likely to have diabetes!")


def main():
	menu = ["Diabetes","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Diabetes":
		st.subheader("Please login or signup to continue")
		
		
	elif choice == "Login":
		st.subheader("Login Section")
		username="";
		password="";
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Check for Diabetes","Analytics","Profiles"])
				if task == "Check for Diabetes":
					st.subheader("Check for Diabetes")
					Glucose = st.number_input('Glucose')
					Insulin = st.number_input('Insulin')
					BMI = st.number_input('BMI')
					Age = st.number_input('Age')
					if st.button("Predict"):
						predict(Glucose, Insulin, BMI, Age)
						
				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")


if __name__ == '__main__':
    # Run the application
    main()
