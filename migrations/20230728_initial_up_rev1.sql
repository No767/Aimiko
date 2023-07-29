CREATE TABLE IF NOT EXISTS guild (
    id BIGINT PRIMARY KEY,
    prefix VARCHAR(255)[],
    ping_checks_channel BIGINT
);

CREATE INDEX IF NOT EXISTS guild_prefix_idx ON guild USING GIN (prefixes);