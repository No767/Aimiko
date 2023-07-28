import os
import sys
from pathlib import Path

import asyncpg
import pytest
from dotenv import load_dotenv

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

load_dotenv()

from libs.utils import ensure_pg_conn


@pytest.fixture(scope="session")
def get_uri():
    pg_uri = os.getenv("POSTGRES_URI")
    if pg_uri is None:
        return "postgresql://postgres:postgres@localhost:5432/test"
    return pg_uri


@pytest.mark.asyncio
async def test_ensure_good_conn(get_uri):
    async with asyncpg.create_pool(dsn=get_uri) as pool:
        res = await ensure_pg_conn(conn_pool=pool)
        assert res is True
