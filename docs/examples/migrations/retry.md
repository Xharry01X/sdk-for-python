```python
import asyncio

from appwrite.client import Client
from appwrite.services.migrations import Migrations
from appwrite.models import Migration


async def main():
    client = Client()
    client.set_endpoint('https://<REGION>.cloud.appwrite.io/v1') # Your API Endpoint
    client.set_project('<YOUR_PROJECT_ID>') # Your project ID
    client.set_key('<YOUR_API_KEY>') # Your secret API key

    migrations = Migrations(client)

    result: Migration = await migrations.retry(
        migration_id = '<MIGRATION_ID>'
    )

    print(result.model_dump())


asyncio.run(main())
```
