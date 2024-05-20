# In the annals of time, there existed a breed of individuals who wore their geekdom and nerdiness 
# like badges of honor. They were the renegades, the visionaries, the ones who dared to dance to the
# beat of their own algorithm. They didn't just write code; they sculpted it with passion, 
# fueled by the thrill of conquest and the joy of creation. 
# Through sleepless nights and endless lines of code, they pursued the elusive specter of possibility,
# unyielding in their quest to conquer the impossible and redefine the boundaries 
# of what was deemed plausible.

# These were the misfits, the rebels, the troublemakers—the square pegs in a world of round holes.
# Rules were mere suggestions to them, and the status quo was nothing but a challenge 
# waiting to be dismantled. You could try to ignore them, but their impact was undeniable. 
# They were the catalysts of change, the architects of progress. 
# While some dismissed them as eccentric or erratic, we recognized their brilliance. 
# For it is often the ones deemed crazy enough to believe they can change the world who are precisely 
# the ones capable of doing so.

# António Cunha Santos AKA SleepDeprivedLoon 08/03/2024 
# In Memorium Deolinda Oliveira dos Santos 1956-2023 (Quem nasce lagartixa nunca chega a jacaré)

import serial
import requests
import csv
import time
from datetime import datetime
from tabulate import tabulate

# Serial port configuration for Arduino and data logging
serial_port = 'COM7'  # Replace with the appropriate serial port
baud_rate = 9600

# Wunderground API settings
wunderground_station_id = "IPVOAD5"
wunderground_api_key = "a99d276be0384c889d276be0386c8848"
wunderground_url = f"https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

# PWSWeather API settings
pwsweather_station_id = 'ROBOTICAEAVEROMAR'
pwsweather_password = '7df56fe4398995e8049a9ab6215983fe'


# Open CSV file for writing
csv_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure', 'Wind Speed (m/s)', 'Wind Gust (m/s)', 'Dew Point (C)', 'Sensor WorkingTime (H)', 'Rainfall (mm)', '1 Hour Rainfall (mm)', 'Raw Rainfall'])

# Initialize serial communication
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def read_sensor_data():
    temperature = None
    humidity = None
    pressure = None
    wind_speed = None
    wind_gust = None
    dew_point = None
    sensor_working_time = None
    rainfall = None
    hour_rainfall = None
    raw_rainfall = None
    
    while True:
        line = ser.readline().decode().strip()
        if line.startswith("Temperature"):
            temperature = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Humidity"):
            humidity = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Pressure"):
            pressure = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("WindSpeed"):
            wind_speed = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("WindGust"):
            wind_gust = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("DewPoint"):
            dew_point = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Sensor WorkingTime"):
            sensor_working_time = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Rainfall"):
            rainfall = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("1 Hour Rainfall"):
            hour_rainfall = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("rainfall raw"):
            raw_rainfall = float(line.split(":")[1].strip().split()[0])
        
        # Check if all variables are set
        if all(x is not None for x in [temperature, humidity, pressure, wind_speed, wind_gust, dew_point, sensor_working_time, rainfall, hour_rainfall, raw_rainfall]):
            return temperature, humidity, pressure, wind_speed, wind_gust, dew_point, sensor_working_time, rainfall, hour_rainfall, raw_rainfall


def transmit_data_wunderground(temperature, humidity, pressure, wind_speed, wind_gust, dew_point):
    payload = {
        "ID": wunderground_station_id,
        "PASSWORD": "jJbvmEnA",
        "dateutc": "now",
        "tempf": temperature * 1.8 + 32,  # Convert Celsius to Fahrenheit
        "humidity": humidity,
        "baromin": pressure * 0.0295300,  # Convert hpa to inHg
        "windspeedmph": abs(wind_speed * 0.6213711922),  # Convert m/s to mph
        "windspeedkmh": wind_speed,
        "windgustmph": abs(wind_gust * 0.6213711922),
        "dewptf": dew_point * 1.8 + 32,  # Convert Celsius to Fahrenheit for dew point
    }

    response = requests.post(wunderground_url, data=payload)
    if response.status_code == 200:
        print("PWS Data transmitted to Wunderground successfully.")
    else:
        print("Failed to transmit data to Wunderground.")

def transmit_data_pwsweather(temperature, humidity, pressure, wind_speed, wind_gust, dew_point, hour_rainfall):
    station_id = pwsweather_station_id
    api_key = pwsweather_password
    temp_f = temperature * 1.8 + 32
    humidity = humidity
    baro_min = pressure * 0.0295300
    wind_speed_mph = abs(wind_speed * 0.6213711922)
    wind_gust_mph = abs(wind_gust * 0.6213711922)
    dewpt_f = dew_point * 1.8 + 32
    rain_in = hour_rainfall * 0.0393701
    date_utc = datetime.utcnow().strftime('%Y-%m-%d+%H:%M:%S')  # Format UTC time

    # Construct the URL
    url = f"https://pwsupdate.pwsweather.com/api/v1/submitwx?ID={station_id}&PASSWORD={api_key}&dateutc={date_utc}&windspeedmph={wind_speed_mph}&windgustmph={wind_gust_mph}&tempf={temp_f}&humidity={humidity}&baromin={baro_min}&dewptf={dewpt_f}&rainin={rain_in}&softwaretype=ChatGPT&action=updateraw"

    # Send GET request to submit weather data
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        print("Weather data submitted successfully.")
    else:
        print(f"Failed to submit weather data. Status code: {response.status_code}")

try:
    while True:
        try:
            # Read sensor data
            sensor_data = read_sensor_data()
            temperature, humidity, pressure, wind_speed, wind_gust, dew_point, sensor_working_time, rainfall, hour_rainfall, raw_rainfall = sensor_data

            # Transmit data to weather APIs
            transmit_data_wunderground(temperature, humidity, pressure, wind_speed, wind_gust, dew_point)
            transmit_data_pwsweather(temperature, humidity, pressure, wind_speed, wind_gust, dew_point, hour_rainfall)

            # Write data to CSV file
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([timestamp, temperature, humidity, pressure, wind_speed, wind_gust, dew_point, sensor_working_time, rainfall, hour_rainfall, raw_rainfall])
            print("Data written to CSV file.")

            # Display data in table format
            print(tabulate([[timestamp, temperature, humidity, pressure, wind_speed, wind_gust, dew_point, sensor_working_time, rainfall, hour_rainfall, raw_rainfall]], headers=['Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure', 'Wind Speed (m/s)', 'Wind Gust (m/s)', 'Dew Point (C)', 'Sensor WorkingTime (H)', 'Rainfall (mm)', '1 Hour Rainfall (mm)', 'Raw Rainfall']))
            print("\n")

            time.sleep(30)  # Delay for 30 seconds between updates

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Restarting...")
            time.sleep(5)  # Delay before restarting
            continue

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    # Close serial port and CSV file
    ser.close()
    csv_file.close()
    print("Serial port and CSV file closed.")