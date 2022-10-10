-- depends: 001.initial-db-creation

CREATE TABLE IF NOT EXISTS "edsm-mirror"."sync_state"
(
    "key"       jsonb PRIMARY KEY,
    "sync_date" timestamp,
    "type"      text,
    "sync_hash" text
);
