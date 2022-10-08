CREATE SCHEMA IF NOT EXISTS "edsm-mirror";

CREATE TABLE IF NOT EXISTS "edsm-mirror"."system"
(
    "key"           jsonb PRIMARY KEY,
    "name"          text,
    "coordinates"   jsonb,
    "requirePermit" boolean,
    "information"   jsonb,
    "updateTime"    timestamp,
    "primaryStar"   jsonb
);

CREATE TABLE IF NOT EXISTS "edsm-mirror"."body"
(
    "key"                   jsonb PRIMARY KEY,
    "systemKey"             jsonb,
    "name"                  text,
    "type"                  text,
    "subType"               text,
    "discovery"             jsonb,
    "updateTime"            timestamp,
    "materials"             jsonb,
    "solidComposition"      jsonb,
    "atmosphereComposition" jsonb,
    "parents"               jsonb,
    "belts"                 jsonb,
    "rings"                 jsonb,
    "properties"            jsonb
);

ALTER TABLE "edsm-mirror"."body"
    ADD FOREIGN KEY ("systemKey") REFERENCES "edsm-mirror"."system" ("key");
