-- Idempotent CKAN Postgres bootstrap

-- 1) Create roles (safe to re-run)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ckan') THEN
    CREATE ROLE ckan LOGIN PASSWORD 'ckan';
  END IF;

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'datastore') THEN
    CREATE ROLE datastore LOGIN PASSWORD 'ckan_datastore';
  END IF;

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'datastore_ro') THEN
    CREATE ROLE datastore_ro LOGIN PASSWORD 'datastore';
  END IF;
END$$;

-- 2) Create databases OUTSIDE a transaction using \gexec
SELECT 'CREATE DATABASE ckan OWNER ckan'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ckan');
\gexec

SELECT 'CREATE DATABASE datastore OWNER datastore'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'datastore');
\gexec

-- 3) Datastore grants, extension, and defaults (safe to re-run)
\connect datastore

CREATE EXTENSION IF NOT EXISTS hstore;

-- Lock down DB-wide defaults and then grant explicit privileges
REVOKE ALL ON DATABASE datastore FROM PUBLIC;
-- CKAN needs to be able to connect and create TEMP tables during checks
GRANT CONNECT, TEMP ON DATABASE datastore TO ckan;
-- (Optional) allow the RO user to use temp tables; harmless if granted
GRANT CONNECT, TEMP ON DATABASE datastore TO datastore_ro;

-- Schema privileges: only ckan can CREATE, both can USAGE
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO ckan, datastore_ro;
GRANT CREATE ON SCHEMA public TO ckan;
REVOKE CREATE ON SCHEMA public FROM datastore_ro;

-- Existing objects
GRANT ALL    ON ALL TABLES    IN SCHEMA public TO ckan;
GRANT SELECT ON ALL TABLES    IN SCHEMA public TO datastore_ro;

GRANT ALL           ON ALL SEQUENCES IN SCHEMA public TO ckan;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO datastore_ro;

-- Default privileges for future objects CREATED BY ckan
ALTER DEFAULT PRIVILEGES FOR ROLE ckan IN SCHEMA public
  GRANT ALL    ON TABLES    TO ckan;
ALTER DEFAULT PRIVILEGES FOR ROLE ckan IN SCHEMA public
  GRANT SELECT ON TABLES    TO datastore_ro;

ALTER DEFAULT PRIVILEGES FOR ROLE ckan IN SCHEMA public
  GRANT ALL           ON SEQUENCES TO ckan;
ALTER DEFAULT PRIVILEGES FOR ROLE ckan IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO datastore_ro;
