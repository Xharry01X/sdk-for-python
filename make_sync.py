#!/usr/bin/env python
"""Generate the synchronous mirror of the asynchronous Appwrite SDK.

The ``appwrite`` package ships a synchronous client (the default) next to an
asynchronous one (``appwrite.async_client`` and ``appwrite.async_services``).
This script mirrors the asynchronous tree into ``appwrite_sync`` + ``test_sync``
so the async sources have a plain-function counterpart: every ``*.py`` file is
run through `unasync <https://github.com/python-trio/unasync>`_, which strips
``async``/``await`` and applies whole-token renames such as ``AsyncClient`` ->
``Client`` and ``appwrite`` -> ``appwrite_sync``. The ``Async*`` services are
renamed to their plain names from the class names the async services declare,
so ``AsyncUsers`` becomes ``Users`` and not ``SyncUsers``. A handful of plain
textual fixes are then applied to the generated files for the spots unasync
cannot restructure (the anyio semaphore and task group in the chunked uploader,
thread offloading, sync-incompatible concurrency tests).

The generated trees are disposable output and are gitignored.

Requires: ``pip install unasync``
"""

import os
import re
import shutil

import unasync

# Whole-NAME-token replacements unasync applies on top of its built-ins
# (async def/await/async with/async for are rewritten automatically).
ADDITIONAL_REPLACEMENTS = {
    "appwrite": "appwrite_sync",
    "async_client": "client",
    "async_services": "services",
    "aclose": "close",
    "__aenter__": "__enter__",
    "__aexit__": "__exit__",
    "AsyncClient": "Client",
    "IsolatedAsyncioTestCase": "TestCase",
    "asyncSetUp": "setUp",
    "asyncTearDown": "tearDown",
}

# The default synchronous SDK is not mirrored: it is generated on its own and
# ships in the `appwrite` package.
NOT_MIRRORED = ("client.py", "services")

