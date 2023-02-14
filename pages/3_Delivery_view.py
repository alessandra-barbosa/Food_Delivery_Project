#imports
import pandas                 as pd
import numpy                  as np
import plotly.express         as px
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title="Company View", page_icon=":)", layout="wide")

########################
#auxiliary functions
#########################
def slowest(df):
            df_aux=((df[['delivery_person_id','city','min_per_Km']]
            .groupby(['city','delivery_person_id']).mean().
             sort_values(['city','min_per_Km'],axis=0, ascending=False).reset_index()))

            df_aux1=df_aux.loc[df_aux['city']=='Metropolitian',:].head(10)
            df_aux2=df_aux.loc[df_aux['city']=='Urban',:].head(10)
            df_aux3=df_aux.loc[df_aux['city']=='Semi-Urban',:].head(10)
            df_lower=pd.concat([df_aux1, df_aux2, df_aux3],axis=0).sort_values(['min_per_Km'],axis=0, ascending=True).reset_index(drop=True)
            df_lower=df_lower.head(10)
            return df_lower
        
def distance(df):
   df['distance']=(df[['restaurant_latitude','restaurant_longitude','delivery_location_latitude','delivery_location_longitude']].
                    apply(lambda x: haversine((x['restaurant_latitude'],x['restaurant_longitude']),              (x['delivery_location_latitude'],x['delivery_location_longitude'])), axis=1))
   df['min_per_Km']=df['time_taken(min)']/df['distance']
   df_aux=((df[['delivery_person_id','city','min_per_Km']]
   .groupby(['city','delivery_person_id']).mean().
   sort_values(['city','min_per_Km'],axis=0, ascending=True).reset_index()))
    
   df_aux1=df_aux.loc[df_aux['city']=='Metropolitian',:].head(10)
   df_aux2=df_aux.loc[df_aux['city']=='Urban',:].head(10)
   df_aux3=df_aux.loc[df_aux['city']=='Semi-Urban',:].head(10)
   df_faster=pd.concat([df_aux1, df_aux2, df_aux3],axis=0).sort_values(['min_per_Km'],axis=0, ascending=False).reset_index(drop=True)
   df_faster=df_faster.head(10)
   return df_faster

def weather_rating(df):
    df_weather_rating = (df.loc[:,['weatherconditions', 'delivery_person_ratings']].
                         groupby('weatherconditions').agg({'delivery_person_ratings':['mean','std']}))
    df_weather_rating.columns=['mean_weather', 'std_weather']
    df_weather_rating=df_weather_rating.reset_index()
    return df_weather_rating

def mean_rating(df):
    df_mean_rating = (df[['delivery_person_id', 'delivery_person_ratings']].
                         groupby('delivery_person_id').mean().reset_index())
    return df_mean_rating

def traffic_rating(df):
                df_traffic_rating = (df.loc[:,['road_traffic_density', 'delivery_person_ratings']].
                                     groupby('road_traffic_density').agg({'delivery_person_ratings':['mean','std']}))
                df_traffic_rating.columns=['mean_rating_traffic', 'std_rating_traffic']
                df_traffic_rating=df_traffic_rating.reset_index()
                return df_traffic_rating
            
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
        Output: Dataframe
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

###########################
# load
###########################
df=pd.read_csv('train.csv')
df=clear_data(df)      
                           
#=========================================================
# Side Bar
#==========================================================
st.sidebar.markdown('# :red[Cury Company]')
st.sidebar.markdown('### :sunglasses: _:green[Delivery person View]_ ')

#path_img=r'C:\Users\Utente77\repos/FTC_Curso/img/shaian-ramesht-exSEmuA7R7k-unsplash_.jpg'
image=Image.open('shaian-ramesht-exSEmuA7R7k-unsplash_.jpg')
st.sidebar.image(image)

st.sidebar.markdown('----------------------')

st.sidebar.markdown('## :orange[Select the date:]')

