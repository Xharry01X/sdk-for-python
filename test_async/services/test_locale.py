import json
import httpx2
import respx
import unittest

from appwrite.async_client import AsyncClient
from appwrite.input_file import InputFile
from appwrite.models import *
from appwrite.async_services.locale import AsyncLocale


class AsyncLocaleServiceTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = AsyncClient()
        self.locale = AsyncLocale(self.client)

    async def asyncTearDown(self):
        await self.client.aclose()

    @respx.mock
    async def test_get(self):
        data = {
            "ip": "127.0.0.1",
            "countryCode": "US",
            "country": "United States",
            "continentCode": "NA",
            "continent": "North America",
            "eu": True,
            "currency": "USD",
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.get()
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_codes(self):
        data = {
            "total": 5.0,
            "localeCodes": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_codes(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_continents(self):
        data = {
            "total": 5.0,
            "continents": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_continents(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_countries(self):
        data = {
            "total": 5.0,
            "countries": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_countries(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_countries_eu(self):
        data = {
            "total": 5.0,
            "countries": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_countries_eu(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_countries_phones(self):
        data = {
            "total": 5.0,
            "phones": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_countries_phones(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_currencies(self):
        data = {
            "total": 5.0,
            "currencies": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_currencies(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_list_languages(self):
        data = {
            "total": 5.0,
            "languages": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.locale.list_languages(
            total=False,
        )
        self.assertEqual(response.to_dict(), data)
