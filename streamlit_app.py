import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError 

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

## create function to get fruityvice data
def get_fruityvice_data(fruit):
   fruity_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
   #streamlit.text(fruity_response.json())
   fruity_response_normalize = pd.json_normalize(fruity_response.json())
   return fruity_response_normalize

# Read data from FruityVice
#Let user choose the fruit option
fruit_choice = streamlit.text_input("What fruit would you like information about?",'Kiwi')
streamlit.write("User selected fruit "+fruit_choice)
try:
  if not fruit_choice:
    streamlit.error("Please select fruit to get information")
  else:
    fruity_response_normalize = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruity_response_normalize)
except URLError as e:
  streamlit.error

def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
      my_data = my_cur.fetchall()
   return my_data

## add a button to load fruit list
if streamlit.button("load fruit data"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_fruit_data = get_fruit_load_list()
   streamlit.header("The Fruit Load list contains:")
   streamlit.dataframe(my_fruit_data)
   
## allow individual to add fruit to the list
def add_fruit_row_snowflake(fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES("+fruit+")")
      return "Thanks for adding fruit: "+fruit
      
# Let's put a pick list here so they can pick the fruit they want to include 
## add a button to add fruit
fruit_sel = streamlit.text_input("What fruit would you like to Add")
if streamlit.button("Add a fruit to the list"):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = add_fruit_row_snowflake(fruit_sel)
   streamlit.write(back_from_function)