dateslider=st.sidebar.slider("Date up to:",
                  value=pd.datetime(2022,4,6),
                  min_value=pd.datetime(2022,1,1), 
                  max_value=pd.datetime( 2022, 12, 31), format="DD-MM-YYYY" )


st.sidebar.markdown('----------------------')

st.sidebar.markdown('## :orange[Select the traffic type:]')

trafficselection=st.sidebar.multiselect ("what is the traffic today?",
                                        ['Low','Jam','Medium','High'],['Low','Jam','Medium','High'])

st.sidebar.markdown('----------------------')

st.sidebar.markdown('## :orange[ Select the city type:]')

cityselection=st.sidebar.multiselect ("Which city type?",
                                        ['Metropolitian','Urban'], ['Metropolitian','Urban'])
                                         
st.sidebar.markdown('----------------------')
st.sidebar.markdown('###### @by Alessandra Barbosa')

# link side bar 
df=df.loc[df['order_date']<= dateslider,:]
df=df.loc[df['road_traffic_density'].isin( trafficselection),:] 
df=df.loc[df['city'].isin( cityselection),:]                                         

############################################################
# Layout
############################################################
st.header('_:red[Cury Company] :green[Delivery person View]_ ')
st.caption('Cury Company is a marketplace that connects restaurants, delivery personnel, and consumers through its app.')
st.caption('In this project, I was responsible for designing metrics, analyzing data, creating a dashboard, and developing an algorithm to assist the CEO in accurately estimating delivery times.')

tab1, tab2, tab3 = st.tabs(["Strategic View", "---", "---"])

with tab1:
    with st.container():
        #order metric
        st.subheader('Metrics Overall')
        cols1,cols2,cols3,cols4=st.columns(4, gap='large')

        with cols1:
            age=df['delivery_person_age'].min()
            cols1.metric('Lowest age',age)
        with cols2:
            age=df['delivery_person_age'].max()
            cols2.metric('High age',age)
            
        with cols3:
            cond=df['vehicle_condition'].min()
            cols3.metric('Worst condition of vehicle',cond)

        with cols4:
            cond=df['vehicle_condition'].max()
            cols4.metric('Best condition of vehicle',cond)
            
    with st.container():

        st.markdown('---------')
        st.subheader('Speed')
        cols1,cols2=st.columns(2, gap='large')
        
        with cols1:
            st.subheader('Top 10 fastest couriers by city')         
            df_faster= distance(df)   
            st.dataframe(df_faster)           

        with cols2:
            fig=px.bar( df_faster, x='min_per_Km', y='delivery_person_id', text_auto='.2s', color='city', orientation='h',title="Faster delivery person")
            st.plotly_chart(fig, use_container_width=True)
            
    with st.container():
        st.markdown('---------')

        cols1,cols2=st.columns(2, gap='large')
        with cols1:
            st.subheader('The 10 slowest couriers by city')
            df_lower=slowest(df)
            st.dataframe(df_lower) 
            
        with cols2:
            fig=px.bar( df_lower, x='min_per_Km', y='delivery_person_id', text_auto='.2s', color='city', orientation='h',title="Slowest delivery person")
            st.plotly_chart(fig, use_container_width=True)

    with st.container():

        st.markdown('---------')
        st.subheader('Rattings')
        
        cols1,cols2,cols3=st.columns(3, gap='large')
        
        with cols1:
            st.markdown('##### Average rating per courier')
            df_mean_rating=mean_rating(df)
            st.dataframe(df_mean_rating)
            
        with cols2:
            st.markdown('##### Average rating and standard deviation by traffic type')
            
            df_traffic_rating=traffic_rating(df)
            st.dataframe(df_traffic_rating)
            
        with cols3:
            st.markdown('##### Average rating and standard deviation by weather conditions')
            df_weather_rating=weather_rating(df)
            st.dataframe(df_weather_rating)
            
