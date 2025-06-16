# custom_components/birdnet/config_flow.py
"""Config flow for BirdNET-Pi integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class BirdnetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BirdNET-Pi."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate connection to BirdNET-Pi bridge
                session = async_get_clientsession(self.hass)
                url = f"http://{user_input['host']}:{user_input['port']}/api/detections/latest?limit=1"
                
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        # Connection successful, create entry
                        return self.async_create_entry(
                            title=f"BirdNET-Pi ({user_input['host']})",
                            data=user_input
                        )
                    else:
                        errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Form schema
        data_schema = vol.Schema(
            {
                vol.Required("host", default="localhost"): str,
                vol.Required("port", default=5000): cv.port,
                vol.Required("scan_interval", default=60): int,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BirdnetOptionsFlowHandler(config_entry)

class BirdnetOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle BirdNET-Pi options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Required(
                "scan_interval",
                default=self.config_entry.options.get("scan_interval", 60),
            ): int,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))