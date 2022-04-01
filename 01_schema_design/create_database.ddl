CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_rating_idx ON content.film_work (creation_date, rating);
CREATE INDEX IF NOT EXISTS film_work_title_idx ON content.film_work (title);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
	film_work_id uuid NOT NULL,
    created timestamp with time zone,
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone,
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id);

ALTER TABLE content.genre_film_work ADD CONSTRAINT genre_film_work_film_work_id_genre_id_uniq UNIQUE (film_work_id, genre_id);
ALTER TABLE content.person_film_work ADD CONSTRAINT person_film_work_film_work_id_person_id_uniq UNIQUE (film_work_id, person_id);

ALTER ROLE app SET search_path TO content,public;