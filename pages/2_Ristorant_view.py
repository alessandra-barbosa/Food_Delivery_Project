#imports
import pandas                 as pd
import numpy                  as np
import plotly.express         as px
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import plotly.graph_objects as go

st.set_page_config(page_title="Company View", page_icon=":)", layout="wide")

###########################
# #Auxiliary functions
############################
def delivery_city_traf(df):
            df_delivery = df.loc[:,['time_taken(min)', 'city','road_traffic_density']].groupby(['city','road_traffic_density']).agg({'time_taken(min)':['mean','std']})
            df_delivery.columns=['mean_time_taking', 'std_time_taking']
            df_delivery=df_delivery.reset_index()
            fig=px.sunburst(df_delivery, path=['city','road_traffic_density'], values='mean_time_taking',color='std_time_taking',
            color_continuous_scale='RdBu',color_continuous_midpoint=np.average(df_delivery['std_time_taking']))
            st.plotly_chart(fig)
            return fig
        
def delivery_2(df_delivery):
    fig=go.Figure(data=[go.Pie(labels=df_delivery['city'],values=df_delivery['mean_time_taking'],pull=[0,0,0.2])])
    st.plotly_chart(fig)
    return fig

def delivery_1(df):
    df_delivery = df.loc[:,['time_taken(min)', 'city','type_of_order']].groupby(['city','type_of_order']).agg({'time_taken(min)':['mean','std']})
    df_delivery.columns=['mean_time_taking', 'std_time_taking']
    df_delivery=df_delivery.reset_index()
    return df_delivery

def delivery(df):

    df_delivery = df.loc[:,['time_taken(min)', 'city']].groupby('city').agg({'time_taken(min)':['mean','std']})
    df_delivery.columns=['mean_time_taking', 'std_time_taking']
    df_delivery=df_delivery.reset_index()
    fig=go.Figure()
    fig.add_trace(go.Bar(name='Control',x=df_delivery['city'],y=df_delivery['mean_time_taking'],error_y=dict(type='data',       array=df_delivery['std_time_taking'])))                                  
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)
    return fig
                
def distance(df):
    df['distance']=(df[['restaurant_latitude','restaurant_longitude','delivery_location_latitude','delivery_location_longitude']]
                    .apply(lambda x: haversine(
    (x['restaurant_latitude'],x['restaurant_longitude']),(x['delivery_location_latitude'],x['delivery_location_longitude'])), axis=1))
    aux= np.round(df['distance'].mean(),2)
    return aux
            
def nofest(df):
    df_fest=df.loc[df['festival']!='Yes']
    df_fest=np.round(df_fest['time_taken(min)'],2)
    return df_fest

def fest(df):
    df_fest=df.loc[df['festival']=='Yes']
    df_fest=np.round(df_fest['time_taken(min)'],2)
    return df_fest

def clear_data(df):
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

#####################                    
# load
#####################

df=pd.read_csv('train.csv')
df=clear_data(df)   

#=========================================================
# Side Bar
#==========================================================
st.sidebar.markdown('# :red[Cury Company]')
st.sidebar.markdown('### :sunglasses: _:green[Ristorant View]_ ')

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
                                        ['Metropolitian','Urban', 'Semi-Urban'], ['Metropolitian','Urban', 'Semi-Urban'])
                                         
st.sidebar.markdown('----------------------')
st.sidebar.markdown('###### @by Alessandra Barbosa')

# link side bar 
df=df.loc[df['order_date']<= dateslider,:]
df=df.loc[df['road_traffic_density'].isin( trafficselection),:] 
df=df.loc[df['city'].isin( cityselection),:]                                         

#####################
# Layout
#####################

st.header('_:red[Cury Company] :green[Ristorant View]_ ')
st.caption('Cury Company is a marketplace that connects restaurants, delivery personnel, and consumers through its app.')
st.caption('In this project, I was responsible for designing metrics, analyzing data, creating a dashboard, and developing an algorithm to assist the CEO in accurately estimating delivery times.')

tab1, tab2, tab3 = st.tabs(["Strategic View", "---", "---"])

with tab1:
    with st.container():
        # order metric
        st.subheader('Metrics Overall')
        cols1,cols2,cols3,cols4,cols5,cols6=st.columns(6, gap='large')

        with cols1:
            aux=len(df['delivery_person_id'].unique())
            cols1.metric( 'delivery person',aux )
            
        with cols2:
            aux=distance(df)
            cols2.metric( 'Avg distance restaurants',aux )

        with cols3:      
            
            df_fest=np.round(fest(df).mean(),2)
            cols3.metric( 'Avg Festival',df_fest )

        with cols4:
            df_fest=np.round(fest(df).std(),2)
            cols4.metric( 'Std Festival',df_fest)
            
        with cols5:
            df_fest=np.round(nofest(df).mean(),2)
            cols5.metric( 'Avg No festival',df_fest )
            
        with cols6:
            df_fest=np.round(nofest(df).std(),2)
            cols6.metric( 'Std No festival',df_fest )
            
    with st.container():
        st.markdown('----------------------')

        cols1,cols2=st.columns(2, gap='large')
        with cols1:
            st.markdown('### Average delivery time and standard deviation by city')
            fig=delivery(df)
            
            
        with cols2:
            st.markdown('### Average delivery time and standard deviation by city and order type')
            df_delivery=delivery_1(df)
            st.dataframe(df_delivery)

    with st.container():
        st.markdown('----------------------')

        cols1,cols2=st.columns(2, gap='large')

        with cols1:
            st.markdown('###  Delivery time average and standard deviation by city')
            fig=delivery_2(df_delivery)
            
        with cols2:
            st.markdown('### Delivery time average and standard deviation by city and type of traffic')
            fig=delivery_city_traf(df)
        
    