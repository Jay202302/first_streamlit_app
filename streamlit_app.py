import streamlit
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text(' Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free Range Egg')
streamlit.text('Avocado Toast')
streamlit.header('Build Your  Own Fruit Smoothie')

import pandas
# We want pandas to read our CSV file from that S3 bucket so we use a pandas function called read_csv  to pull the data into a dataframe we'll call my_fruit_list. 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc(fruits_selected)

# Display the table with selected fruits.
streamlit.dataframe(my_fruit_list)

# Display the table on the page.
streamlit.dataframe(my_fruit_list)
