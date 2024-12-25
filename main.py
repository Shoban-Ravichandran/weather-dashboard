import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import io
import folium
from folium import plugins
from io import BytesIO
from streamlit_folium import folium_static
from datetime import timedelta 

# Load environment variables (ensure .env file is correctly set up)
api_key = os.getenv("OPENWEATHER_API_KEY")

# Function to convert UTC time to local time using timezone offset
def convert_to_local_time(utc_time, timezone_offset):
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

# Cache the weather data to improve performance
@st.cache_data
def fetch_weather_for_all_cities(cities, api_key, units="metric", lang="en"):
    weather_data_list = []
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            timezone_offset = data['timezone']
            utc_time = datetime.utcfromtimestamp(data['dt'])
            local_time = convert_to_local_time(utc_time, timezone_offset)
            weather_info = {
                'City': data['name'],
                'Temperature (°C)' if units == "metric" else 'Temperature (°F)': data['main']['temp'],
                'Feels Like (°C)' if units == "metric" else 'Feels Like (°F)': data['main']['feels_like'],
                'Humidity (%)': data['main']['humidity'],
                'Wind Speed (m/s)' if units == "metric" else 'Wind Speed (mph)': data['wind']['speed'],
                'Visibility (m)': data.get('visibility', 'N/A'),
                'Pressure (hPa)': data['main']['pressure'],
                'Weather': data['weather'][0]['description'],
                'Time': local_time,  # Local time for the city
                'Sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'Sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
                'Latitude': data['coord']['lat'],
                'Longitude': data['coord']['lon']
            }
            weather_data_list.append(weather_info)
        else:
            st.error(f"Failed to fetch data for {city}. Check the city name or API key.")
    
    return pd.DataFrame(weather_data_list) if weather_data_list else pd.DataFrame()

# Streamlit App Layout
st.title("Live Weather Dashboard For Cities around the globe 🌤️")

# Sidebar elements
units = st.sidebar.selectbox("Select Units:", ["Metric (°C, m/s)", "Imperial (°F, mph)"])
units_code = "metric" if "Metric" in units else "imperial"

language = st.sidebar.selectbox("Select Language:", ["en", "es", "fr", "de", "it", "ru", "zh", "ar"])
st.sidebar.write(f"Language selected: {language.upper()}")

# Dropdown for city selection
available_cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose","Jacksonville",  # USA
    "London", "Birmingham", "Manchester", "Leeds", "Glasgow", "Liverpool", "Edinburgh", "Bristol", "Sheffield", "Leicester","Cambridge",  # UK
    "Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad","Ahmedabad", "Pune", "Surat", "Jaipur", "Lucknow", "Kanpur","Nagpur", "Indore", "Patna", "Vadodara", "Ghaziabad", "Ludhiana","Agra", "Nashik", "Faridabad", "Meerut", "Bhopal", "Coimbatore","Kochi", "Vijayawada", "Madurai", "Chandigarh", "Mysore", "Visakhapatnam","Rajkot", "Shivamogga", "Gurugram",#India
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
    "Dubai", "Abu Dhabi", "Sharjah", "Ajman","Fujairah", "Umm Al-Quwain", "Al Ain", "Khalifa City",  # UAE
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
    "Dublin", "Cork", "Limerick", "Galway", "Waterford", "Kilkenny","Derry", "Belfast", "Sligo", "Tralee", "Ennis", "Letterkenny","Wexford", "Killarney", "Athlone", "Cavan", "Clonmel", "Armagh","Carrickfergus", "Newry", "Tullamore", "Bray", "Navan", "Drogheda"# Ireland
]

# Initialize session state for cities and weather data if not already set
if "cities" not in st.session_state:
    st.session_state.cities = ["Chennai", "Kochi"]  # Default cities if not set
if "weather_data" not in st.session_state:
    st.session_state.weather_data = pd.DataFrame()  # Placeholder for weather data
# Allow user to select cities, using session state to store the cities
cities = st.multiselect("Select cities for weather data:", available_cities, default=st.session_state.cities)
st.session_state.cities = available_cities
# Select Cities with 'Select All' button
if st.button("Select All Cities"):
    st.session_state.cities = available_cities
