"""Sensor platform for Mealie."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from . import clean_obj
from .const import DOMAIN
from .const import SENSOR
from .entity import MealPlanEntity

ICONS = {
    "breakfast": "mdi:egg-fried",
    "lunch": "mdi:bread-slice",
    "dinner": "mdi:pot-steam",
    "side": "mdi:bowl-mix-outline",
}


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            MealPlanSensor(meal, coordinator, entry)
            for meal in ["breakfast", "lunch", "dinner", "side"]
        ]
    )


class MealPlanSensor(MealPlanEntity, SensorEntity):
    """mealie Sensor class."""

    def __init__(self, meal, coordinator, config_entry):
        super().__init__(meal, coordinator, config_entry)
        SensorEntity.__init__(self)

    @staticmethod
    def _format_instructions(instructions):
        text = ""
        for idx, i in enumerate(instructions):
            if title := i.get('title'):
                text += f"\n## {title}\n"
            text += f"### Step {idx+1}\n\n{i.get('text')}\n"
        return None if text == "" else text

    @staticmethod
    def _format_ingredients(ingredients):
        text = ""
        for i in ingredients:
            if title := i.get('title'):
                text += f"\n## {title}\n"
            if any(k in i for k in ['unit', 'food']):
                text += f"- [ ]{' ' + str(i.get('quantity', '')) if i.get('quantity') else ''}"
                for key in ['unit', 'food']:
                    text += f" {i.get(key, {}).get('name', '')}" if i.get(key) else ""
                text += f"{', ' + i.get('note', '') if i.get('note', '') else ''}\n"
            else:
                text += f"- [ ] {i.get('note')}\n"
        return None if text == "" else text

    @staticmethod
    def _format_tags(tags):
        text = ', '.join([t['name'] for t in tags])
        return None if text == "" else text

    @staticmethod
    def _format_categories(categories):
        text = ', '.join([c['name'] for c in categories])
        return None if text == "" else text

    @staticmethod
    def _format_nutrition(nutrition):
        text = ""
        if nutrition:
            text = "| Type | Amount |\n|:-----|-------:|\n"

        formatted = {k.replace("Content", ""): v for k, v in nutrition.items()}
        for n in formatted:
            text += f"| {n.title()} | {formatted[n]} |\n"
        return None if text == "" else text

    @staticmethod
    def _format_tools(tools):
        text = ""
        for t in tools:
            text += f"- [ ] {t.get('name')}\n"
        return None if text == "" else text

    @staticmethod
    def _format_comments(comments):
        text = ""
        for c in sorted(comments, key=lambda x: x['createdAt']):
            text += f"* {c.get('text')} by {c.get('user', {}).get('username', 'Anonymous')} @ {c.get('createdAt')}\n"
        return None if text == "" else text

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.endpoint}_{self.meal}_{SENSOR}"

    @property
    def native_value(self):
        return None if not self.recipes else self.recipes[self.idx]['name']

    @property
    def extra_state_attributes(self):
        attrs = {}
        if self.recipes:
            recipe = self.recipes[self.idx]
            attrs = {
                "instructions": clean_obj(recipe.get("recipeInstructions")),
                "instructions_md": self._format_instructions(
                    clean_obj(recipe.get("recipeInstructions", []))
                ),
                "ingredients": clean_obj(recipe.get("recipeIngredient")),
                "ingredients_md": self._format_ingredients(
                    clean_obj(recipe.get("recipeIngredient", []))
                ),
                "tools": clean_obj(recipe.get("tools")),
                "tools_md": self._format_tools(clean_obj(recipe.get("tools", {}))),
                "nutrition": clean_obj(recipe.get("nutrition")),
                "nutrition_md": self._format_nutrition(
                    clean_obj(recipe.get("nutrition", {}))
                ),
                "comments": clean_obj(recipe.get("comments")),
                "comments_md": self._format_comments(
                    clean_obj(recipe.get("comments", []))
                ),
                "tags": clean_obj(recipe.get("tags")),
                "tags_md": self._format_tags(recipe.get("tags", [])),
                "categories": clean_obj(recipe.get("recipeCategory")),
                "categories_md": self._format_categories(
                    recipe.get("recipeCategory", [])
                ),
                "yield": recipe.get("recipeYield"),
                "total_time": recipe.get("totalTime"),
                "prep_time": recipe.get("prepTime"),
                "cook_time": recipe.get("performTime"),
                "rating": recipe.get("rating"),
                "description": recipe.get("description"),
                "name": recipe.get("name"),
                "original_url": recipe.get("orgURL"),
                "mealie_url": f"{self.coordinator.data.get('host', '')}/recipe/{recipe.get('slug', '')}",
                "assets": clean_obj(recipe.get("assets", [])),
                "notes": clean_obj(recipe.get("notes", [])),
                "extras": clean_obj(recipe.get("extras", {})),
            }

        return clean_obj(attrs)
