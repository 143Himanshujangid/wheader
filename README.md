# Weather Forecaster Streamlit App

This is a simple weather forecasting web app built with Streamlit, PyOWM, and Matplotlib. It allows users to:
- Enter a city name
- Select temperature unit (Celsius/Fahrenheit)
- View current weather, 5-day min/max temperature (bar/line graph), humidity, sunrise/sunset, and weather alerts

## Setup Instructions

1. **Clone the repository or copy the files to your project folder.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenWeatherMap API key:**
   - Edit `.streamlit/secrets.toml` and set:
     ```toml
     API_KEY = "5838cfe633915c04639d62384cdf614d"
     ```
4. **Run the app:**
   ```bash
   streamlit run weather_app.py
   ```

## Usage
- Enter the city name (for best results: `city, country_code`, e.g., `London, GB`)
- Select temperature unit and graph type
- Click **Show Weather**

## Features
- Current weather with icon
- 5-day min/max temperature (bar/line graph)
- Humidity forecast
- Sunrise and sunset times
- Weather alerts (rain, snow, storm, etc.)

---
Made with ❤️ using Streamlit and PyOWM 