# Prompt for API Key input
api_key_input = st.text_input("Enter your OpenWeatherMap API Key:", type="password")

# If the API key is not entered, provide a link to get one
if not api_key_input:
    st.caption("Don't have an API Key? You can get one for free from OpenWeatherMap [here](https://openweathermap.org/api).")
    st.caption("If you still face issues generating your API Key please refer to this [youtube tutorial](https://www.youtube.com/watch?v=Czdg9RhoI_I)")
    st.caption("Note: Make sure to use the auto generated closed captions for better understanding.")
if api_key_input:
    st.session_state.api_key = api_key_input

if st.button("Fetch Weather Data") and api_key_input:
    api_key_to_use = st.session_state.get("api_key", None)
    
    if api_key_to_use:
        # Fetch the weather data only if not already fetched
        if st.session_state.weather_data.empty:
            st.session_state.weather_data = fetch_weather_for_all_cities(cities, api_key_to_use, units_code, language)
            if st.session_state.weather_data.empty:
                st.error("No weather data fetched. Please try again.")
            else:
                st.success(f"Fetched weather data for {len(st.session_state.weather_data)} cities.")
        else:
            st.warning("Weather data is already fetched. Please refresh the page")

# Ensure weather data is available before processing
weather_data = st.session_state.weather_data

