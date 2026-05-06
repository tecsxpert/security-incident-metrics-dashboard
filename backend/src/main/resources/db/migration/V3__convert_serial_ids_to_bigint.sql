ALTER TABLE app_users ALTER COLUMN id TYPE bigint;
ALTER SEQUENCE app_users_id_seq AS bigint;

ALTER TABLE audit_log ALTER COLUMN id TYPE bigint;
ALTER SEQUENCE audit_log_id_seq AS bigint;
