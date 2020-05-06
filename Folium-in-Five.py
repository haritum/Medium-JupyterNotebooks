#!/usr/bin/env python
# coding: utf-8

# # Folium in Five:

# ### Introduction to Folium: 
# - Manipulates data in Python, then visualize it in on a Leaflet map via _folium_. 
# - In other words, data is manipulated in Python and visualized on an interactive leaflet map. 
# - It enables both the binding of data to a map for choropleth visualization as well as vector/raster/HTNL visualizations as markers on the map.
# - No. of built-in tilesets include:
#     - OpenStreetMap
#     - Mapbox and Stamen
#     - Custom tilesets support with Mapbox or Cloudmade API keys
# - Allows both Image, Video, GeoJSON and TopoJSON overlays.

# ### Installation of Folium (locally):
# Python 3.x doesn't come pre-installed with _folium_ library. You can install _folium_ by typing the below command on your terminal.  

# ```
# $ pip install --user folium
# ```

# ### First Base Map in Folium:
# We need to specify the coordinates (latitude and longitude) of interest to create a base map. Ofcourse, this is after importing _folium_ module.

# In[1]:


import numpy as np
import pandas as pd
import folium
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[41]:


europe_map = folium.Map(location=[50.0, 15.0],
                        width='100%', height='80%',
                        zoom_start=3)
europe_map


# ### Different Map Tiles in Folium:
# Having a choice among different map tiles can be a great way to change or improve the look of the map. 
# The default tile in folium, which is shown above, is "OpenStreetMap". Now, let's try some other tile possibilities. 

# In[40]:


europe_map1 = folium.Map(location=[50.0, 15.0],
                        tiles='openstreetmap',
                        width='100%', height='80%',
                        zoom_start=3)
europe_map1


# #### Stamen Terrain:

# In[42]:


europe_map2 = folium.Map(location=[50.0, 15.0],
                        width='100%', height='80%', 
                        tiles='stamenterrain',
                        zoom_start=3)
europe_map2


# #### Stamen Toner:

# In[43]:


europe_map3 = folium.Map(location=[50.0, 15.0],
                        tiles='stamentoner',
                        width='100%', height='80%',  
                        zoom_start=3)
europe_map3


# #### Stamen Watercolor:

# In[44]:


europe_map4 = folium.Map(location=[50.0, 15.0],
                        tiles='stamenwatercolor',
                        width='100%', height='80%', 
                        zoom_start=3)
europe_map4


# #### Mapbox:
# For building a custom map using API key.

# ### Markers
# As per the documentation, there are _numerous_ marker types. Let's try out adding makers on some (9) of the popular cities in Europe i.e., Paris, Rome, Amsterdam, Brussels, Berlin, Madrid, Vienna, Stockholm, Geneva.  

# In[7]:


# Instead of creating a customized information about european cities, 
#    I have downloaded all the world cities information that is freely available.
world_cities_df = pd.read_csv('data/worldcities.csv')


# In[8]:


europe_cities = ['Paris','Rome','Amsterdam','Brussels','Berlin','Barcelona','Vienna','Stockholm','Geneva']
europe_cities_df = world_cities_df[world_cities_df['city'].isin(europe_cities)]


# Looks like, there are cities in the US with exactly the same name as their popular european counterparts. Let's drop those for now!

# In[9]:


europe_cities_df['country'].unique()


# In[10]:


europe_cities_df = europe_cities_df[europe_cities_df['country'] != 'United States']


# In[11]:


europe_cities_df = europe_cities_df[europe_cities_df['country'] != 'Venezuela']


# In[12]:


europe_cities_df.reset_index(inplace=True)
europe_cities_df.drop(columns=['index','id','admin_name','iso3','capital','population','city_ascii'], inplace=True)


# In[13]:


europe_cities_df


# Let's use the OpenStreetMap created for europe and add these popular cities as markers one by one on the map.  

# In[14]:


for icity,ilat,ilng in zip(europe_cities_df.city,europe_cities_df.lat,europe_cities_df.lng):
    folium.Marker([ilat, ilng], popup='<i>'+icity+'</i>', icon=folium.Icon(icon='info-sign')).add_to(europe_map)


