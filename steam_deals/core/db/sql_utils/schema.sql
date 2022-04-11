BEGIN;

DROP TABLE IF EXISTS public.users;
CREATE TABLE IF NOT EXISTS public.users
(
    username        text                        NOT NULL,
    email           text                        NOT NULL,
    hashed_password text                        NOT NULL,
    "timestamp"     timestamp without time zone NOT NULL,
    first_name      text                        NOT NULL,
    last_name       text                        NOT NULL,
    disabled        boolean                     NOT NULL DEFAULT false,
    admin           boolean                     NOT NULL DEFAULT false,
    verified        boolean                     NOT NULL DEFAULT false,
    PRIMARY KEY (username)
);

DROP INDEX IF EXISTS ix_users_username;
CREATE INDEX ix_users_username ON public.users(username);

DROP INDEX IF EXISTS ix_users_email;
CREATE INDEX ix_users_email ON public.users(email);

END;
