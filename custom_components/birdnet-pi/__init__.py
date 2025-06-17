# custom_components/birdnet/__init__.py
"""The BirdNET-Pi integration."""
import asyncio
import logging
from datetime import timedelta

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BirdNET-Pi from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    
    # Ajoutez cette ligne
    hass.data[DOMAIN][entry.entry_id]["entity_namespace"] = "birdnet"
    host = entry.data["host"]
    port = entry.data["port"]
    scan_interval = entry.options.get("scan_interval", entry.data.get("scan_interval", 60))

    session = async_get_clientsession(hass)
    
    # Setup coordinator
    coordinator = BirdNETDataUpdateCoordinator(
        hass, 
        logger=_LOGGER,
        name=f"BirdNET-Pi {host}",
        session=session,
        host=host,
        port=port,
        update_interval=timedelta(seconds=scan_interval),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator,
    }

    # Set up all platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.add_update_listener(async_update_entry)
    return True


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options when entry is updated."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class BirdNETDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching BirdNET-Pi data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        name: str,
        session: aiohttp.ClientSession,
        host: str,
        port: int,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.host = host
        self.port = port
        self.session = session
        self.base_url = f"http://{host}:{port}/api"

        super().__init__(hass, logger, name=name, update_interval=update_interval)

    async def _async_update_data(self):
        """Fetch data from BirdNET-Pi."""
        data = {}
        
        try:
            async with async_timeout.timeout(10):
                # Get latest detections
                latest_url = f"{self.base_url}/detections/latest?limit=5"
                async with self.session.get(latest_url) as resp:
                    if resp.status == 200:
                        data["latest_detections"] = await resp.json()
                    else:
                        raise UpdateFailed(f"Error fetching latest detections: {resp.status}")
                
                # Get today's detections
                today_url = f"{self.base_url}/detections/today"
                async with self.session.get(today_url) as resp:
                    if resp.status == 200:
                        today_detections = await resp.json()
                        data["today_detections"] = today_detections
                        
                        # Count species
                        species_set = set()
                        for detection in today_detections:
                            species_set.add(detection.get("common_name", ""))
                        
                        data["today_count"] = len(today_detections)
                        data["species_count"] = len(species_set)
                        data["species_list"] = sorted(list(species_set))
                    else:
                        raise UpdateFailed(f"Error fetching today's detections: {resp.status}")
                
                # Get daily stats
                stats_url = f"{self.base_url}/stats/daily"
                async with self.session.get(stats_url) as resp:
                    if resp.status == 200:
                        data["daily_stats"] = await resp.json()
                    else:
                        raise UpdateFailed(f"Error fetching daily stats: {resp.status}")
                
            return data
        except asyncio.TimeoutError:
            raise UpdateFailed("Timeout error fetching BirdNET-Pi data")
        except Exception as err:
            raise UpdateFailed(f"Error communicating with BirdNET-Pi: {err}")