# Sensor Experiments Dashboard

This project visualizes live sensor data from a phone running Phyphox and streams it into a Python dashboard.

## Setup Screenshots

### Step 1: Open the Phyphox app

![Step 1 - Starting page of the mobile app](Step%201.jpeg)

### Step 2: Create the experiment with selected sensors

![Step 2 - Creating an experiment with selected sensors](Step%202.jpeg)

### Step 3: Start streaming with Remote Access enabled

![Step 3 - Running experiment with Remote Access and URL shown](Step%203.jpeg)

### Step 4: View the custom Python dashboard

![Step 4 - Custom built dashboard](Step%204.png)

## Files

- `sensor_data_visual.py` - PyQt6 dashboard with live plots for accelerometer, gyroscope, orientation, magnetometer, and light.
- `requirements.txt` - Python dependencies.

## Requirements

- Python 3.10 or newer
- A smartphone with Phyphox installed
- Phone and computer on the same Wi-Fi network

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Phyphox

1. Open Phyphox on your phone.
2. Select or create an experiment that exposes the sensors you want.
3. Make sure your phone and laptop are connected to the same Wi-Fi network.
4. Enable Remote Access in Phyphox.
5. Copy the IP address shown by Phyphox.
6. Set the `PHY_IP` environment variable before running the dashboard, for example:

```bash
set PHY_IP=192.168.1.100:8080
```

If you prefer, you can set it in your shell session before launching the app. On PowerShell, use `$env:PHY_IP="192.168.1.100:8080"`.

## Run the Dashboard

```bash
python sensor_data_visual.py
```