# In[15]:


europe_map.save('europe_cities9_openstreetmap.html')


# ### Tiles & Layer Control
# Now, we are going to add a control with "TileLayer()" or switch between layers with the "LayerControl()" methods. After completing the task, look for the layer control on the top right of the map. We have now successfully created an interactive feature in the map using _folium_ methods.

# In[45]:


imap = folium.Map(location=[50.0, 15.0],
                  zoom_start=3)
folium.TileLayer('openstreetmap').add_to(imap)
folium.TileLayer('stamenterrain').add_to(imap)
folium.TileLayer('stamentoner').add_to(imap)
for icity,ilat,ilng in zip(europe_cities_df.city,europe_cities_df.lat,europe_cities_df.lng):
    folium.Marker([ilat, ilng], popup='<i>'+icity+'</i>', icon=folium.Icon(icon='info-sign')).add_to(imap)
folium.LayerControl().add_to(imap)
imap.save('europe_cities9_interactive.html')


# Of course, we can customize our map, icons, popups as we want. Now, let's try out one more powerful feature of _folium_: Overlays.

# ### Overlays in Folium
# - GeoJSON and TopoJSON layers can be passed to the map as an overlay.
# - Multiple layers can be visualized on the same map.
# 
# Let's now test our _folium_ skills learnt so far by creating a final 'visual of the day'. To make things a a bit more interesting, we choose to work with live data. 
# 
# Since, **Soccer** (undoubtedly!) is one of the most popular sport in Europe. We are going to use [Soccer Database from Kaggle](https://d17h27t6h515a5.cloudfront.net/topher/2017/November/5a0a4cad_database/database.sqlite) and create a Choropleth map of the total number of matches played in different countries across Europe from 2008 to 2016.    

# #### Soccer data from Kaggle (locally downloaded)
# I already downloaded the soccer data from Kaggle and saved it locally on my machine. Let's first connect to the local SQLite database and pull the required data.

# In[17]:


import sqlite3

#
# Function to create an SQL connection
def sql_connection(loc):
    try:
        con = sqlite3.connect(loc)
        print("Connection successfully established to Database: {}\n".format(loc))
        return con
    except Error:
        print(Error)

