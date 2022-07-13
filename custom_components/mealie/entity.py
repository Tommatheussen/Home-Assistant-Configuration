"""MealieEntity class"""
from __future__ import annotations

import time

from homeassistant.const import CONF_HOST, CONF_USERNAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .const import ICONS
from .const import NAME


class MealieEntity(CoordinatorEntity):
    """mealie Entity class."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.api = self.coordinator.api
        self.coordinator = coordinator
        self.config_entry = config_entry
        self.endpoint = "app/about"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        about_data = self.coordinator.data.get("app/about")
        config_data = self.config_entry.data
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": str(config_data.get(CONF_USERNAME)),
            "model": str(about_data.get("version")),
            "manufacturer": NAME,
            "configuration_url": str(config_data.get(CONF_HOST)),
            "suggested_area": "Kitchen",
        }


class MealPlanEntity(MealieEntity):
    """mealie Meal Plan Entity class."""

    def __init__(self, meal, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self.config_entry = config_entry
        self.endpoint = "groups/mealplans/today"
        self.meal = meal
        self.idx = None
        self.recipes = []

    @property
    def name(self):
        return f"Meal Plan {self.meal.title()}"

    @property
    def icon(self):
        """Return the icon of the camera."""
        return ICONS.get(self.meal)

    def _get_recipes(self):
        mealplans = self.coordinator.data.get(self.endpoint, {})
        self.recipes = [i['recipe'] for i in mealplans if i['entryType'] == self.meal]
        self.idx = self._get_time_based_index()

    def _get_time_based_index(self, interval=60):
        return round(
            ((int(time.time()) % interval) / interval) * (len(self.recipes) - 1)
        )

    async def async_update(self):
        self._get_recipes()

    async def async_added_to_hass(self) -> None:
        self._get_recipes()
