
import sys
import os
import requests
import numpy as np

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QVBoxLayout, QTextEdit
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

PHY_IP = os.getenv("PHY_IP", "").strip()

HISTORY = 100

pg.setConfigOptions(antialias=True)


class SensorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Phone Sensor Dashboard")
        self.resize(1400, 900)

        self.data = {}
        keys = [
            "accX","accY","accZ",
            "gyrX","gyrY","gyrZ",
            "yaw","pitch","roll",
            "magX","magY","magZ",
            "light","prox"
        ]
        for k in keys:
            self.data[k] = [0.0] * HISTORY

        layout = QGridLayout()
        self.setLayout(layout)

        self.acc_plot = self.make_plot("Accelerometer")
        self.gyr_plot = self.make_plot("Gyroscope")
        self.ori_plot = self.make_plot("Orientation")
        self.mag_plot = self.make_plot("Magnetometer")
        self.light_plot = self.make_plot("Light")
        # Replace proximity plot with a log panel for runtime messages
        self.prox_plot = None
        self.log_widget = QWidget()
        vlog = QVBoxLayout(self.log_widget)
        vlog_label = QLabel("Logs")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background:#0f0f0f; color:#ffffff;")
        vlog.addWidget(vlog_label)
        vlog.addWidget(self.log_text)

        layout.addWidget(self.acc_plot["widget"], 0, 0)
        layout.addWidget(self.gyr_plot["widget"], 0, 1)

        layout.addWidget(self.ori_plot["widget"], 1, 0)
        layout.addWidget(self.mag_plot["widget"], 1, 1)

        layout.addWidget(self.light_plot["widget"], 2, 0)
        layout.addWidget(self.log_widget, 2, 1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def make_plot(self, title):
        container = QWidget()
        v = QVBoxLayout(container)

        label = QLabel(title)
        plot = pg.PlotWidget()
        plot.showGrid(x=True, y=True)
        plot.setBackground("#1e1e1e")

        v.addWidget(label)
        v.addWidget(plot)

        return {"widget": container, "plot": plot}

    def push(self, key, value):
        arr = self.data[key]
        arr.pop(0)
        arr.append(float(value))

    def append_log(self, msg: str):
        from datetime import datetime

        ts = datetime.now().strftime("%H:%M:%S")
        try:
            # Append with timestamp and keep latest visible
            self.log_text.append(f"[{ts}] {msg}")
        except Exception:
            pass

    def fetch(self):
        if not PHY_IP:
            raise RuntimeError("Set the PHY_IP environment variable to your Phyphox address, for example 192.168.1.100:8080")

        url = f"http://{PHY_IP}/get?accX&accY&accZ&gyrX&gyrY&gyrZ&yaw&pitch&roll&light&magX&magY&magZ&prox"
        r = requests.get(url, timeout=1)
        return r.json()

    def update_data(self):
        try:
            j = self.fetch()
            buf = j["buffer"]

            for key in self.data.keys():
                self.push(key, buf[key]["buffer"][0])

            # Add a concise log entry including proximity and light
            try:
                prox_val = buf.get("prox", {}).get("buffer", [None])[0]
            except Exception:
                prox_val = None
            try:
                light_val = buf.get("light", {}).get("buffer", [None])[0]
            except Exception:
                light_val = None

            self.append_log(f"Fetched sensors - prox={prox_val} light={light_val}")
            self.redraw()

        except Exception as e:
            err = str(e)
            print("Fetch error:", err)
            self.append_log(f"Fetch error: {err}")

    def redraw(self):
        x = np.arange(HISTORY)

        # Plot accelerometer (X=red, Y=green, Z=blue)
        self.acc_plot["plot"].clear()
        self.acc_plot["plot"].plot(x, self.data["accX"], pen=pg.mkPen("r", width=2))
        self.acc_plot["plot"].plot(x, self.data["accY"], pen=pg.mkPen("g", width=2))
        self.acc_plot["plot"].plot(x, self.data["accZ"], pen=pg.mkPen("b", width=2))


        # Plot gyroscope (X=red, Y=green, Z=blue)
        self.gyr_plot["plot"].clear()
        self.gyr_plot["plot"].plot(x, self.data["gyrX"], pen=pg.mkPen("r", width=2))
        self.gyr_plot["plot"].plot(x, self.data["gyrY"], pen=pg.mkPen("g", width=2))
        self.gyr_plot["plot"].plot(x, self.data["gyrZ"], pen=pg.mkPen("b", width=2))


        # Plot orientation (yaw/pitch/roll) using distinct colors
        self.ori_plot["plot"].clear()
        self.ori_plot["plot"].plot(x, self.data["yaw"], pen=pg.mkPen("r", width=2))
        self.ori_plot["plot"].plot(x, self.data["pitch"], pen=pg.mkPen("g", width=2))
        self.ori_plot["plot"].plot(x, self.data["roll"], pen=pg.mkPen("b", width=2))


        # Plot magnetometer (X=red, Y=green, Z=blue)
        self.mag_plot["plot"].clear()
        self.mag_plot["plot"].plot(x, self.data["magX"], pen=pg.mkPen("r", width=2))
        self.mag_plot["plot"].plot(x, self.data["magY"], pen=pg.mkPen("g", width=2))
        self.mag_plot["plot"].plot(x, self.data["magZ"], pen=pg.mkPen("b", width=2))


        # Light (yellow)
        self.light_plot["plot"].clear()
        self.light_plot["plot"].plot(x, self.data["light"], pen=pg.mkPen("#ffcc00", width=2))

        # Proximity is shown in the log panel instead of a plot


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SensorDashboard()
    w.show()
    sys.exit(app.exec())