if not weather_data.empty:
    st.subheader("Weather Data for Selected Cities")
    st.write(weather_data)

    # Export Options
    csv = weather_data.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="weather_data.csv", mime="text/csv")

    json_data = weather_data.to_json(orient="records")
    st.download_button("Download JSON", data=json_data, file_name="weather_data.json", mime="application/json")

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        weather_data.to_excel(writer, index=False, sheet_name='Weather Data')
    excel_buffer.seek(0)
    st.download_button("Download Excel", data=excel_buffer, file_name="weather_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Comparison Plot (User selects cities)
    if len(cities) > 1:
        st.subheader("Compare Weather Data")

        comparison_cities = st.multiselect(
            "Select cities to compare:",
            options=cities,
            default=cities[:5],  # Default to all cities
        )
        if len(comparison_cities)==0:
            st.write("No cities selected.")
        # Allow user to choose which metrics to compare
        metrics_to_compare = st.multiselect(
            "Select Metrics to Compare", 
            ['Temperature (°C)', 'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)'], 
            default=['Temperature (°C)', 'Humidity (%)', 'Pressure (hPa)']
        )

        # Filter weather data for selected cities
        comparison_data = weather_data[weather_data['City'].isin(comparison_cities)]
        if len(metrics_to_compare)==0:
            st.write("No metrics selected.")
        if not comparison_data.empty:
            fig = go.Figure()

            # Add traces for the selected metrics
            for col in metrics_to_compare:
                if col in comparison_data.columns:
                    fig.add_trace(go.Bar(
                        name=col, 
                        x=comparison_data['City'], 
                        y=comparison_data[col],
                        hovertemplate='%{x}: %{y}<extra></extra>',  # Show city and value on hover
                    ))
            fig.update_layout(
                barmode='group',
                title="Weather Comparison for Selected Cities",
                xaxis_title="City",
                yaxis_title="Value",
                template="plotly_dark"  # Add a dark theme for better visibility
            )
            st.plotly_chart(fig)
        

    # Dynamic Insights
    st.subheader("Dynamic Weather Insights")

    # Top 5 Hottest and Coldest Cities
    top_5_hot = weather_data.nlargest(5, 'Temperature (°C)')
    top_5_cold = weather_data.nsmallest(5, 'Temperature (°C)')

    st.write("Top 5 Hottest Cities:")
    st.write(top_5_hot[['City', 'Temperature (°C)']])

    st.write("Top 5 Coldest Cities:")
    st.write(top_5_cold[['City', 'Temperature (°C)']])

    # Average Temperature and Humidity
    avg_temp = weather_data['Temperature (°C)'].mean()
    avg_humidity = weather_data['Humidity (%)'].mean()

    st.write(f"Average Temperature: {avg_temp:.2f}°C")
    st.write(f"Average Humidity: {avg_humidity:.2f}%")

    # Significant Weather Events (e.g., storms, rain)
    significant_weather = weather_data[weather_data['Weather'].str.contains("storm|rain|snow", case=False, na=False)]
    st.write("Cities with Significant Weather Events:")
    st.write(significant_weather[['City', 'Weather']])

    # Map to display weather insights
    st.subheader("Weather on Map")
    weather_map = folium.Map(location=[weather_data['Latitude'].mean(), weather_data['Longitude'].mean()], zoom_start=5)

    # Add markers for each city
    for _, row in weather_data.iterrows():
        color = 'green'  # Default color for clear weather
        if 'rain' in row['Weather'].lower():
            color = 'blue'
        elif 'storm' in row['Weather'].lower():
            color = 'red'
        elif row['Temperature (°C)'] > 30:
            color = 'orange'
        elif row['Temperature (°C)'] < 10:
            color = 'purple'

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=(f"<b>{row['City']}</b><br>"
                f"Temperature: {row['Temperature (°C)']}°C<br>"
                f"Weather: {row['Weather']}<br>"
                f"Humidity: {row['Humidity (%)']}%<br>"
                f"Wind Speed: {row['Wind Speed (m/s)']} m/s"),
            icon=folium.Icon(color=color)
        ).add_to(weather_map)

    # Create a custom HTML legend for the map
    legend_html = '''
    <div style="position: bottom; 
                bottom: 50px; left: 10px; 
                width: 150px; height: 170px; 
                background-color: opaque; 
                border: 2px solid gray; 
                z-index: 9999; 
                font-size: 14px;
                padding: 10px; 
                box-shadow: 2px 2px 5px rgba(0,0,0,0.5);">
        <b>Weather Legend</b><br>
        <i style="background-color: green; width: 20px; height: 20px; display: inline-block;"></i> Clear Weather<br>
        <i style="background-color: blue; width: 20px; height: 20px; display: inline-block;"></i> Rain<br>
        <i style="background-color: red; width: 20px; height: 20px; display: inline-block;"></i> Storm<br>
        <i style="background-color: orange; width: 20px; height: 20px; display: inline-block;"></i> Hot (> 30°C)<br>
        <i style="background-color: purple; width: 20px; height: 20px; display: inline-block;"></i> Cold (< 10°C)
    </div>
    '''

    # Add the legend to the map
    folium.Marker(
        location=[weather_data['Latitude'].mean(), weather_data['Longitude'].mean()],
        icon=folium.DivIcon(html=legend_html)
    ).add_to(weather_map)
    # Display the map in the app
    folium_static(weather_map)
    # Display Time Column for Selected Cities
    if not weather_data.empty:
        # Check if the DataFrame is not empty
        if not weather_data.empty:
            st.write("Local Time for Selected Cities:")
            
            # Multiselect widget for city selection with session state
            selected_cities = st.multiselect(
                "Select cities to display time:",
                options=weather_data['City'].tolist(),
                default=cities[:2]
            )
            
            # Update session state when selection changes
            st.session_state.selected_cities = selected_cities

            # Filter the DataFrame based on selected cities
            if selected_cities:
                filtered_data = weather_data[weather_data['City'].isin(selected_cities)]
                filtered_data['Time'] = pd.to_datetime(filtered_data['Time'], errors='coerce')
                if pd.api.types.is_datetime64_any_dtype(filtered_data['Time']):
                            filtered_data['Formatted Time'] = filtered_data['Time'].dt.strftime('%H:%M , %A')
                else:
                    st.write("Time column is not in a datetime format. Please check the data.")                
                filtered_data = filtered_data[['City','Formatted Time']]
                st.write(filtered_data)
            else:
                st.write("No cities selected.")
else:
    st.warning("Please fetch weather data first.")


# Footer
st.markdown("---")
st.caption("Built with 💪 by Shoban Ravichandran")
st.caption("Feel free to drop in your comments and feedbacks at connectshoban@gmail.com")
