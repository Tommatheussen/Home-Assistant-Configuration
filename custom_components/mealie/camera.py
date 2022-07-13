"""Sensor platform for Mealie."""
from __future__ import annotations

from homeassistant.components.camera import Camera

from .const import CAMERA
from .const import DOMAIN
from .entity import MealPlanEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            MealPlanCamera(meal, coordinator, entry)
            for meal in ["breakfast", "lunch", "dinner", "side"]
        ]
    )


class MealPlanCamera(MealPlanEntity, Camera):
    """mealie Camera class."""

    def __init__(self, meal, coordinator, config_entry):
        super().__init__(meal, coordinator, config_entry)
        Camera.__init__(self)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.endpoint}_{self.meal}_{CAMERA}"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        return (
            None
            if not self.recipes
            else await self.coordinator.api.async_get_api_media_recipes_images(
                self.recipes[self.idx]['id']
            )
        )
