import numpy as np
import pandas as pd
import pickle
import streamlit as st
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import numpy as np
import smtplib

current_email = ""

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
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,email TEXT)')
def create_userhealth():
	c.execute('CREATE TABLE IF NOT EXISTS usershealth(username TEXT,age integer,bmi real,glucose real,insulin real)')

def add_userdata(username,password,email):
	c.execute('INSERT INTO userstable(username,password,email) VALUES (?,?,?)',(username,password,email))
	conn.commit()
def add_userhealth_data(username,age,bmi,glucose,insulin):
	c.execute('INSERT INTO usershealth(username,age,bmi,glucose,insulin) VALUES (?,?,?,?,?)',(username,age,bmi,glucose,insulin))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def getEmail(username,password):
	c.execute('SELECT email FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users(user):
	c.execute('SELECT * FROM usershealth')
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
        st.text("The patient is likely to have diabetes! Mail sent.")
        sender = "iupacwecare@gmail.com"
        receiver = current_email
        password= "iupac@123"
        message = "The patient is likely to have diabetes!"
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver,message)


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

				data1 = getEmail(username,check_hashes(password,hashed_pswd))
				global current_email
				current_email = data1[0][0]

				task = st.selectbox("Task",["Check for Diabetes","Profiles"])
				if task == "Check for Diabetes":
					st.subheader("Check for Diabetes")
					glucose = st.number_input('Glucose')
					insulin = st.number_input('Insulin')
					bmi = st.number_input('BMI')
					age = st.number_input('Age')
					if st.button("Predict"):
						predict(glucose, insulin, bmi, age)
						create_userhealth()					
						add_userhealth_data(username,age,bmi,glucose,insulin)
						
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users(username)
					clean_db = pd.DataFrame(user_result,columns=["username","age","glucose","bmi","insulin"])
					select_user=clean_db.loc[clean_db["username"]==username]

					select_user2=select_user[["age","glucose","bmi","insulin"]]
					st.dataframe(select_user2)
					
					
					
					
					grp_slt = st.selectbox("Graphs",["Age vs BMI","Age vs Glucose","Age vs Insulin"])
					if grp_slt=="Age vs BMI":
						#st.line_chart(select_user2[["age","bmi"]])
						x=select_user[["age"]]
						y=select_user[["bmi"]]
						fig = plt.figure()
						ax = fig.add_subplot(1,1,1)
						ax.plot(x,y)
						ax.set_xlabel("Age")
						ax.set_ylabel("BMI")
						st.write(fig)
						
					elif grp_slt=="Age vs Glucose":
						#st.line_chart(select_user2[["age","glucose"]])
						x=select_user[["age"]]
						y=select_user[["glucose"]]
						fig = plt.figure()
						ax = fig.add_subplot(1,1,1)
						ax.plot(x,y)
						ax.set_xlabel("Age")
						ax.set_ylabel("Glucose")
						st.write(fig)
					else:
						#st.line_chart(select_user2[["age","insulin"]])
						x=select_user[["age"]]
						y=select_user[["insulin"]]
						fig = plt.figure()
						ax = fig.add_subplot(1,1,1)
						ax.plot(x,y)
						ax.set_xlabel("Age")
						ax.set_ylabel("Insulin")
						st.write(fig)
					
			else:
				st.warning("Incorrect Username/Password")
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_email = st.text_input("Email")
		new_password = st.text_input("Password",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password),new_email)
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")


if __name__ == '__main__':
    # Run the application
    main()
