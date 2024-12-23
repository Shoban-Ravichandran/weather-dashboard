import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import time

# Function to Fetch Weather Data
def fetch_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'City': data['name'],
            'Temperature (°C)': data['main']['temp'],
            'Humidity (%)': data['main']['humidity'],
            'Weather': data['weather'][0]['description'],
            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_info
    else:
        st.error("Failed to fetch data. Check the city name or API key.")
        return None

# Streamlit App Layout
st.title("Live Weather Dashboard 🌤️")

# Input Section
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key:", type="password")
city = st.sidebar.text_input("Enter the city name:", value="Dublin")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds):", 10, 300, 60)

# Placeholder for live updates
placeholder = st.empty()

if api_key and city:
    # Live Weather Data Display
    with placeholder.container():
        while True:
            weather_data = fetch_weather(city, api_key)
            if weather_data:
                # Display Data
                st.subheader("Weather Data")
                st.write(weather_data)

                # DataFrame for Visualization
                df = pd.DataFrame([weather_data])

                # Temperature & Humidity Plot
                st.subheader("Temperature & Humidity")
                fig, ax = plt.subplots()
                ax.bar(["Temperature", "Humidity"], [df['Temperature (°C)'][0], df['Humidity (%)'][0]], color=["blue", "green"])
                ax.set_ylabel("Value")
                st.pyplot(fig)

                # Advanced Visualization with Plotly
                st.subheader("Interactive Visualization")
                fig_plotly = px.bar(
                    x=["Temperature (°C)", "Humidity (%)"],
                    y=[df['Temperature (°C)'][0], df['Humidity (%)'][0]],
                    labels={'x': "Metric", 'y': "Value"},
                    title=f"Weather Metrics for {city}"
                )
                st.plotly_chart(fig_plotly)

                # CSV Download Option
                st.download_button(
                    label="Download Weather Data as CSV",
                    data=df.to_csv(index=False),
                    file_name=f'{city}_weather_data.csv',
                    mime='text/csv',
                )

            # Wait for the refresh interval before updating
            time.sleep(refresh_interval)
else:
    st.warning("Please enter both the API key and city name in the sidebar to start.")
