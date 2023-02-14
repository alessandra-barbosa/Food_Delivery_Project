import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="Home",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state ="auto"

)

st.sidebar.markdown('# _:red[Cury Company]_')


st.sidebar.markdown('### :sunglasses:_:green[Dashboard]_')

#image_path=r'C:\Users\Utente77\repos/FTC_Curso/img/'
image=Image.open('shaian-ramesht-exSEmuA7R7k-unsplash_.jpg')    
st.sidebar.image(image)
st.sidebar.markdown('----------------------')
st.sidebar.markdown('#### Ask for help _@Alessandra_Barbosa_')
### ')

st.header('_:red[Cury Company] :green[Dashboard]_ ')
st.markdown('----------------------')

st.markdown ('### _:orange[Food Delivery Project]_ ')

st.caption('Cury Company is a marketplace that connects restaurants, delivery personnel, and consumers through its app.')
st.caption('In this project, I was responsible for designing metrics, analyzing data, creating a dashboard, and developing an algorithm to assist the CEO in accurately estimating delivery times.')

st.markdown('----------------------')

st.markdown("""
#### **How to use the dashboard?**:pencil:
####  _:green[- Company view]_
    - Managerial view: general behavioral metrics
    - tactical view: weekly growth indicators
    - geographic view: geolocation insights
#### _:green[- Delivery view ]_
    - Monitoring of weekly growth indicators
#### _:green[- Restaurant view]_
    - Weekly restaurant growth indicators

""")