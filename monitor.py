import sqlite3
import time
from datetime import date
import sys
import Adafruit_DHT

# Parse command line parameters.
sensor_args = {
    "11": Adafruit_DHT.DHT11,
    "22": Adafruit_DHT.DHT22,
    "2302": Adafruit_DHT.AM2302,
}
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print("Usage: sudo ./monitor.py [11|22|2302] <GPIO pin number>")
    print(
        "Example: sudo ./monitor.py 2302 4 - Read from an AM2302 connected to GPIO pin #4"
    )
    sys.exit(1)

# Connect to the database and create the tables if they don't exist
conn = sqlite3.connect("temperature.db")
conn.execute("CREATE TABLE IF NOT EXISTS daily_data (daily_high REAL, daily_low REAL)")
conn.execute(
    "CREATE TABLE IF NOT EXISTS all_time_data (all_time_high REAL, all_time_low REAL)"
)
conn.commit()

# Retrieve the all-time high and low values from the database
cursor = conn.execute("SELECT * FROM all_time_data")
row = cursor.fetchone()
all_time_high, all_time_low = row if row else (-9999.0, 9999.0)
conn.execute(
    "INSERT INTO all_time_data (all_time_high, all_time_low) VALUES (?, ?)",
    (all_time_high, all_time_low),
)

# Retrieve the daily high and low values from the database
cursor = conn.execute("SELECT * FROM daily_data")
row = cursor.fetchone()
daily_high, daily_low = row if row else (-9999.0, 9999.0)
conn.execute(
    "INSERT INTO daily_data (daily_high, daily_low) VALUES (?, ?)",
    (daily_high, daily_low),
)

today = date.today()

# Initialize the previous temperature and humidity
prev_temperature = -9999.0
prev_humidity = -9999.0

while True:
    # Read the temperature and humidity from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # If the temperature or humidity is valid, print the values
    if humidity is not None and temperature is not None:
        current_date = time.strftime("%d-%m-%Y")
        current_time = time.strftime("%H:%M:%S")

        # Update the daily high and low temperatures
        if today != date.today():
            daily_high = temperature
            daily_low = temperature
            today = date.today()
            conn.execute(
                "UPDATE daily_data SET daily_high=?, daily_low=",
                (daily_high, daily_low),
            )
            conn.commit()

        # Update the all-time high and low temperatures
        if temperature > all_time_high or temperature < all_time_low:
            all_time_high = max(temperature, all_time_high)
            all_time_low = min(temperature, all_time_low)
            conn.execute(
                "UPDATE all_time_data SET all_time_high=?, all_time_low=?",
                (all_time_high, all_time_low),
            )
            conn.commit()

        # Update the daily high and low temperatures
        if temperature > daily_high or temperature < daily_low:
            daily_high = max(daily_high, temperature)
            daily_low = min(daily_low, temperature)
            conn.execute(
                "UPDATE daily_data SET daily_high=?, daily_low=?",
                (daily_high, daily_low),
            )

            conn.commit()

        # Check if the temperature has changed by any amount or the humidity has changed by +-3%
        if prev_temperature != temperature or abs(prev_humidity - humidity) >= 3.0:
            # Print the time, temperature, and humidity to the screen
            print(
                f"[{current_time}] Temperature: {temperature} Humidity: {humidity} [DH {daily_high} / DL {daily_low}] [ATH {all_time_high} / ATL {all_time_low}]"
            )

        # Update the previous temperature and humidity
        prev_temperature = temperature
        prev_humidity = humidity

    # Wait for 10 seconds before reading the sensor again
    time.sleep(10)

# Close the database connection
conn.close()
