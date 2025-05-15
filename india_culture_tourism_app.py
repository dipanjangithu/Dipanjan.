import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
from PIL import Image

# Snowflake connection (replace with actual credentials)
conn = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='CULTURE_TOURISM',
    schema='PUBLIC'
)

# Function to load data from Snowflake
def load_data(query):
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    return df

# Streamlit app
st.title("Explore India's Art, Culture, and Responsible Tourism")

# Sidebar for navigation
section = st.sidebar.selectbox("Choose Section", ["Home", "Cultural Heritage", "Tourism Insights", "Responsible Tourism"])

if section == "Home":
    st.header("Welcome to India's Cultural Journey")
    st.write("Discover traditional art forms, cultural experiences, and eco-tourism destinations.")
    st.image("https://example.com/taj_mahal.jpg", caption="Taj Mahal, a UNESCO World Heritage Site")

elif section == "Cultural Heritage":
    st.header("Cultural Heritage Explorer")
    # Load heritage sites data
    heritage_query = "SELECT * FROM HERITAGE_SITES"
    heritage_df = load_data(heritage_query)
    
    # Display map
    fig = px.scatter_geo(heritage_df, lat="LATITUDE", lon="LONGITUDE", hover_name="SITE_NAME",
                         title="Cultural Heritage Sites in India")
    st.plotly_chart(fig)
    
    # Display sample art form image
    st.subheader("Traditional Art Forms")
    st.image("https://example.com/madhubani_painting.jpg", caption="Madhubani Painting")

elif section == "Tourism Insights":
    st.header("Tourism Insights Dashboard")
    # Load tourism data
    tourism_query = "SELECT * FROM TOURISM_STATISTICS"
    tourism_df = load_data(tourism_query)
    
    # Bar chart for tourist visits by state
    state_visits = tourism_df.groupby("STATE")["TOTAL_VISITS"].sum().reset_index()
    fig = px.bar(state_visits, x="STATE", y="TOTAL_VISITS", title="Tourist Visits by State")
    st.plotly_chart(fig)
    
    # Line chart for seasonal trends
    monthly_visits = tourism_df.groupby("MONTH")["TOTAL_VISITS"].sum().reset_index()
    fig = px.line(monthly_visits, x="MONTH", y="TOTAL_VISITS", title="Monthly Tourism Trends")
    st.plotly_chart(fig)

elif section == "Responsible Tourism":
    st.header("Responsible Tourism Guide")
    # Load protected areas data
    protected_query = "SELECT * FROM PROTECTED_AREAS"
    protected_df = load_data(protected_query)
    
    # Display map
    fig = px.scatter_geo(protected_df, lat="LATITUDE", lon="LONGITUDE", hover_name="AREA_NAME",
                         title="Eco-Tourism Destinations in India")
    st.plotly_chart(fig)
    
    # Eco-tourism tips
    st.subheader("Tips for Responsible Travel")
    st.write("- Support local communities by using local guides.")
    st.write("- Avoid single-use plastics in protected areas.")
    st.write("- Respect wildlife and maintain a safe distance.")

# Close Snowflake connection
conn.close()