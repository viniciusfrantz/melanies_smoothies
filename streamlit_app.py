# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!:cup_with_straw:")
# st.header("🥤 Customize your Smoothie! 🥤")
st.write(
  """##### Choose the Fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:', max_chars=30)
st.write('The name in your order will be:', name_on_order)
#     '''INSERT INTO smoothies.public.order(name_on_order)
# values'''(customer)''' ''')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
                                                                      
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe, 
    max_selections = 5
)

if ingredients_list: #same that if ingredient_list is not null
    ingredients_string = ''
    
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', ingredient, ' is ', search_on, '.')
      
        st.subheader(ingredient + 'Nutrition_Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values('""" + ingredients_string + """', '""" +name_on_order+ """') """
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon='✅')


