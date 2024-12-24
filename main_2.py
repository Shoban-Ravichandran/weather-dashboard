import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import time

# Predefined list of available cities
available_cities = ["Dublin", "Paris", "New York", "London", "Tokyo", "Berlin", "Sydney", "Los Angeles", "Mumbai", "Cairo","Chennai"]

# Cache the weather data to improve performance
@st.cache_data
def fetch_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'City': data['name'],
            'Temperature (°C)': data['main']['temp'],
            'Humidity (%)': data['main']['humidity'],
            'Wind Speed (m/s)': data['wind']['speed'],
            'Pressure (hPa)': data['main']['pressure'],
            'Weather': data['weather'][0]['description'],
            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
            'Sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        }
        return weather_info
    else:
        st.error("Failed to fetch data. Check the city name or API key.")
        return None

# Fetch forecast data (optional)
@st.cache_data
def fetch_forecast(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        for entry in data['list'][:8]:  # Get next 24 hours forecast
            forecast_data.append({
                'Time': datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'Temperature (°C)': entry['main']['temp'],
                'Humidity (%)': entry['main']['humidity']
            })
        return pd.DataFrame(forecast_data)
    else:
        return None

# Fetch historical weather data (based on date range)
@st.cache_data
def fetch_historical_weather(city, api_key, start_date, end_date):
    lat, lon = get_city_coordinates(city, api_key)
    if not lat or not lon:
        return None

    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine"
    historical_data = []
    # Loop through the date range and fetch hourly data for each day
    for single_date in pd.date_range(start_date, end_date, freq="D"):
        timestamp = int(single_date.timestamp())
        response = requests.get(f"{url}?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}&units=metric")
        if response.status_code == 200:
            data = response.json()
            historical_data.append({
                'Date': single_date.strftime('%Y-%m-%d'),
                'Temperature (°C)': data['current']['temp'],
                'Humidity (%)': data['current']['humidity'],
                'Weather': data['current']['weather'][0]['description']
            })
    return pd.DataFrame(historical_data)

# Get latitude and longitude of the city
@st.cache_data
def get_city_coordinates(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None

# Streamlit App Layout
st.title("Live Weather Dashboard 🌤️")

# Dropdown selection for cities
cities = st.sidebar.multiselect("Select cities:", available_cities, default=["Chennai"])

# Input for API Key and Refresh Interval
api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key:", type="password")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds):", 10, 300, 30)

# Date range input for historical weather data
start_date = st.sidebar.date_input("Select Start Date for Historical Data", datetime(2023, 1, 1))
end_date = st.sidebar.date_input("Select End Date for Historical Data", datetime.now())

# Initialize session state to store historical weather data
if "weather_history" not in st.session_state:
    st.session_state.weather_history = []

# Placeholder for live updates for multiple cities
for city in cities:
    # Display the title without 'key' for subheader
    st.subheader(f"Weather Data for {city}")
    
    weather_data = fetch_weather(city, api_key)
    if weather_data:
        # Append the latest weather data to session history
        st.session_state.weather_history.append(weather_data)

        # Display Data
        st.write(weather_data)

        # DataFrame for Visualization
        df = pd.DataFrame([weather_data])

        # Temperature & Humidity Plot
        st.subheader("Temperature & Humidity")
        fig, ax = plt.subplots()
        ax.bar(["Temperature", "Humidity", "Wind Speed", "Pressure"], 
               [df['Temperature (°C)'][0], df['Humidity (%)'][0], df['Wind Speed (m/s)'][0], df['Pressure (hPa)'][0]], 
               color=["blue", "green", "orange", "red"])
        ax.set_ylabel("Value")
        st.pyplot(fig)

        # Advanced Visualization with Plotly - generate unique key for each city and time
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_key = f"interactive_plot_{city}_{timestamp}"
        
        st.subheader("Interactive Visualization")
        fig_plotly = px.bar(
            x=["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Pressure (hPa)"],
            y=[df['Temperature (°C)'][0], df['Humidity (%)'][0], df['Wind Speed (m/s)'][0], df['Pressure (hPa)'][0]],
            labels={'x': "Metric", 'y': "Value"},
            title=f"Weather Metrics for {city}"
        )
        st.plotly_chart(fig_plotly, use_container_width=True, key=unique_key)

        # Show 24-hour forecast with unique key
        forecast_df = fetch_forecast(city, api_key)
        if forecast_df is not None:
            st.subheader(f"24-Hour Forecast for {city}")
            st.write(forecast_df)
            fig_forecast = px.line(forecast_df, x="Time", y="Temperature (°C)", title=f"24-Hour Temperature Forecast for {city}")
            st.plotly_chart(fig_forecast, key=f"forecast_plot_{city}_{timestamp}")

    # Fetch historical weather data if date range is specified
    if start_date and end_date:
        historical_data_df = fetch_historical_weather(city, api_key, start_date, end_date)
        if historical_data_df is not None:
            st.subheader(f"Historical Weather Data for {city} ({start_date} to {end_date})")
            st.write(historical_data_df)
            st.line_chart(historical_data_df.set_index('Date')[['Temperature (°C)']])

    # Wait for the refresh interval before updating all cities
    time.sleep(refresh_interval)

# Download all historical data recorded during the session
if st.session_state.weather_history:
    st.subheader("Download All Recorded Weather Data")
    history_df = pd.DataFrame(st.session_state.weather_history)
    st.download_button(
        label="Download Full Weather History as CSV",
        data=history_df.to_csv(index=False),
        file_name=f'full_weather_history.csv',
        mime='text/csv',
        key="download_button_unique"
    )
else:
    st.warning("No data collected yet. Please wait until the data starts appearing.")
