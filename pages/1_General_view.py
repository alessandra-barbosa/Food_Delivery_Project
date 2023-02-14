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

st.set_page_config(page_title="Company View", page_icon=":)", layout="wide")

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
    
def maps(df):
        data_plot = df.loc[:,['city', 'road_traffic_density','delivery_location_latitude','delivery_location_longitude']].groupby(                    
                                ['city','road_traffic_density']).median().reset_index()
        # Desenhar o mapa
        map = folium.Map( zoom_start=0.1 )
        for index, location_info in data_plot.iterrows():
            folium.Marker( [location_info['delivery_location_latitude'],
            location_info['delivery_location_longitude']],
            popup=location_info[['city', 'road_traffic_density']] ).add_to( map )
        folium_static(map, width=1024,height=600)
        return None
    
def order_person_week(df):
        df_aux1 = df.loc[:, ['id', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
        df_aux2 = df.loc[:, ['delivery_person_id', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
        df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
        df_aux['order_by_delivery'] = df_aux['id'] / df_aux['delivery_person_id']
        # gráfico
        fig=px.line( df_aux, x='week_of_year', y='order_by_delivery', markers=True, title="Orders per delivery person a week" )    
        st.plotly_chart(fig, use_container_width=True)
        return fig
    
def order_week(df):
            df['week_of_year'] = df['order_date'].dt.strftime( "%U" )
            df_aux = df.loc[:, ['id', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
            df_aux.columns = ['week_of_year','orders']
            # gráfico
            fig=px.bar( df_aux, x='week_of_year', y='orders', text_auto='.2s', color='orders', title="Orders per week")
            st.plotly_chart(fig, use_container_width=True)
            return fig
        
def order_traffic_city(df):

                df_aux = df.loc[:, ['id', 'city','road_traffic_density']].groupby(['city','road_traffic_density']
                    ).count().reset_index()
                fig=px.scatter( df_aux, x='city', y='road_traffic_density', 
                               size='id', color='city', title="Orders per traffic density and city")
                st.plotly_chart(fig, use_container_width=True)
                return fig
            
def order_traffic(df):
                df_aux = df.loc[:, ['id', 'road_traffic_density']].groupby( 'road_traffic_density' ).count().reset_index()
                df_aux['perc_id'] = 100 * ( df_aux['id'] / df_aux['id'].sum() )
                # gráfico
                fig=px.pie( df_aux, values='perc_id', names='road_traffic_density',title="Orders per traffic density")
                st.plotly_chart(fig, use_container_width=True)
                return fig
            
def order_metric(df): 
    """ define metrics of orders"""
    
    df_aux = df.loc[:, ['id', 'order_date']].groupby( 'order_date' ).count().reset_index()
    df_aux.columns = ['order_date', 'orders']
    fig=px.bar( df_aux, x='order_date', y='orders', text_auto='.2s', color='orders', title="Orders per day")
    st.plotly_chart(fig, use_container_width=True)
    return fig
        
    
#############
# load
#############

#df=pd.read_csv(r'C:\Users\Utente77\repos\FTC_Curso\dataset\train.csv')
df=pd.read_csv('train.csv')

df=clear_data(df)      

#=========================================================
# Side Bar
#==========================================================
st.sidebar.markdown('# :red[Cury Company]')
st.sidebar.markdown('### :sunglasses: _:green[General View]_ ')

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

st.header('_:red[Cury Company] :green[General View]_ ')
st.caption('Cury Company is a marketplace that connects restaurants, delivery personnel, and consumers through its app.')
st.caption('In this project, I was responsible for designing metrics, analyzing data, creating a dashboard, and developing an algorithm to assist the CEO in accurately estimating delivery times.')

tab1, tab2, tab3 = st.tabs(["Strategic View", "Management View", "Geografic View"])

with tab1:
    with st.container():
        #order metric
        fig=order_metric(df)
        
   
    with st.container():
        st.markdown('----------------------')

        cols1,cols2=st.columns(2)

        with cols1:
            fig=order_traffic(df)
            
        with cols2:
            fig=order_traffic_city(df)
            
with tab2:
    cols1,cols2=st.columns(2)

    with cols1:
        fig=order_week(df)
        
    with cols2:
        fig=order_person_week(df)
    
with tab3:
    st.markdown( '## Country Map')
    maps(df)

    