#
# Function to return a list of tables present in the SQLite3 Database
def sql_tables(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type="table"')
    list_tables = list(itab[0] for itab in cursorObj.fetchall())
    return list_tables

#
# Function to return rows from Player_Atrributes table in the SQLite3 Database
def sql_table(con,table_name):
    df = pd.read_sql_query("SELECT * FROM "+table_name, con)    
    return df 


# Call functions to load soccer data from SQLite database
con = sql_connection("data/europe_soccer.sqlite")    
tab = sql_tables(con)
print('List of Tables in the Soccer Database are:')
for itab in tab:
    print(itab)
# 
# Database tables are loaded into Pandas DataFrames
soccer_matches = sql_table(con, 'Match')
soccer_country = sql_table(con, 'Country')


# ### Which of the 27 European countries play soccer?

# In[18]:


soccer_country


# Now, let's recreate the interactive folium map with capitals of soccer playing countries in europe as markers. To do this, we need to take help of the world_cities Data Frame from before. I will do this in two steps. First, islocate the european cities from that of the world. Second, drop the european cities that are not capitals. I am doing this simply to avoid cluttering of the markers on the map. Anyway, you will understand why I did this after looking at the final 'visual for the day'. 

# No wonder the names England and Scotland are marked in the world cities as United Kingdom. We are going to address this issue by creating a new data frame for 'United Kingdom' called df_uk and merging it with the final data frame.

# In[19]:


uk_df = world_cities_df[(world_cities_df['country'] == 'United Kingdom') & (world_cities_df['city'].isin(['London','Edinburgh']))]
uk_df


# In[20]:


list_soccer_country = soccer_country['name'].values
list_soccer_country


# In[21]:


soccer_europe_cities = world_cities_df[world_cities_df['country'].isin(list_soccer_country)]
soccer_europe_cities.head()


# In[22]:


soccer_europe_capitals = soccer_europe_cities[(soccer_europe_cities['capital'] == 'primary')]
soccer_europe_capitals = soccer_europe_capitals[soccer_europe_capitals['city'] != 'The Hague']
soccer_europe_capitals


# In[23]:


soccer_europe_capitals = pd.concat([soccer_europe_capitals, uk_df])
soccer_europe_capitals


# I am quickly checking if the newly created dataframe (soccer_europe_capitals) has same no. of rows as that of soccer_country. If not, we need drop few data.

# In[24]:


soccer_country.shape[0] == soccer_europe_capitals.shape[0]


# Let's drop unnecessary columns from soccer_europe_capitals dataframe.

# In[25]:


soccer_europe_capitals.drop(columns=['city_ascii','iso3','admin_name','population','id','capital'], inplace=True)
soccer_europe_capitals.reset_index(inplace=True)
soccer_europe_capitals


# In[26]:


soccer_europe_capitals


# OK! We have now successfully created a new dataframe of the capitals of soccer playing countries in europe. Let's highlight then as markers on a folium openstreetmap.

# In[46]:


soccer_map = folium.Map(location=[50.0,6.0],
                        width='100%', height='80%',
                         zoom_start=4)
folium.TileLayer('openstreetmap').add_to(soccer_map)
folium.TileLayer('stamentoner').add_to(soccer_map)
for icity,ilat,ilng in zip(soccer_europe_capitals.city,soccer_europe_capitals.lat,soccer_europe_capitals.lng):
    folium.Marker([ilat, ilng], popup='<i>'+icity+'</i>', icon=folium.Icon(icon='info-sign')).add_to(soccer_map)
folium.LayerControl().add_to(soccer_map)
soccer_map


# In[28]:


soccer_map.save('europe_soccer_capitals.html')


# In[29]:


soccer_country[soccer_country['id'].isin(soccer_matches['country_id'].unique())]


# In[30]:


#soccer_matches['country_id'].unique()
match_count_dict = soccer_matches['country_id'].value_counts().to_dict()
match_count_dict


# In[31]:


soccer_country['match_count'] = soccer_country['id']
soccer_country['match_count'] = soccer_country.apply(lambda x: match_count_dict[x['match_count']], axis=1)
soccer_country.replace({'England':'United Kingdom'}, inplace=True)
soccer_country


# In[39]:


import os

country_geo = os.path.join('data/world-countries.json')

soccer_map_choropleth = folium.Map(location=[50.0,6.0],
                                   zoom_start=4,
                                   width='100%', height='80%')
folium.TileLayer('openstreetmap').add_to(soccer_map_choropleth)
folium.TileLayer('stamentoner').add_to(soccer_map_choropleth)

for icity,ilat,ilng in zip(soccer_europe_capitals.city,soccer_europe_capitals.lat,soccer_europe_capitals.lng):
    folium.Marker([ilat, ilng], popup='<i>'+icity+'</i>', icon=folium.Icon(icon='info-sign')).add_to(soccer_map_choropleth)


folium.Choropleth(geo_data=country_geo,
                  name='choropleth',
                  data=soccer_country,
                  columns=['name','match_count'],
                  key_on='feature.properties.name',
                  fill_color='YlOrRd',
                  nan_fill_color='white',
                  fill_opacity=0.45,
                  line_opacity=0.5,
                  legend_name='No. of matches [2008-2016]').add_to(soccer_map_choropleth)

folium.LayerControl().add_to(soccer_map_choropleth)
soccer_map_choropleth


# In[33]:


soccer_map.save('europe_soccer_capitals_choropleth.html')


# I didn't have to use two different dataframes: one for plotting choropleth map and another for city markers. The issue popped in as Kaggle considered England and Scotland as two different countries. Whereas, choropleth world json considered England and Scotland together as 'United Kingdom'. For some reason I didn't want to spend more time on this trivial issue. I guess, I can now say, final 'visual for the day' is done. See you next time around!
