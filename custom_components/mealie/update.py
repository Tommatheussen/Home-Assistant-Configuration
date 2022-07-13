"""Sensor platform for Mealie."""
from __future__ import annotations

import aiohttp

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from .const import NAME
from .const import SOURCE_REPO
from .const import DOMAIN
from .const import UPDATE
from .entity import MealieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([MealieUpdate(coordinator, entry)])


class MealieUpdate(MealieEntity, UpdateEntity):
    """mealie Update class."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        UpdateEntity.__init__(self)
        self._latest_version = None
        self._release_url = None
        self._release_notes = None

    async def _get_update_data(self):
        url = f"https://api.github.com/repos/{SOURCE_REPO}/releases"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response:
                    json = await response.json()
                    self._latest_version = json[0]['tag_name']
                    self._release_url = json[0]['html_url']
                    self._release_notes = json[0]['body']

    async def async_update(self):
        await self._get_update_data()

    async def async_added_to_hass(self) -> None:
        await self._get_update_data()

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.endpoint}_{UPDATE}"

    @property
    def installed_version(self):
        about_data = self.coordinator.data.get(self.endpoint)
        return about_data['version']

    @property
    def latest_version(self):
        return self._latest_version

    @property
    def release_url(self):
        return self._release_url

    @property
    def name(self):
        """Return the name of the update."""
        return f"{NAME} {UPDATE.title()}"

    @property
    def title(self):
        return NAME

    async def async_release_notes(self) -> str | None:
        return self._release_notes

    @property
    def supported_features(self):
        return UpdateEntityFeature.RELEASE_NOTES
