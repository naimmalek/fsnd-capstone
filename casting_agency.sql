-- Adminer 4.8.1 PostgreSQL 12.7 (Ubuntu 12.7-0ubuntu0.20.04.1) dump

DROP TABLE IF EXISTS "actor_in_movie";
CREATE TABLE "public"."actor_in_movie" (
    "actor_id" integer NOT NULL,
    "movie_id" integer NOT NULL,
    CONSTRAINT "actor_in_movie_pkey" PRIMARY KEY ("actor_id", "movie_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "actors";
DROP SEQUENCE IF EXISTS actors_id_seq;
CREATE SEQUENCE actors_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."actors" (
    "id" integer DEFAULT nextval('actors_id_seq') NOT NULL,
    "full_name" character varying,
    "date_of_birth" date NOT NULL,
    CONSTRAINT "actors_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "actors" ("id", "full_name", "date_of_birth") VALUES
(13,	'James bond',	'1993-06-15'),
(66,	'James bond',	'1993-06-15'),
(67,	'James bond',	'1993-06-15');

DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL,
    CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
) WITH (oids = false);


DROP TABLE IF EXISTS "movies";
DROP SEQUENCE IF EXISTS movies_id_seq;
CREATE SEQUENCE movies_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."movies" (
    "id" integer DEFAULT nextval('movies_id_seq') NOT NULL,
    "title" character varying(256) NOT NULL,
    "release_year" integer NOT NULL,
    "duration" integer NOT NULL,
    "imdb_rating" double precision NOT NULL,
    CONSTRAINT "movies_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "movies" ("id", "title", "release_year", "duration", "imdb_rating") VALUES
(13,	'ett awe',	2005,	20,	9.9),
(22,	'ett rtrtrt',	2005,	20,	9.9);

ALTER TABLE ONLY "public"."actor_in_movie" ADD CONSTRAINT "actor_in_movie_actor_id_fkey" FOREIGN KEY (actor_id) REFERENCES actors(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."actor_in_movie" ADD CONSTRAINT "actor_in_movie_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movies(id) NOT DEFERRABLE;

-- 2021-06-30 16:40:32.846665+05:30
