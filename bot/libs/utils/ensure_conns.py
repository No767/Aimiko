import logging
from typing import Literal

import asyncpg


async def ensure_pg_conn(pool: asyncpg.Pool) -> Literal[True]:
    """Ensures that the current connection pulled from the pool can be ran.

    Args:
        pool (asyncpg.Pool): Asyncpg connection pool
    """
    logger = logging.getLogger("discord")
    async with pool.acquire() as conn:
        status = conn.is_closed()
        if status is False:
            logger.info("PostgreSQL server is up")
        return True
