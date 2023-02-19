# Temperature and Humidity Sensor DHT Monitoring Script

This project is a simple temperature monitor for the Raspberry Pi using the DHT11, DHT22 or AM2302 temperature and humidity sensors. The temperature and humidity data is logged to a SQLite database, and the script will print the time, temperature, and humidity to the screen if the temperature changes by any amount or the humidity changes by +-3%. Additionally, it prints the all-time high and low temperature values, as well as the daily high and low temperature values. The all-time high and low values are stored in a separate table in the database and are independent of the date. The daily high and low values are reset every day and are also stored in the database.

## Prerequisites

Raspberry Pi with GPIO pins
DHT11, DHT22 or AM2302 temperature and humidity sensor
Python 3
Adafruit_DHT library
Systemd (for running the script as a service)

## Installation

1. Connect a sensor to your Raspberry Pi or other device that supports GPIO pins.
2. Ensure that the sqlite3 library is installed. It should be included in most Python installations by default.

## Usage

1. Clone the repository: `git clone https://github.com/KaramanJoe/DHT-sensor-monitor.git`
2. Open a terminal and navigate to the directory where the script is located.
3. Install the required packages using pip with the following command: `sudo pip install -r requirements.txt`
4. Test the script by running the following command (replace sensor_type and pin_number with the appropriate values for your sensor and GPIO pin): `sudo python3 monitor.py <sensor_type> <pin_number>`. For example, if you are using a DHT11 sensor connected to GPIO pin 4, run the following command: `sudo python3 monitor.py 11 4`
5. Run the script by entering the following command: `python3 monitor.py`
6. The script will start reading the temperature and humidity from the sensor and storing it in the database.
7. If the temperature changes by any amount or the humidity changes by +-3%, the script will print the time, temperature, humidity, and a corresponding tag (ATH, ATL, DH, DL) indicating if it is the all-time high, all-time low, daily high, or daily low value.

## Running the script automatically on startup using systemd

If you want the script to run automatically on startup, you can use the systemd service file to do so: `temperature-monitor.service`

To use this file, copy it to `/etc/systemd/system/temperature-monitor.service`.

Reload the systemd configuration and enable the service:
`sudo systemctl daemon-reload`
`sudo systemctl enable temperature-monitor.service`

Start the service: `sudo systemctl start temperature-monitor.service`

Check the status of the service: `sudo systemctl status temperature-monitor.service`

Note that the paths and command line parameters in the `ExecStart` line may need to be adjusted depending on the location of the script, sensor type and GPIO pin.

## Acknowledgments

- This script was inspired by Adafruit's DHT11 Python library examples.
- The sqlite3 library documentation was helpful in understanding how to interact with a database using Python.