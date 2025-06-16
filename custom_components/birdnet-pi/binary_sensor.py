# custom_components/birdnet/binary_sensor.py
"""Binary sensor platform for BirdNET-Pi integration."""
import logging
from typing import Optional

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the BirdNET-Pi binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    # Add presence binary sensor (binary_sensor.birdnet_detection_recent)
    binary_sensors = [BirdDetectionBinarySensor(coordinator, entry)]
    
    # Add individual species presence sensors (binary_sensor.birdnet_presence_roselin_familier, etc.)
    if coordinator.data and "species_list" in coordinator.data:
        for species in coordinator.data["species_list"]:
            clean_species = species.lower().replace(" ", "_").replace("'", "").replace("é", "e").replace("à", "a").replace("ê", "e").replace("è", "e")
            binary_sensors.append(
                BirdSpeciesPresenceSensor(
                    coordinator,
                    entry,
                    f"presence_{clean_species}",  # Ceci générera des id comme "binary_sensor.birdnet_presence_roselin_familier"
                    f"{species} Presence",
                    species,
                )
            )

    async_add_entities(binary_sensors)


class BirdDetectionBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for recent bird detection."""

    def __init__(self, coordinator, entry):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_detection_recent"
        self._attr_name = "BirdNET Detection Recent"
        self._attr_device_class = BinarySensorDeviceClass.SOUND
        self._attr_icon = "mdi:bird"

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
    def is_on(self) -> bool:
        """Return true if a bird was detected in the last update cycle."""
        if not self.coordinator.data:
            return False
            
        if "latest_detections" in self.coordinator.data and len(self.coordinator.data["latest_detections"]) > 0:
            latest = self.coordinator.data["latest_detections"][0]
            # Check if the latest detection is from today
            if "date" in latest and "time" in latest:
                # You could add more sophisticated time checking here
                return True
                
        return False

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        
        if not self.coordinator.data:
            return attrs
            
        if "latest_detections" in self.coordinator.data and len(self.coordinator.data["latest_detections"]) > 0:
            latest = self.coordinator.data["latest_detections"][0]
            attrs = {
                "species": latest.get("common_name", "Unknown"),
                "scientific_name": latest.get("scientific_name", ""),
                "confidence": latest.get("confidence", 0),
                "date": latest.get("date", ""),
                "time": latest.get("time", ""),
            }
            
        return attrs


class BirdSpeciesPresenceSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for species presence."""

    def __init__(self, coordinator, entry, unique_id, name, species_name):
        """Initialize the species presence sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._species_name = species_name
        
        # Créons un ID propre pour l'espèce
        clean_species = species_name.lower().replace(" ", "_").replace("'", "").replace("é", "e").replace("à", "a").replace("ê", "e").replace("è", "e")
        
        # Définir l'unique_id et le nom
        self._attr_unique_id = f"{entry.entry_id}_presence_{clean_species}"
        self._attr_name = f"Presence {species_name}"
        
        # Définissons l'entity_id personnalisé
        self.entity_id = f"binary_sensor.birdnet_presence_{clean_species}"
        
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE
        self._attr_icon = "mdi:bird"

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
    def is_on(self) -> bool:
        """Return true if this species was detected today."""
        if not self.coordinator.data or "today_detections" not in self.coordinator.data:
            return False
            
        # Check if this species is in today's detections
        for detection in self.coordinator.data["today_detections"]:
            if detection.get("common_name", "") == self._species_name:
                return True
                
        return False

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            "species": self._species_name,
        }
        
        if not self.coordinator.data or "today_detections" not in self.coordinator.data:
            return attrs
            
        # Get latest detection and count for this species
        latest = None
        latest_time = ""
        count = 0
        
        for detection in self.coordinator.data["today_detections"]:
            if detection.get("common_name", "") == self._species_name:
                count += 1
                
                # Check if this is the latest detection
                detection_time = f"{detection.get('date', '')} {detection.get('time', '')}"
                if not latest_time or detection_time > latest_time:
                    latest = detection
                    latest_time = detection_time
        
        attrs["count_today"] = count
        
        if latest:
            attrs.update({
                "scientific_name": latest.get("scientific_name", ""),
                "last_confidence": latest.get("confidence", 0),
                "last_detection_time": latest.get("time", ""),
            })
            
        return attrs