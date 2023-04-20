import streamlit
import pandas as pd
import request
streamlit.header(' 🥣 Breakfast Menu')
streamlit.text(' 🥗 Omega 3\'s & Blueberry Oatmeal')
streamlit.text(' 🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index("Fruit")
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
my_fruit_list = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(my_fruit_list)

streamlit.header("Fruityvice Fruit Advice!")

# Read data from FruityVice
fruity_response = request.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruity_response)
