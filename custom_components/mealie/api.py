from __future__ import annotations

import asyncio
from functools import wraps
import logging
import socket
from urllib.parse import urlencode

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


def apirequest(func) -> dict:
    """Decorator for request methods."""

    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> dict | bytes | None:
        """Get information from the API."""

        if not kwargs.get('headers'):
            kwargs['headers'] = self._headers

        if not kwargs.get('skip_auth') and "Authorization" not in kwargs.get('headers'):
            kwargs['headers'].update(await self.async_get_api_auth_token())

        try:
            async with async_timeout.timeout(TIMEOUT):
                return await func(self, *args, **kwargs)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                args[0],
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                args[0],
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                args[0],
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)

    return wrapper


class MealieApi:
    """Wrapper for Mealie's API."""

    def __init__(
        self, username: str, password: str, host: str, session: aiohttp.ClientSession
    ) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._session = session
        self._headers = {
            "Content-type": "application/json; charset=UTF-8",
            "Accept": "application/json",
        }

    def get_host(self):
        return self._host

    @apirequest
    async def _get(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        as_bytes: bool = False,
        skip_auth: bool = False,
    ):
        response = await self._session.get(
            f"{self._host}/api/" + url,
            params=params,
            json=data,
            headers=headers,
        )
        return await (response.read() if as_bytes else response.json())

    @apirequest
    async def _put(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ):
        return await self._session.put(
            f"{self._host}/api/" + url,
            params=params,
            json=data,
            headers=headers,
        )

    @apirequest
    async def _patch(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ):
        return await self._session.patch(
            f"{self._host}/api/" + url,
            params=params,
            json=data,
            headers=headers,
        )

    @apirequest
    async def _post(
        self,
        url: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        skip_auth: bool = True,
    ):
        return await self._session.post(
            f"{self._host}/api/" + url,
            params=params,
            data=data,
            headers=headers,
        )

    async def async_get_api_app_about(self) -> dict:
        """Get data from the API."""
        return await self._get("app/about", skip_auth=True)

    async def async_get_api_groups_mealplans_today(self) -> dict:
        """Get today's mealplan from the API."""
        return await self._get("groups/mealplans/today")

    async def async_get_api_recipes(self, recipe_slug) -> dict:
        """Get recipe details from the API."""
        return await self._get(f"recipes/{recipe_slug}")

    async def async_get_api_recipes_exports(self, recipe_slug, template="recipes.md"):
        """Get formatted recipe data from the API."""
        return await self._get(
            f"recipes/{recipe_slug}/exports",
            params={"template_name": template},
            as_bytes=True,
        )

    async def async_get_api_media_recipes_images(self, recipe_id) -> bytes:
        """Get the image for a recipe from the API."""
        filename = "min-original.webp"
        url = f"media/recipes/{recipe_id}/images/{filename}"
        return await self._get(
            url, headers={"Content-type": "image/webp"}, as_bytes=True
        )

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        await self._patch(url, data={"title": value}, headers=self._headers)

    async def async_get_api_auth_token(self) -> str:
        """Gets an access token from the API."""
        url = "auth/token"
        payload = urlencode(
            {
                "username": self._username,
                "password": self._password,
                "grant_type": "password",
            }
        )

        response = await self._post(
            url,
            data=payload,
            headers={"Content-type": "application/x-www-form-urlencoded"},
            skip_auth=True,
        )

        data = await response.json()
        access_token = data.get("access_token")
        self._headers["Authorization"] = f"Bearer {access_token}"
        return {"Authorization": f"Bearer {access_token}"}
