# custom_components/birdnet/sensor.py
"""Sensor platform for BirdNET-Pi integration."""
import logging
from typing import Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import COORDINATOR, DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the BirdNET-Pi sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    # Add standard sensors
    sensors = []
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        sensors.append(
            BirdNETSensor(
                coordinator,
                entry,
                sensor_type,
                sensor_info["name"],
                sensor_info["icon"],
                sensor_info["device_class"],
                sensor_info["state_class"],
                sensor_info["unit_of_measurement"],
            )
        )
    
    # Add sensor for each detected species today
    if coordinator.data and "species_list" in coordinator.data:
        for species in coordinator.data["species_list"]:
            clean_species = species.lower().replace(" ", "_").replace("'", "").replace("é", "e").replace("è", "e").replace("ê", "e").replace("ç", "c").replace("à", "a")
            sensors.append(
                BirdNETSpeciesSensor(
                    coordinator,
                    entry,
                    clean_species,
                    species,
                    "mdi:bird",
                    None,
                    None,
                    None,
                    species,
                )
            )

    async_add_entities(sensors)


class BirdNETSensor(CoordinatorEntity, SensorEntity):
    """Representation of a BirdNET-Pi sensor."""

    def __init__(
        self,
        coordinator,
        entry,
        sensor_type,
        name,
        icon,
        device_class,
        state_class,
        unit_of_measurement,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_type = sensor_type
        self._name = name
        self._icon = icon
        self._device_class = device_class
        self._state_class = state_class
        self._unit_of_measurement = unit_of_measurement
        self._unique_id = f"{entry.entry_id}_{sensor_type}"
        self.entity_id = f"sensor.birdnet_{sensor_type}"

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"BirdNET {self._name}"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return self._icon

    @property
    def device_class(self) -> Optional[str]:
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self) -> Optional[str]:
        """Return the state class of the sensor."""
        return self._state_class

    @property
    def unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"BirdNET-Pi ({self._entry.data['host']})",
            "manufacturer": "BirdNET",
            "model": "BirdNET-Pi Bridge",
            "sw_version": "0.1.0",
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.data:
            return False
            
        # Check if the specific data for this sensor type is available
        if self._sensor_type == "last_detection":
            return "latest_detections" in self.coordinator.data and len(self.coordinator.data["latest_detections"]) > 0
        elif self._sensor_type in ["today_count", "species_count"]:
            return self._sensor_type in self.coordinator.data
            
        return True

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        if self._sensor_type == "last_detection":
            if "latest_detections" in self.coordinator.data and len(self.coordinator.data["latest_detections"]) > 0:
                detection = self.coordinator.data["latest_detections"][0]
                return detection.get("common_name", "Unknown")
            return None
        elif self._sensor_type in ["today_count", "species_count"]:
            return self.coordinator.data.get(self._sensor_type, 0)
            
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        
        if not self.coordinator.data:
            return attrs
            
        if self._sensor_type == "last_detection":
            if "latest_detections" in self.coordinator.data and len(self.coordinator.data["latest_detections"]) > 0:
                detection = self.coordinator.data["latest_detections"][0]
                attrs = {
                    "scientific_name": detection.get("scientific_name", ""),
                    "confidence": detection.get("confidence", 0),
                    "date": detection.get("date", ""),
                    "time": detection.get("time", ""),
                    "audio_file": detection.get("audio_file", ""),
                }
        elif self._sensor_type == "species_count":
            attrs["species_list"] = self.coordinator.data.get("species_list", [])
            
        return attrs


class BirdNETSpeciesSensor(BirdNETSensor):
    """Representation of a BirdNET-Pi species sensor."""

    def __init__(
        self,
        coordinator,
        entry,
        species_id,
        species_name,
        icon,
        device_class,
        state_class,
        unit_of_measurement,
        species_name_full,
    ):
        """Initialize the sensor."""
        # Utilisons un identifiant unique pour cette espèce
        sensor_type = f"species_{species_id}"
        
        # Cette ligne est nécessaire pour le traitement ultérieur
        self._species_name = species_name_full
        
        # Configuration du capteur parent
        super().__init__(
            coordinator,
            entry,
            sensor_type,
            species_name,
            icon,
            device_class,
            state_class,
            unit_of_measurement,
        )
        
        # Définir explicitement l'entity_id
        self.entity_id = f"sensor.birdnet_species_{species_id}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self._species_name}"  # Juste le nom de l'espèce

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data is not None and "today_detections" in self.coordinator.data

    @property
    def state(self):
        """Return the count of detections for this species today."""
        if not self.coordinator.data or "today_detections" not in self.coordinator.data:
            return 0
            
        # Count detections for this species
        count = 0
        for detection in self.coordinator.data["today_detections"]:
            if detection.get("common_name", "") == self._species_name:
                count += 1
                
        return count

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        
        if not self.coordinator.data or "today_detections" not in self.coordinator.data:
            return attrs
            
        # Get latest detection for this species
        latest = None
        latest_time = ""
        
        for detection in self.coordinator.data["today_detections"]:
            if detection.get("common_name", "") == self._species_name:
                # Check if this is the latest detection
                detection_time = f"{detection.get('date', '')} {detection.get('time', '')}"
                if not latest_time or detection_time > latest_time:
                    latest = detection
                    latest_time = detection_time
        
        if latest:
            attrs = {
                "scientific_name": latest.get("scientific_name", ""),
                "last_confidence": latest.get("confidence", 0),
                "last_detection_time": latest.get("time", ""),
                "last_audio_file": latest.get("audio_file", ""),
            }
            
        return attrs