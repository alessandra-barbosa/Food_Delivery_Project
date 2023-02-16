###############################
#imports
###############################

import pandas                 as pd
import numpy                  as np
import plotly.express         as px
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Home",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state ="auto"

)
#################################
#Auxiliary functions
#################################

def clear_data(df):# ID - Remove spaces in strings
    """ 
            Clean dataset with:
            1. remove NA's
            2.change column type
            3.remove spaces
            4.format columns
            5.clean time variables
            6. change capital letters column names
            
        Input: Dataframe
        Ouput: Dataframe
    """
    
    df.loc[:,'ID']=df.loc[:,'ID'].str.strip()

    # Delivery_person_Age - Transform in int
    df = df.loc[df['Delivery_person_Age'] != 'NaN ']
    df['Delivery_person_Age']=df['Delivery_person_Age'].astype(int)  

    # Delivery_person_Ratings Transform in float
    df['Delivery_person_Ratings']=df['Delivery_person_Ratings'].astype(float)

    # Order_Date  - transform in date                  
    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

    # Time_Orderd  - transform in date 
    df = df.loc[df['Time_Orderd'] != 'NaN ']
    df['Time_Orderd'] = pd.to_datetime( df['Time_Orderd'], format='%H:%M:%S'  )

    # Time_Order_picked  - transform in date                  
    df = df.loc[df['Time_Order_picked'] != 'NaN ']
    df['Time_Order_picked'] = pd.to_datetime( df['Time_Order_picked'], format='%H:%M:%S' )

    # Delivery_person_ID - Remove spaces in strings
    df['Delivery_person_ID']=df['Delivery_person_ID'].apply(lambda x: str.strip(x))

    # Road_traffic_density - Remove spaces in strings
    df.loc[:,'Road_traffic_density']=df.loc[:,'Road_traffic_density'].str.strip()

    # Type_of_order - Remove spaces in strings
    df.loc[:,'Type_of_order']=df.loc[:,'Type_of_order'].str.strip()

    # Type_of_vehicle - Remove spaces in strings
    df.loc[:,'Type_of_vehicle']=df.loc[:,'Type_of_vehicle'].str.strip()

    # Festival - Remove spaces in strings
    df = df.loc[df['Festival'] != 'NaN ']
    df.loc[:,'Festival']=df.loc[:,'Festival'].str.strip()

    # Vehicle_condition Transform in float
    df['Vehicle_condition']=df['Vehicle_condition'].astype(int)

    # Vehicle_condition Transform in float
    aux = df['multiple_deliveries'] != 'NaN '
    df = df.loc[aux, :]
    df['multiple_deliveries']=df['multiple_deliveries'].astype(int)

    # City - Remove spaces in strings
    df = df.loc[df['City'] != 'NaN ']
    df.loc[:,'City']=df.loc[:,'City'].str.strip()

    # Time_taken - remove min
    df['Time_taken(min)']= df['Time_taken(min)'].apply(lambda x:x.split(' ')[1])
    df['Time_taken(min)']=df['Time_taken(min)'].astype(int)

    # Change columns name
    df.columns = map(str.lower, df.columns)
    return df

#############
# load
#############

#df=pd.read_csv(r'C:\Users\Utente77\repos\FTC_Curso\dataset\train.csv')
df=pd.read_csv('train.csv')

df=clear_data(df)      

#=========================================================
# Side Bar
#==========================================================


st.sidebar.markdown('## :orange[ Select the city type:]')

cityselection=st.sidebar.multiselect ("Which city type?",
                                        ['Metropolitian','Urban','Semi-Urban'], ['Metropolitian','Urban','Semi-Urban'])
              
df=df.loc[df['city'].isin( cityselection),:]  

st.sidebar.markdown('## :orange[ Select the order type:]')

cityselection=st.sidebar.multiselect ("Which order type?",
                                       ['Snack', 'Drinks', 'Buffet', 'Meal'], ['Snack', 'Drinks', 'Buffet', 'Meal'])
              
df=df.loc[df['type_of_order'].isin( cityselection),:]  



#=================================
#Layout
#=================================
image1=Image.open('banner.png')    
st.image(image1,width=800, use_column_width=None)

tab1, tab2, tab3 = st.tabs(["Home","How to use", "Ask for help"])

with tab1:
    with st.container():
        # order metric
        cols1,cols2,cols3,cols4=st.columns(4, gap='small')

        with cols1:
            aux=len(df)
            cols1.metric( 'Orders',aux )
            
        with cols2:
            aux=len(df['restaurant_latitude'].unique())
            cols2.metric( 'Restaurant',aux )
            
        with cols3:
            aux=len(df['delivery_person_id'].unique())
            cols3.metric( 'Delivery person',aux )
            
        with cols4:
            aux=np.round(df['delivery_person_ratings'].mean(),2)
            cols4.metric( 'Delivery Ratings',aux )
   
        st.markdown('----------------------')       
        

with tab2:
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
            
    with tab3:
        st.markdown('#### Ask for help _@Alessandra_Barbosa_')
