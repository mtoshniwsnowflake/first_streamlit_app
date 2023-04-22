import streamlit
import pandas as pd
import requests
import snowflake.connector

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
#Let user choose the fruit option
fruit_choice = streamlit.text_input("What fruit would you like information about?",'Kiwi')
streamlit.write("User selected fruit "+fruit_choice)
fruity_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruity_response.json())
fruity_response_normalize = pd.json_normalize(fruity_response.json())
streamlit.dataframe(fruity_response_normalize)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

