import streamlit as st
import pandas as pd 
import plotly.express as px

data = pd.read_parquet("data.parquet.gzip")

st.title("Water Access Points in Africa")
st.sidebar.title("Sidebar")
st.sidebar.write("")
country = st.sidebar.selectbox("Select the country you wish to analyse:",
                     ["All"] + list(data.country_name.unique()))
if country != "All":
    data = data[data.country_name == country].copy()

st.write(country)
st.write(data)
col1, col2 = st.columns([5,5])

with col1:
    wt = st.multiselect(
        label="Select the water te3ch you wish to see:",
        options=data.water_tech.unique())
    checkbox_wt = st.checkbox("Apply water tech filter.")

with col2:
    ws = st.multiselect(
        label="Select the water tech you wish to see:",
        options=data.water_source.unique())
    checkbox_ws = st.checkbox("Apply water source filter.")

if checkbox_wt:
    filter_ = data.water_tech.apply(lambda x: x in wt)
    data = data[filter_].copy()

if checkbox_ws:
    filter_ = data.water_source.apply(lambda x: x in ws)
    data = data[filter_].copy()

st.dataframe(data)

# filters: water_tech, water_source

st.header("Data Visualization")

selection = st.radio("Select the variable you wish to visualize:",
["Water source", "Water tech"])

mapping = {"Water source": "water_source",
"Water tech": "water_tech"}

selection = mapping[selection]

data_per_water_source = data.groupby(selection,
as_index=False).agg("count")[[selection, "row_id"]]

data_per_water_source.columns = [selection, "number"]
data_per_water_source.sort_values("number", inplace=True)

fig = px.bar(data_per_water_source,
x="number",
y=selection,
orientation="h",
title="number of water access points per {}".format(selection.replace("_", " ")),
template="simple_white",
labels={
    "water_source": "Water Source",
    "water_tech": "Water Tech",
    "number": "Number of water access points"
})







st.plotly_chart(fig)

fig = px.scatter_geo(data,
lat="lat_deg",
lon="lon_deg",
color=selection,
opacity=0.5,
title="Geographical location of access points",
labels={
    "lat_deg": "Latitude",
    "lon_deg": "Longitude",
    "water_source": "Water Source",
    "water_tech": "Water Tech",
    "number": "Number of water access points"},
template="simple_white",
hover_name="country_name",
hover_data=["install_year"],
scope='africa',
projection='mercator')

st.plotly_chart(fig)