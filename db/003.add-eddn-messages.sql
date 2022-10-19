-- depends: 001.initial-db-creation

CREATE TABLE IF NOT EXISTS "edsm-mirror"."eddn_message"
(
    "id"        uuid PRIMARY KEY default uuid_generate_v4(),
    "schema"    text      not null,
    "header"    jsonb     not null,
    "message"   jsonb     not null,
    "recv_date" timestamp not null,
    "sync_date" timestamp
);
