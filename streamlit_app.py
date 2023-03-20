import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import streamlit
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text(' Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free Range Egg')
streamlit.text('Avocado Toast')
streamlit.header('Build Your  Own Fruit Smoothie')

#import pandas
# We want pandas to read our CSV file from that S3 bucket so we use a pandas function called read_csv  to pull the data into a dataframe we'll call my_fruit_list. 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table with selected fruits.
streamlit.dataframe(fruits_to_show)

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

# new section to display Fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
  # accept user input
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    # import requests
    # using static url
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    
    # using url with appended components
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
    
    # using url with variable
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    
    # just writes the response code for e.g 200
    # streamlit.text(fruityvice_response)
    
    # just write the data to the screen
    # streamlit.text(fruityvice_response.json())
    
    # normalizes the json version of data
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    
    # prints normalised json data in tabular format
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
      
# don't run below this
streamlit.stop()

#import snowflake.connector
# connection 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

# cursor related to this connections
my_cur = my_cnx.cursor()

# associate cursor with query
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_row)

# Alow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
