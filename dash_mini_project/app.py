import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(layout='wide')

# Load dataset
df = pd.read_csv(r'india.csv')

# Sidebar Components
st.sidebar.title('India Ka Data Viz')

list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')

selected_state = st.sidebar.selectbox('Select a state', list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter', sorted(df.columns[0:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns[0:]))

# Graph Type Selection
graph_type = st.sidebar.selectbox(
    "Select Graph Type", 
    ["Scatter Map", "Bar Chart", "Line Chart", "Pie Chart", "Bubble Chart", "Histogram", "Box Plot", "Heatmap"]
)

plot = st.sidebar.button('Plot Graph')

if plot:
    st.subheader(f"Visualization: {graph_type}")
    st.text('Size represents primary parameter')
    st.text('Color represents secondary parameter')

    if selected_state == 'Overall India':
        data = df
    else:
        data = df[df['State'] == selected_state]

    # Generate Graphs Based on Selection
    if graph_type == "Scatter Map":
        fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", 
                                size=primary, color=secondary, zoom=6 if selected_state != 'Overall India' else 4,
                                size_max=35, mapbox_style="carto-positron", 
                                width=1200, height=700, hover_name='District')

    elif graph_type == "Bar Chart":
        fig = px.bar(data, x="District", y=primary, color=secondary, 
                     title=f"{primary} vs {secondary} in {selected_state}", 
                     width=1200, height=700)

    elif graph_type == "Line Chart":
        fig = px.line(data, x="District", y=primary, color=secondary, 
                      title=f"Line Chart of {primary} vs {secondary} in {selected_state}", 
                      markers=True, width=1200, height=700)

    elif graph_type == "Pie Chart":
        fig = px.pie(data, names="District", values=primary, 
                     title=f"Distribution of {primary} in {selected_state}", 
                     width=900, height=700)

    elif graph_type == "Bubble Chart":
        fig = px.scatter(data, x="District", y=primary, size=secondary, color=secondary, 
                         title=f"Bubble Chart of {primary} vs {secondary} in {selected_state}", 
                         width=1200, height=700)

    elif graph_type == "Histogram":
        fig = px.histogram(data, x=primary, color=secondary, 
                           title=f"Distribution of {primary} in {selected_state}", 
                           width=1200, height=700, nbins=20)

    elif graph_type == "Box Plot":
        fig = px.box(data, x="District", y=primary, color=secondary, 
                     title=f"Box Plot of {primary} in {selected_state}", 
                     width=1200, height=700)

    elif graph_type == "Heatmap":
        correlation_matrix = data.select_dtypes(include=[np.number]).corr()
        fig = ff.create_annotated_heatmap(
            z=correlation_matrix.values,
            x=list(correlation_matrix.columns),
            y=list(correlation_matrix.index),
            annotation_text=np.round(correlation_matrix.values, 2),
            colorscale="Viridis",
            showscale=True
        )

    # Display Plot
    st.plotly_chart(fig, use_container_width=True)



