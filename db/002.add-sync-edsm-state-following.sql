-- depends: 001.initial-db-creation

CREATE TABLE IF NOT EXISTS "edsm-mirror"."sync_state"
(
    "key"            jsonb PRIMARY KEY,
    "sync_date"      timestamp not null,
    "type"           text      not null,
    "sync_hash"      text,
    "previous_state" jsonb
);