# unasync rewrites tokens, but it cannot restructure code. These plain
# str.replace fixes are applied to the *generated* files after rendering.
# Keys are repo-root-relative paths into the generated trees; values are
# ordered (old, new) replacement pairs.
POST_SYNC_FIXES = {
    "appwrite_sync/client.py": {
        # Only the async paths need these imports.
        "import anyio\nimport inspect\n": "",
        # Reading a chunk was offloaded to a worker thread; call it directly.
        "anyio.to_thread.run_sync(read_chunk, chunk['start'], chunk['end'])": (
            "read_chunk(chunk['start'], chunk['end'])"
        ),
        # Sync mode uploads the remaining chunks sequentially, so the
        # semaphore and the task group below are dropped in favour of a
        # plain loop.
        "        semaphore = anyio.Semaphore(8)\n"
        "\n"
        "        failures = []": "        failures = []",
        "                with semaphore:\n"
        "                    chunk_result = upload_chunk(chunk, upload_id_header)": (
            "                chunk_result = upload_chunk(chunk, upload_id_header)"
        ),
        "            # a task group cancels siblings on the first raise, so failures,\n"
        "            # including ones raised by the progress callback, are captured here\n"
        "            # to keep gather(return_exceptions=True) semantics.": (
            "            # failures are captured so every remaining chunk is still\n"
            "            # attempted before the first error is raised."
        ),
        "        # Wait for every sibling chunk to settle before surfacing a failure, so the\n"
        "        # caller never observes an error while other chunks are still being written.\n"
        "        with anyio.create_task_group() as tg:\n"
        "            for chunk in chunks[1:]:\n"
        "                tg.start_soon(upload_remaining_chunk, chunk)": (
            "        # Sync mode has no concurrency; upload the remaining chunks in order.\n"
            "        for chunk in chunks[1:]:\n"
            "            upload_remaining_chunk(chunk)"
        ),
        "Invoke the progress callback, awaiting it when it is a coroutine.": (
            "Invoke the progress callback."
        ),
        "        result = on_progress(payload)\n"
        "        if inspect.isawaitable(result):\n"
        "            result": "        on_progress(payload)",
        "        # anyio has no fire-and-forget tasks, so the replaced client is parked here\n"
        "        # and closed together with the active one once aclose() runs.": (
            "        # the replaced client is parked here and closed together with the\n"
            "        # active one once close() runs."
        ),
    },
    # unasync also rewrites string literals whose *entire* content matches a
    # replacement key, which would corrupt values sent to the server; these
    # fixes restore them.
    "appwrite_sync/enums/o_auth_provider.py": {
        'APPWRITE = "appwrite_sync"': 'APPWRITE = "appwrite"',
    },
    "appwrite_sync/enums/project_o_auth_provider_id.py": {
        'APPWRITE = "appwrite_sync"': 'APPWRITE = "appwrite"',
    },
    "appwrite_sync/models/organization.py": {
        "data['platform'] = 'appwrite_sync'": "data['platform'] = 'appwrite'",
    },
    "test_sync/test_client.py": {
        # Concurrency cannot be asserted in a sync mirror: drop the
        # asyncio.gather()-based test, then redirect the remaining
        # asyncio.sleep() calls in handlers to time.sleep().
        "    @respx.mock\n"
        "    def test_requests_are_served_concurrently(self):\n"
        "        in_flight = 0\n"
        "        peak = 0\n"
        "\n"
        "        def handler(request):\n"
        "            nonlocal in_flight, peak\n"
        "            in_flight += 1\n"
        "            peak = max(peak, in_flight)\n"
        "            asyncio.sleep(0.05)\n"
        "            in_flight -= 1\n"
        "            return httpx2.Response(200, json={'$id': 'user-1'}, headers={'Content-Type': 'application/json'})\n"
        "\n"
        "        respx.route().mock(side_effect=handler)\n"
        "\n"
        "        with Client() as client:\n"
        "            responses = asyncio.gather(\n"
        "                *[client.call('get', f'/users/{index}', {'accept': 'application/json'}) for index in range(5)]\n"
        "            )\n"
        "\n"
        "        self.assertEqual(len(responses), 5)\n"
        "        self.assertEqual(peak, 5)\n"
        "\n": "",
        "import asyncio\nimport unittest\n": "import time\nimport unittest\n",
        "asyncio.sleep(": "time.sleep(",
    },
    "test_sync/test_deprecated.py": {
        "import asyncio\n": "import time\n",
        "asyncio.sleep(0)": "time.sleep(0)",
    },
    "test_sync/test_query.py": {
        # aread() is the async API of httpx2's Request; the sync mirror
        # must read the request body with read().
        "json_request.aread()": "json_request.read()",
        "multipart_request.aread()": "multipart_request.read()",
    },
    "test_sync/test_integration.py": {
        "import asyncio\nimport hashlib\n": "import hashlib\n",
        # Concurrency cannot be asserted in a sync mirror: drop the two
        # asyncio.gather()-based tests of TestRealConcurrency.
        "    def test_requests_overlap_on_the_wire(self):\n"
        "        \"\"\"Sequential calls pay the delay every time; concurrent calls overlap.\"\"\"\n"
        "        count = 8\n"
        "        delay = 0.25\n"
        "\n"
        "        self.state.reset()\n"
        "        started = time.perf_counter()\n"
        "        for _ in range(count):\n"
        "            self.client.call('get', '/slow', {}, {'delay': str(delay)})\n"
        "        sequential = time.perf_counter() - started\n"
        "\n"
        "        self.state.reset()\n"
        "        started = time.perf_counter()\n"
        "        asyncio.gather(*[self.client.call('get', '/slow', {}, {'delay': str(delay)}) for _ in range(count)])\n"
        "        concurrent = time.perf_counter() - started\n"
        "\n"
        "        self.assertGreater(sequential, delay * count * 0.9, 'sequential baseline should pay the delay every time')\n"
        "        self.assertLess(concurrent, sequential / 3, 'concurrent calls should overlap instead of queueing')\n"
        "        self.assertGreater(self.state.peak_in_flight, 1, 'the server never handled two requests at once')\n"
        "\n": "",
        "    def test_each_concurrent_request_gets_its_own_connection(self):\n"
        "        count = 6\n"
        "        self.state.reset()\n"
        "\n"
        "        asyncio.gather(*[self.client.call('get', '/slow', {}, {'delay': '0.2'}) for _ in range(count)])\n"
        "\n"
        "        self.assertEqual(self.state.requests, count)\n"
        "        self.assertEqual(self.state.connections, count, 'requests were serialised onto a single connection')\n"
        "\n": "",
        # There is no asyncio.wait_for in sync mode; call() already raises
        # AppwriteException on its own when the endpoint is unreachable.
        "asyncio.wait_for(client.call('get', '/health'), timeout=20)": (
            "client.call('get', '/health')"
        ),
    },
}

