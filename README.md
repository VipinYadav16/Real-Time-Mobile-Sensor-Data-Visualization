# Sensor Experiments Dashboard

This project visualizes live sensor data from a phone running Phyphox and streams it into a Python dashboard.

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
3. Enable Remote Access in Phyphox.
4. Copy the IP address shown by Phyphox.
5. Update the `PHY_IP` value in `sensor_data_visual.py` so it points to your phone, for example:

```python
PHY_IP = "192.168.1.100:8080"
```

## Run the Dashboard

```bash
python sensor_data_visual.py
```
