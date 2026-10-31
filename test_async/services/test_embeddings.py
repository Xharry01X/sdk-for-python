import json
import httpx2
import respx
import unittest

from appwrite.async_client import AsyncClient
from appwrite.input_file import InputFile
from appwrite.models import *
from appwrite.async_services.embeddings import AsyncEmbeddings


class AsyncEmbeddingsServiceTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = AsyncClient()
        self.embeddings = AsyncEmbeddings(self.client)

    async def asyncTearDown(self):
        await self.client.aclose()

    @respx.mock
    async def test_create_text_embeddings(self):
        data = {
            "total": 5.0,
            "embeddings": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.embeddings.create_text_embeddings(
            [],
            model='nomic-embed-text',
        )
        self.assertEqual(response.to_dict(), data)
