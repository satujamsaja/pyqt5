"""
Distance calculator app.
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QDesktopWidget, QGroupBox, QFormLayout, \
    QLabel, QPushButton, QDoubleSpinBox
from geopy.distance import great_circle
import requests
import yaml


class DistanceCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Line edits.
        self.from_lat = QDoubleSpinBox()
        self.from_lon = QDoubleSpinBox()
        self.from_lat.setMinimum(-999)
        self.from_lat.setMaximum(999)
        self.from_lat.setDecimals(6)
        self.from_lon.setMinimum(-999)
        self.from_lon.setMaximum(999)
        self.from_lon.setDecimals(6)
        self.to_lat = QDoubleSpinBox()
        self.to_lon = QDoubleSpinBox()
        self.to_lat.setMinimum(-999)
        self.to_lat.setMaximum(999)
        self.to_lat.setDecimals(6)
        self.to_lon.setMinimum(-999)
        self.to_lon.setMaximum(999)
        self.to_lon.setDecimals(6)
        self.city_from = QLineEdit()
        self.city_to = QLineEdit()

        # Buttons
        self.calc_latlon = QPushButton("Calculate")
        self.calc_latlon.clicked.connect(self.distance_calc)
        self.calc_cities = QPushButton("Calculate")
        self.calc_cities.clicked.connect(self.cities_calc)

        # Result
        self.distance_km = QLabel("0")
        self.distance_mile = QLabel("0")

        # Config.
        self.config = self.get_config()
        # Init ui.
        self.init_ui()

    """
    Init all ui.
    """
    def init_ui(self):
        self.setWindowTitle("Distance Calculator")
        self.resize(300, 200)
        self.init_center()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.init_coordinate_widget())
        main_layout.addWidget(self.init_city_widget())
        main_layout.addWidget(self.init_result_widget())
        self.setLayout(main_layout)

        self.show()

    """
    Coordinate widget and layout form.
    """
    def init_coordinate_widget(self):
        coordinate_group = QGroupBox("GREAT CIRCLE DISTANCE BY COORDINATE")
        coordinate_layout = QFormLayout()
        coordinate_layout.addRow(QLabel("From latitude: "), self.from_lat)
        coordinate_layout.addRow(QLabel("From longitude: "), self.from_lon)
        coordinate_layout.addRow(QLabel("To latitude: "), self.to_lat)
        coordinate_layout.addRow(QLabel("To longitude: "), self.to_lon)
        coordinate_layout.addWidget(self.calc_latlon)
        coordinate_group.setLayout(coordinate_layout)

        return coordinate_group

    """
    City widget and layout form.
    """
    def init_city_widget(self):
        city_group = QGroupBox("GREAT CIRCLE DISTANCE BY CITY")
        city_layout = QFormLayout()
        city_layout.addRow(QLabel("From city: "), self.city_from)
        city_layout.addRow(QLabel("To city: "), self.city_to)
        city_layout.addWidget(self.calc_cities)
        city_group.setLayout(city_layout)
        return city_group

    """
    Result section in widget.
    """
    def init_result_widget(self):
        result_group = QGroupBox("RESULT")
        result_layout = QFormLayout()
        result_layout.addRow(QLabel("Distance in Km: "), self.distance_km)
        result_layout.addRow(QLabel("Distance in Mile: "), self.distance_mile)
        result_group.setLayout(result_layout)
        return result_group

    """
    Set window app in center.
    """
    def init_center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    """
    Calculate distance by coordinate.
    """
    def distance_calc(self):
        coord_from = (self.from_lat.value(), self.from_lon.value())
        coord_to = (self.to_lat.value(), self.to_lon.value())
        dkm = great_circle(coord_from, coord_to).km
        dmi = great_circle(coord_from, coord_to).miles

        self.distance_km.setText("{}".format(round(dkm, 2)))
        self.distance_mile.setText("{}".format(round(dmi, 2)))

    """
    Calculate distance by city.
    """
    def cities_calc(self):
        city_from = self.city_from.text()
        city_to = self.city_to.text()
        if city_to and city_from:
            data_from = self.city_geocode(city_from)
            data_to = self.city_geocode(city_to)
            if data_from and data_to:
                coord_from = (data_from.get('latt'), data_from.get('longt'))
                coord_to = (data_to.get('latt'), data_to.get('longt'))
                dkm = great_circle(coord_from, coord_to).km
                dmi = great_circle(coord_from, coord_to).miles

                self.distance_km.setText("{}".format(round(dkm, 2)))
                self.distance_mile.setText("{}".format(round(dmi, 2)))

    """
    Get geocode from location.
    """
    def city_geocode(self, city):
        if self.config:
            try:
                url = self.config.get('api_url') + "{}".format(city) + "?json=1" + \
                      "&auth={}".format(self.config.get('api_auth'))
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return data
            except requests.exceptions.ConnectionError as e:
                print(e)
        else:
            print("Config not found.")

    """
    Get api settings.
    """
    @staticmethod
    def get_config():
        with open('auth.yml') as yml:
            config = yaml.load(yml, Loader=yaml.SafeLoader)
            if config:
                return config


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exc = DistanceCalculator()
    sys.exit(app.exec_())
