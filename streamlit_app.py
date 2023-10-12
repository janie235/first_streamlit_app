import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the all fruits table on the page.
streamlit.dataframe(fruits_to_show)

##New section to display fruityvice api response
#streamlit.header("Fruityvice Fruit Advice!")
## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
##import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
## writes data from Fruityvice API on the screen in the original format
# streamlit.text(fruityvice_response.json())
## creates the normalized table from the API repsonse
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
## display the normalized table on the page
#streamlit.dataframe(fruityvice_normalized)

#New section to display fruityvice api response for taking in customers choices
#Introducing this structure allows us to separate the code that is loaded once from the code that should be repeated each time a new value is entered.
#Notice there are three lines of code under the ELSE. These are important steps we will be repeating. We can pull them out into a separate bit of code called a function. We'll do that next. 

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error(""Please select a fruit to get information."")
  else
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)    
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

streamlit.write('The user entered ', fruit_choice)

#stop snowflake because there's sme problem adding rows into DB from the app
streamlit.stop()

# adding SF connector
#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)

# change the data format to make it look better
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)

# GET ALL ROWS, NOT JUST ONE
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the user to add his selected fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding  jackfruit')

# this will be adding rows into SF table after inserts them in the app
my_cur.execute("insert into fruit_load_list values ('from streamlit')")


