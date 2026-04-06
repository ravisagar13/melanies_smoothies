# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(f"Customiza Your Smoothie ! :cup_with_straw: ")
st.write(
  """Choose the Fruit you want in your custom Smoothie!
  """
)

# Create a selectbox
#option = st.selectbox(
 #   "What is your favorite fruit?", # Label for the selectbox
  #  ("Banana", "Strawberries", "Peaches")) # Options as a tuple (or list, numpy array, pandas DataFrame/Series)

# Display the selected option
#st.write("Your favorite fruit is:", option)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

   # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('submit Order')

    if time_to_insert:
     session.sql(my_insert_stmt).collect()
     st.success('Your Smoothie is ordered!', icon="✅")


smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
    
