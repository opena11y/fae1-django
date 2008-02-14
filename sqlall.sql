BEGIN;
CREATE TABLE "fae_userreport" (
    "id" varchar(30) NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL,
    "pgcount" integer NOT NULL,
    "url" varchar(200) NOT NULL,
    "urlcount" integer NOT NULL,
    "depth" integer NOT NULL,
    "title" varchar(128) NOT NULL,
    "delete" boolean NOT NULL,
    "stats" boolean NOT NULL
);
CREATE TABLE "fae_emailsuffix" (
    "suffix" varchar(128) NOT NULL PRIMARY KEY,
    "org_id" integer NOT NULL
);
CREATE TABLE "fae_usagestats" (
    "date" date NOT NULL PRIMARY KEY,
    "user_reports" integer NOT NULL,
    "user_pgcount" integer NOT NULL,
    "guest_reports" integer NOT NULL,
    "guest_pgcount" integer NOT NULL,
    "depth_2" integer NOT NULL,
    "depth_3" integer NOT NULL
);
CREATE TABLE "fae_guestreport" (
    "id" varchar(30) NOT NULL PRIMARY KEY,
    "timestamp" timestamp with time zone NOT NULL,
    "pgcount" integer NOT NULL,
    "url" varchar(200) NOT NULL,
    "stats" boolean NOT NULL
);
CREATE TABLE "fae_organization" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(128) NOT NULL,
    "org_type" integer NOT NULL,
    "url" varchar(200) NOT NULL
);
ALTER TABLE "fae_emailsuffix" ADD CONSTRAINT org_id_refs_id_225db99c FOREIGN KEY ("org_id") REFERENCES "fae_organization" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "fae_userprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "acct_type" integer NOT NULL,
    "org_id" integer NOT NULL REFERENCES "fae_organization" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reg_date" timestamp with time zone NOT NULL,
    "reg_key" varchar(30) NOT NULL
);
CREATE INDEX fae_userreport_user_id ON "fae_userreport" ("user_id");
CREATE INDEX fae_emailsuffix_org_id ON "fae_emailsuffix" ("org_id");
CREATE UNIQUE INDEX fae_userprofile_user_id ON "fae_userprofile" ("user_id");
CREATE INDEX fae_userprofile_org_id ON "fae_userprofile" ("org_id");
COMMIT;
