import streamlit as st
from multiapp import MultiApp
from apps import heart_disease_app, diabetes_app, home # import your app modules here

app = MultiApp()


# Add all your application here
app.add_app("Home", home.main)
app.add_app("Heart", heart_disease_app.main)
app.add_app("Diabetes", diabetes_app.main)
# The main app
app.run()
