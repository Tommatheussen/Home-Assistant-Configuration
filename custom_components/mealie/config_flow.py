"""Adds config flow for Mealie."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_HOST
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import MealieApi
from .const import DOMAIN


class MealieFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for mealie."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                user_input[CONF_HOST],
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password, host):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = MealieApi(username, password, host, session)
            await client.async_get_api_app_about()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False
