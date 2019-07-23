# Sense Dashboard
This simple PyQT5 desktop app show realtime data plotting from Raspberry Pi 3 and Arduino Uno via serial port.

# Screenshots
![Screenshot1](https://github.com/satujamsaja/pyqt5/raw/master/sensehat/httpapi.png?raw=true)
![Screenshot2](https://github.com/satujamsaja/pyqt5/raw/master/sensehat/serialport.png?raw=true)

# Requirements
* PyQT5
* pyqtgraph
* requests
* pyserial
* flask

# Sense API (senseapp/)
Simple Flask app that act as API for the dashboard.

# Arduino sketch (dht22bmp280.ino)
Arduino sketch that output data on serial for the dashboard.

# Plotting via HTTP, run via shell/terminal
* $ cd senseapp/app
* $ export FLASK_APP=senseapp.py
* $ flask run -h <ip address> -p <port>

# Plotting via serial port
* Configure data pin for DHT22 in pin 2 digital
* Configure i2c for BMP280 in analog pin 4 and 5
* Upload sketch and check in serial monitor

# Run sense dashboard
* $ cd sensedashboard
* $ python senseenv.py
* Select data source via HTTP or serial port.

