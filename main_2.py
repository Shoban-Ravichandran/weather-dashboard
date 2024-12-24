import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import time

# List of available cities (top 1000 cities for demonstration purposes)
available_cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",  # USA
    "London", "Birmingham", "Manchester", "Leeds", "Glasgow", "Liverpool", "Edinburgh", "Bristol", "Sheffield", "Leicester",  # UK
    "Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Surat",  # India
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille",  # France
    "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Dusseldorf", "Dortmund", "Essen", "Bremen",  # Germany
    "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Quebec City", "Winnipeg", "Hamilton", "Kitchener",  # Canada
    "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart", "Darwin", "Cairns", "Gold Coast", "Newcastle",  # Australia
    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Tianjin", "Chongqing", "Hong Kong", "Chengdu", "Hangzhou", "Wuhan",  # China
    "Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kawasaki", "Sendai", "Chiba",  # Japan
    "Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod", "Samara", "Omsk", "Kazan", "Chelyabinsk", "Rostov-on-Don",  # Russia
    "Cairo", "Alexandria", "Giza", "Shubra El-Kheima", "Port Said", "Suez", "Mansoura", "Tanta", "Aswan", "Zagazig",  # Egypt
    "Rio de Janeiro", "Sao Paulo", "Brasilia", "Salvador", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",  # Brazil
    "Buenos Aires", "Cordoba", "Rosario", "Mendoza", "La Plata", "San Miguel de Tucuman", "Mar del Plata", "Salta", "Santa Fe", "San Juan",  # Argentina
    "Cape Town", "Johannesburg", "Durban", "Pretoria", "Port Elizabeth", "Bloemfontein", "East London", "Polokwane", "Nelspruit", "Kimberley",  # South Africa
    "Mexico City", "Guadalajara", "Monterrey", "Cancun", "Puebla", "Tijuana", "Mérida", "Chihuahua", "Leon", "Zapopan",  # Mexico
    "Lagos", "Abuja", "Kano", "Ibadan", "Benin City", "Port Harcourt", "Kaduna", "Zaria", "Jos", "Maiduguri",  # Nigeria
    "Istanbul", "Ankara", "Izmir", "Bursa", "Adana", "Gaziantep", "Konya", "Antalya", "Mersin", "Kayseri",  # Turkey
    "Kuala Lumpur", "Singapore", "Jakarta", "Bangkok", "Manila", "Hanoi", "Ho Chi Minh City", "Yangon", "Seoul", "Taipei",  # Southeast Asia
    "Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Gyeongju", "Suwon", "Jeonju",  # South Korea
    "Lagos", "Abuja", "Kano", "Ibadan", "Benin City", "Port Harcourt", "Kaduna", "Zaria", "Jos", "Maiduguri",  # Nigeria
    "Singapore", "Manila", "Kuala Lumpur", "Jakarta", "Bangkok", "Ho Chi Minh City", "Hanoi", "Taipei", "Seoul", "Yangon",  # Southeast Asia
    "Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al-Quwain", "Al Ain", "Khalifa City", "Dubai Silicon Oasis",  # UAE
    "Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa", "Volos", "Ioannina", "Chania", "Rhodes", "Kavala",  # Greece
    "Seville", "Barcelona", "Madrid", "Valencia", "Malaga", "Zaragoza", "Murcia", "Palma", "Las Palmas de Gran Canaria", "Bilbao",  # Spain
    "Milan", "Rome", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Catania",  # Italy
    "Kiev", "Kharkiv", "Odessa", "Dnipro", "Lviv", "Zaporizhzhia", "Kherson", "Mykolaiv", "Mariupol", "Vinnytsia",  # Ukraine
    "Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Piura", "Iquitos", "Tacna", "Chimbote", "Pucallpa",  # Peru
    "Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena", "Cucuta", "Bucaramanga", "Santa Marta", "Manizales", "Pereira",  # Colombia
    "Quito", "Guayaquil", "Cuenca", "Ambato", "Machala", "Loja", "Portoviejo", "Manta", "Riobamba", "Esmeraldas",  # Ecuador
    "Santiago", "Valparaiso", "Concepcion", "La Serena", "Antofagasta", "Temuco", "Rancagua", "Talca", "Arica", "Iquique",  # Chile
    "Asunción", "Ciudad del Este", "San Lorenzo", "Lambaré", "Encarnación", "Pedro Juan Caballero", "Caaguazu", "Coronel Oviedo", "Concepción", "Luque",  # Paraguay
    "Montevideo", "Salto", "Paysandu", "Maldonado", "Canelones", "Tacuarembo", "Durazno", "San José de Mayo", "Rivera", "Artigas",  # Uruguay
    "Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Maracay", "Maturín", "San Cristobal", "Puerto La Cruz", "Ciudad Guayana", "San Fernando de Apure",  # Venezuela
    "La Paz", "Santa Cruz", "Cochabamba", "Oruro", "Sucre", "Tarija", "Potosi", "El Alto", "Pando", "Beni",  # Bolivia
    "Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Kaduna", "Benin City", "Maiduguri", "Zaria", "Jos",  # Nigeria
]

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

# Streamlit App Layout
st.title("Live Weather Dashboard 🌤️")

# Dropdown for city selection (User can select multiple cities)
cities = st.multiselect("Select cities for weather data:", available_cities, default=["Dublin", "Paris"])

# Add "Select All" Button to select all cities
if st.button('Select All Cities'):
    cities = available_cities

# Input for API Key and Refresh Interval
api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key:", type="password")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds):", 10, 300, 30)

# Initialize session state to store historical weather data
if "weather_history" not in st.session_state:
    st.session_state.weather_history = []

# Placeholder for live updates for multiple cities
while True:
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

    # Wait for the refresh interval before updating all cities
    time.sleep(refresh_interval)

# Download all recorded data during the session
if st.session_state.weather_history:
    st.subheader("Download All Recorded Weather Data")
    history_df = pd.DataFrame(st.session_state.weather_history)
    
    # Fix download button issue and ensure file download
    st.download_button(
        label="Download Full Weather History as CSV",
        data=history_df.to_csv(index=False),
        file_name=f'full_weather_history.csv',
        mime='text/csv',
        key="download_button"
    )
