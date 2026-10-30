import json
import httpx2
import respx
import unittest

from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.models import *
from appwrite.services.waf import Waf


class WafServiceTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = Client()
        self.waf = Waf(self.client)

    async def asyncTearDown(self):
        await self.client.aclose()

    @respx.mock
    async def test_list_rules(self):
        data = {
            "total": 5.0,
            "rules": [],
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.list_rules(
            queries=[],
            search='<SEARCH>',
            total=False,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_create_bypass_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.create_bypass_rule(
            '<RULE_ID>',
            'api',
            '<NAME>',
            resource_id='<RESOURCE_ID>',
            description='<DESCRIPTION>',
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_update_bypass_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.update_bypass_rule(
            '<RULE_ID>',
            resource_type='api',
            resource_id='<RESOURCE_ID>',
            name='<NAME>',
            description='<DESCRIPTION>',
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_create_challenge_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "challengeType": "compute",
            "difficulty": 3.0,
            "ttl": 1800.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.create_challenge_rule(
            '<RULE_ID>',
            'api',
            '<NAME>',
            resource_id='<RESOURCE_ID>',
            description='<DESCRIPTION>',
            challenge_type='compute',
            priority=1,
            enabled=False,
            conditions=[],
            difficulty=1,
            ttl=1,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_update_challenge_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "challengeType": "compute",
            "difficulty": 3.0,
            "ttl": 1800.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.update_challenge_rule(
            '<RULE_ID>',
            resource_type='api',
            resource_id='<RESOURCE_ID>',
            name='<NAME>',
            description='<DESCRIPTION>',
            challenge_type='compute',
            priority=1,
            enabled=False,
            conditions=[],
            difficulty=1,
            ttl=1,
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_create_deny_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.create_deny_rule(
            '<RULE_ID>',
            'api',
            '<NAME>',
            resource_id='<RESOURCE_ID>',
            description='<DESCRIPTION>',
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_update_deny_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.update_deny_rule(
            '<RULE_ID>',
            resource_type='api',
            resource_id='<RESOURCE_ID>',
            name='<NAME>',
            description='<DESCRIPTION>',
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_create_rate_limit_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "limit": 1000.0,
            "interval": 60.0,
            "key": "userId",
            "strategy": "slidingWindow",
            "maxBucketSize": 200.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.create_rate_limit_rule(
            '<RULE_ID>',
            'api',
            '<NAME>',
            1,
            1,
            resource_id='<RESOURCE_ID>',
            description='<DESCRIPTION>',
            key='ip',
            strategy='fixedWindow',
            max_bucket_size=1,
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_update_rate_limit_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "limit": 1000.0,
            "interval": 60.0,
            "key": "userId",
            "strategy": "slidingWindow",
            "maxBucketSize": 200.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.update_rate_limit_rule(
            '<RULE_ID>',
            resource_type='api',
            resource_id='<RESOURCE_ID>',
            name='<NAME>',
            description='<DESCRIPTION>',
            limit=1,
            interval=1,
            key='ip',
            max_bucket_size=1,
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_create_redirect_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "location": "\/maintenance",
            "statusCode": 301.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.create_redirect_rule(
            '<RULE_ID>',
            'api',
            '<NAME>',
            '<LOCATION>',
            1,
            resource_id='<RESOURCE_ID>',
            description='<DESCRIPTION>',
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_update_redirect_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
            "location": "\/maintenance",
            "statusCode": 301.0,
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.update_redirect_rule(
            '<RULE_ID>',
            resource_type='api',
            resource_id='<RESOURCE_ID>',
            name='<NAME>',
            description='<DESCRIPTION>',
            location='<LOCATION>',
            status_code=1,
            priority=1,
            enabled=False,
            conditions=[],
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_get_rule(self):
        data = {
            "$id": "wafRule1",
            "$createdAt": "2020-10-15T06:38:00.000+00:00",
            "$updatedAt": "2020-10-15T06:38:00.000+00:00",
            "name": "Block anonymous POST traffic",
            "description": "Blocks anonymous POST calls to \/v1\/graphql",
            "teamId": "5e5ea5c16897e",
            "projectId": "cloudConsole",
            "resourceType": "functions",
            "resourceId": "functionId",
            "action": "deny",
            "priority": 100.0,
            "enabled": True,
            "conditions": [],
            "config": {},
        }
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.get_rule(
            '<RULE_ID>',
        )
        self.assertEqual(response.to_dict(), data)

    @respx.mock
    async def test_delete_rule(self):
        data = ''
        headers = {'Content-Type': 'application/json'}
        respx.route().mock(
            return_value=httpx2.Response(200, text=json.dumps(data), headers=headers),
        )
        response = await self.waf.delete_rule(
            '<RULE_ID>',
        )
        self.assertEqual(response, data)