# The generated mirror must be fully synchronous.
ASYNC_REMNANTS = ("anyio", "asyncio", "await ", "async def", "aclose")

# The async services declare the class name the mirror has to use.
SERVICE_CLASS = re.compile(r"^class (Async[A-Za-z0-9_]+)\(Service\):", re.MULTILINE)


def service_replacements(repo_root):
    """The token renames for the async services, taken from the classes they declare."""
    replacements = {}
    services_dir = os.path.join(repo_root, "appwrite", "async_services")

    for filename in sorted(os.listdir(services_dir)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        with open(os.path.join(services_dir, filename), "r", encoding="utf-8") as f:
            match = SERVICE_CLASS.search(f.read())

        if match is None:
            raise SystemExit(f"no async service class found in {filename}")

        name = match.group(1)
        plain = name[len("Async") :]
        replacements[name] = plain
        replacements[f"{name}ServiceTest"] = f"{plain}ServiceTest"

    return replacements


def collect_source_files(repo_root):
    filepaths = []
    for source_dir in ("appwrite", "test_async"):
        for root, dirs, files in os.walk(os.path.join(repo_root, source_dir)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for filename in files:
                if not filename.endswith(".py"):
                    continue

                path = os.path.join(root, filename)
                relative = os.path.relpath(path, repo_root)
                parts = relative.split(os.sep)
                if parts[0] == "appwrite" and parts[1] in NOT_MIRRORED:
                    continue

                filepaths.append(path)
    return filepaths


def apply_post_sync_fixes(repo_root):
    for relative_path, replacements in POST_SYNC_FIXES.items():
        path = os.path.join(repo_root, *relative_path.split("/"))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        for old, new in replacements.items():
            if old not in content:
                raise SystemExit(f"post-sync fix no longer matches {relative_path}:\n{old}")
            content = content.replace(old, new)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)


def assert_no_async_remnants(repo_root):
    offenders = []
    for generated in ("appwrite_sync", "test_sync"):
        for root, dirs, files in os.walk(os.path.join(repo_root, generated)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for filename in files:
                if not filename.endswith(".py"):
                    continue
                path = os.path.join(root, filename)
                with open(path, "r", encoding="utf-8") as f:
                    for lineno, line in enumerate(f, start=1):
                        if any(pattern in line for pattern in ASYNC_REMNANTS):
                            offenders.append(f"{os.path.relpath(path, repo_root)}:{lineno}: {line.strip()}")
    if offenders:
        raise SystemExit("async remnants found in the generated mirror:\n" + "\n".join(offenders))


def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))

    replacements = dict(ADDITIONAL_REPLACEMENTS)
    replacements.update(service_replacements(repo_root))

    rules = [
        unasync.Rule(
            fromdir="/appwrite/async_client.py",
            todir="/appwrite_sync/client.py",
            additional_replacements=replacements,
        ),
        unasync.Rule(
            fromdir="/appwrite/async_services/",
            todir="/appwrite_sync/services/",
            additional_replacements=replacements,
        ),
        unasync.Rule(
            fromdir="/appwrite/",
            todir="/appwrite_sync/",
            additional_replacements=replacements,
        ),
        unasync.Rule(
            fromdir="/test_async/",
            todir="/test_sync/",
            additional_replacements=replacements,
        ),
    ]

    # The mirror is disposable output: wipe it so stale files from sources
    # that were renamed or removed never linger.
    for generated in ("appwrite_sync", "test_sync"):
        generated_dir = os.path.join(repo_root, generated)
        if os.path.isdir(generated_dir):
            shutil.rmtree(generated_dir)

    filepaths = collect_source_files(repo_root)
    unasync.unasync_files(filepaths, rules)

    apply_post_sync_fixes(repo_root)
    assert_no_async_remnants(repo_root)

    print(f"Generated appwrite_sync/ and test_sync/ from {len(filepaths)} source files.")


if __name__ == "__main__":
    main()
