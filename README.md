# Live Weather Dashboard

A live weather dashboard built using Streamlit, OpenWeather API, and Plotly to provide weather information for cities around the globe. The app fetches real-time weather data, compares metrics for selected cities, and displays insights with visualizations and maps.

## Features

- **Weather Data**: Fetches real-time weather data such as temperature, humidity, wind speed, and weather description for selected cities.
- **Units and Language Selection**: Choose between Metric (°C, m/s) or Imperial (°F, mph) units. Supports multiple languages for weather data.
- **City Selection**: Select cities for weather data using a multi-select dropdown.
- **Weather Data Comparison**: Compare weather metrics (temperature, humidity, pressure, and wind speed) across selected cities.
- **Dynamic Insights**: Display insights such as top 5 hottest/coldest cities, average temperature and humidity, and cities with significant weather events.
- **Weather Map**: Visualize weather data for cities on an interactive map with customized weather icons.
- **Time Information**: View the local time for selected cities.
- **Export Options**: Download weather data in CSV, JSON, or Excel formats.

## Installation

1. Clone the repository:
  ```bash
   git clone https://github.com/Shoban-Ravichandran/weather-dashboard.git
  ```
2. Install the required dependencies:

  ```bash
  pip install -r requirements.txt
  ```
3. Obtain an API key from OpenWeatherMap.

4. Create a .env file in the root directory and add your OpenWeather API key:

  ```makefile
  OPENWEATHER_API_KEY=your_api_key_here
  ```
## Usage
1. Run the Streamlit app:

  ```bash
  streamlit run app.py
  ```
2. Enter your OpenWeather API key in the app or set it in the .env file.

3. Select cities, units, and language from the sidebar to customize your dashboard.

4. Click Fetch Weather Data to load the weather information.

5. View and compare weather metrics, download data, and explore insights on the map.

## File Structure
  ```bash
  /live-weather-dashboard
  │
  ├── app.py                    # Main Streamlit application file
  ├── requirements.txt           # List of Python dependencies
  ├── .env                       # Environment variables (API keys)
  └── README.md                  # Documentation
  ```
## Libraries Used

- Streamlit: Framework for building the web app.
- Requests: For making API requests to OpenWeatherMap.
- Pandas: Data manipulation and storage.
- Plotly: For interactive weather data visualizations.
- Folium: For rendering interactive maps with weather data.
- XlsxWriter: For exporting weather data to Excel.
- dotenv: For loading environment variables from the .env file.

## App Layout
### Sidebar:
1. Units: Choose between Metric (°C, m/s) or Imperial (°F, mph).
2. Language: Select a language for weather data (e.g., English, Spanish, French).

### Main Area:
1. City Selection: Select cities to fetch weather data for. You can select multiple cities or use the "Select All Cities" button.
2. API Key Input: Enter your OpenWeather API key.
3. Weather Data: Displayed in a table with details such as temperature, humidity, and weather conditions.
4. Download Buttons: Options to download the weather data in CSV, JSON, or Excel format.
5. Comparison Plot: Visualize a comparison of selected metrics for the cities.
6. Weather Insights: Display dynamic insights such as top hottest/coldest cities, average temperature, and humidity.
7. Weather Map: Interactive map showing cities and weather conditions with color-coded markers.
8. Time Information: Display the local time for selected cities.

## Contributing
Feel free to fork the repository, make improvements, or report issues. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Submit a pull request.

## Acknowledgements
- [OpenWeatherMap API](https://openweathermap.org/api) for providing real-time weather data.
- [Streamlit](https://streamlit.io/) for building the interactive web app.
- [Plotly](https://pypi.org/project/plotly/) for creating the interactive charts.
- [Folium](https://pypi.org/project/folium/) for generating interactive maps.

## Contact

If you have any questions, feel free to reach out via email or open an issue in the repository.

Email: connectshoban@gmail.com
