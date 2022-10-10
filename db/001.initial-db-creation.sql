CREATE SCHEMA IF NOT EXISTS "edsm-mirror";

CREATE TABLE IF NOT EXISTS "edsm-mirror"."system"
(
    "key"            jsonb PRIMARY KEY,
    "name"           text,
    "coordinates"    jsonb,
    "require_permit" boolean,
    "information"    jsonb,
    "update_time"    timestamp,
    "primary_star"   jsonb
);

CREATE TABLE IF NOT EXISTS "edsm-mirror"."body"
(
    "key"                    jsonb PRIMARY KEY,
    "system_key"             jsonb,
    "name"                   text,
    "type"                   text,
    "sub_type"               text,
    "discovery"              jsonb,
    "update_time"            timestamp,
    "materials"              jsonb,
    "solid_composition"      jsonb,
    "atmosphere_composition" jsonb,
    "parents"                jsonb,
    "belts"                  jsonb,
    "rings"                  jsonb,
    "properties"             jsonb
);

ALTER TABLE "edsm-mirror"."body"
    ADD FOREIGN KEY (system_key) REFERENCES "edsm-mirror"."system" (key);
