import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="URL Shortener Dashboard", layout="centered")

st.title("🔗 URL Shortener & Analytics")

# --- Tab 1: Create Short Link ---
tab1, tab2 = st.tabs(["Create Link", "View Analytics"])

with tab1:
    st.subheader("Shorten a new URL")
    long_url = st.text_input("Enter Long URL (e.g., https://example.com)")
    
    if st.button("Shorten!"):
        if long_url:
            with st.spinner("Generating short link..."):
                response = requests.post(
                    f"{API_BASE_URL}/api/shorten", 
                    json={"long_url": long_url}
                )
                if response.status_code == 200:
                    data = response.json()
                    short_code = data["short_code"]
                    short_url = f"{API_BASE_URL}/{short_code}"
                    st.success("Success!")
                    st.code(short_url, language="text")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Invalid Request')}")

# --- Tab 2: Analytics ---
with tab2:
    st.subheader("Link Analytics")
    search_code = st.text_input("Enter Short Code (e.g., b, c, 1A)")
    
    if st.button("Get Stats"):
        if search_code:
            with st.spinner("Fetching analytics..."):
                response = requests.get(f"{API_BASE_URL}/api/analytics/{search_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown(f"**Original URL:** [{data['long_url']}]({data['long_url']})")
                    st.metric(label="Total Clicks", value=data['total_clicks'])
                    
                    if data['total_clicks'] > 0:
                        df = pd.DataFrame(data['clicks'])
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        df['date'] = df['timestamp'].dt.date
                        
                        # Clicks over time chart
                        clicks_per_day = df.groupby('date').size().reset_index(name='clicks')
                        fig = px.line(clicks_per_day, x='date', y='clicks', title="Clicks Over Time", markers=True)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Raw Data table
                        st.write("Recent Activity Log")
                        st.dataframe(df[['timestamp', 'ip_address', 'user_agent']].sort_values(by='timestamp', ascending=False))
                    else:
                        st.info("No clicks recorded yet.")
                else:
                    st.error("Analytics not found for this short code.")