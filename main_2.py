import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import time
import random

# List of available cities (top 1000 cities for demonstration purposes)
available_cities = [
    "Dublin",
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
def fetch_weather_for_all_cities(cities, api_key):
    weather_data_list = []
    for city in cities:
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
            weather_data_list.append(weather_info)
        else:
            st.error(f"Failed to fetch data for {city}. Check the city name or API key.")
    
    return pd.DataFrame(weather_data_list)

# Streamlit App Layout
st.title("Live Weather Dashboard 🌤️")

# Initialize cities in session state
if 'cities' not in st.session_state:
    st.session_state.cities = []

# Dropdown for city selection (User can select multiple cities)
cities = st.multiselect("Select cities for weather data:", available_cities, default=["Dublin", "Paris"])

# Button to select all cities
if st.button('Select All Cities'):
    st.session_state.cities = available_cities  # Save all cities to session state

# Update cities list if modified
cities = st.session_state.cities if st.session_state.cities else cities

# Input for API Key
api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key:", type="password")

# Button to fetch all data at once
if st.button("Fetch All Weather Data"):
    if api_key:
        # Fetch weather data for all selected cities
        weather_data = fetch_weather_for_all_cities(cities, api_key)
        
        # Display the fetched data in a table
        st.subheader("Weather Data for Selected Cities")
        st.write(weather_data)

        # Plot the data using Plotly for each city
        for city in cities:
            city_data = weather_data[weather_data['City'] == city]
            fig = px.bar(city_data, x='City', y=['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Pressure (hPa)'],
                         title=f"Weather Metrics for {city}")
            st.plotly_chart(fig)

        # Provide a download button for the data
        csv = weather_data.to_csv(index=False)
        st.download_button(
            label="Download Weather Data as CSV",
            data=csv,
            file_name="weather_data.csv",
            mime="text/csv"
        )
    else:
        st.error("Please enter a valid API key.")

