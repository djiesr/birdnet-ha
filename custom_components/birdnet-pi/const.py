# custom_components/birdnet/const.py
"""Constants for the BirdNET-Pi integration."""

DOMAIN = "birdnet"
COORDINATOR = "coordinator"

# Sensor types
SENSOR_TYPES = {
    "last_detection": {
        "name": "Last Bird Detection",
        "icon": "mdi:bird",
        "device_class": None,
        "state_class": None,
        "unit_of_measurement": None,
    },
    "today_count": {
        "name": "Birds Detected Today",
        "icon": "mdi:counter",
        "device_class": None,
        "state_class": "measurement",
        "unit_of_measurement": "birds",
    },
    "species_count": {
        "name": "Bird Species Today",
        "icon": "mdi:nature",
        "device_class": None,
        "state_class": "measurement",
        "unit_of_measurement": "species",
    },
}