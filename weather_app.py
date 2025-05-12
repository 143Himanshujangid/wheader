import streamlit as st
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates
import pyowm

# Fetch API key from Streamlit secrets
device_api_key = st.secrets["API_KEY"]
owm = pyowm.OWM(device_api_key)
mgr = owm.weather_manager()
sign = u"\N{DEGREE SIGN}"

st.title("Weather Forecaster")
st.write("## Enter the city name, choose a temperature unit, and select a graph type:")

location = st.text_input("City Name:", "")
units = st.selectbox("Temperature Unit:", ("celsius", "fahrenheit"))
graph = st.selectbox("Graph Type:", ("Bar Graph", "Line Graph"))

degree = "C" if units == "celsius" else "F"

def get_temperature():
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast
    days, dates_list, temp_min, temp_max = [], [], [], []
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_list:
            dates_list.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temp = weather.temperature(unit=units)['temp']
        if temp_min[-1] is None or temp < temp_min[-1]:
            temp_min[-1] = temp
        if temp_max[-1] is None or temp > temp_max[-1]:
            temp_max[-1] = temp
    return days, temp_min, temp_max

def plot_temperature_bar():
    days, temp_min, temp_max = get_temperature()
    days_num = dates.date2num(days)
    plt.style.use('ggplot')
    plt.figure(figsize=(7,4))
    plt.xlabel('Day')
    plt.ylabel(f'Temperature ({sign}{degree})')
    plt.title('5-Day Min/Max Temperature')
    plt.bar(days_num-0.2, temp_min, width=0.4, color='#42bff4', label='Min')
    plt.bar(days_num+0.2, temp_max, width=0.4, color='#ff5349', label='Max')
    plt.xticks(days_num)
    axes = plt.gca()
    axes.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
    plt.legend()
    st.pyplot(plt)

def plot_temperature_line():
    days, temp_min, temp_max = get_temperature()
    days_num = dates.date2num(days)
    plt.style.use('ggplot')
    plt.figure(figsize=(7,4))
    plt.xlabel('Day')
    plt.ylabel(f'Temperature ({sign}{degree})')
    plt.title('5-Day Min/Max Temperature')
    plt.plot(days_num, temp_min, marker='o', color='#42bff4', label='Min')
    plt.plot(days_num, temp_max, marker='o', color='#ff5349', label='Max')
    plt.xticks(days_num)
    axes = plt.gca()
    axes.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
    plt.legend()
    st.pyplot(plt)

def show_current_weather():
    obs = mgr.weather_at_place(location)
    weather = obs.weather
    icon = weather.weather_icon_url(size='4x')
    temp = weather.temperature(unit=units)['temp']
    temp_felt = weather.temperature(unit=units)['feels_like']
    st.image(icon, caption=weather.detailed_status.title())
    st.markdown(f"## 🌡️ Temperature: **{round(temp)}{sign}{degree}**")
    st.write(f"### Feels Like: {round(temp_felt)}{sign}{degree}")
    st.write(f"### ☁️ Clouds: {weather.clouds}%")
    st.write(f"### 💨 Wind: {weather.wind()['speed']} m/s")
    st.write(f"### 💧 Humidity: {weather.humidity}%")
    st.write(f"### ⏲️ Pressure: {weather.pressure['press']} mBar")
    st.write(f"### 🛣️ Visibility: {weather.visibility(unit='kilometers')} km")

def show_sunrise_sunset():
    obs = mgr.weather_at_place(location)
    weather = obs.weather
    sunrise = datetime.utcfromtimestamp(weather.sunrise_time())
    sunset = datetime.utcfromtimestamp(weather.sunset_time())
    st.write(f"#### 🌅 Sunrise: {sunrise.date()} {sunrise.time()}")
    st.write(f"#### 🌇 Sunset: {sunset.date()} {sunset.time()}")

def show_weather_alerts():
    forecaster = mgr.forecast_at_place(location, '3h')
    st.write("### Upcoming Weather Alerts:")
    alerts = []
    if forecaster.will_have_clouds(): alerts.append("Clouds ⛅")
    if forecaster.will_have_rain(): alerts.append("Rain 🌧️")
    if forecaster.will_have_snow(): alerts.append("Snow ❄️")
    if forecaster.will_have_hurricane(): alerts.append("Hurricane 🌀")
    if forecaster.will_have_tornado(): alerts.append("Tornado 🌪️")
    if forecaster.will_have_fog(): alerts.append("Fog 🌫️")
    if forecaster.will_have_storm(): alerts.append("Storm 🌩️")
    if alerts:
        for alert in alerts:
            st.write(f"- {alert}")
    else:
        st.write("No upcoming alerts!")

def get_humidity():
    days, dates_list, humidity_max = [], [], []
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_list:
            dates_list.append(date)
            humidity_max.append(None)
            days.append(date)
        humidity = weather.humidity
        if humidity_max[-1] is None or humidity > humidity_max[-1]:
            humidity_max[-1] = humidity
    return days, humidity_max

def plot_humidity():
    days, humidity = get_humidity()
    days_num = dates.date2num(days)
    plt.style.use('ggplot')
    plt.figure(figsize=(7,4))
    plt.xlabel('Day')
    plt.ylabel('Humidity (%)')
    plt.title('5-Day Humidity Forecast')
    plt.bar(days_num, humidity, color='#42bff4')
    plt.xticks(days_num)
    axes = plt.gca()
    axes.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
    st.pyplot(plt)

if st.button('Show Weather'):
    if not location:
        st.warning('Please enter a city name!')
    else:
        try:
            show_current_weather()
            if graph == 'Bar Graph':
                plot_temperature_bar()
            else:
                plot_temperature_line()
            show_weather_alerts()
            show_sunrise_sunset()
            plot_humidity()
        except Exception as e:
            st.error(f"Error: {e}\nTry entering city as 'city, country_code' (e.g., London, GB)") 