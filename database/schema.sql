-- Dropping all of the tables
DROP TABLE IF EXISTS "game" CASCADE;
DROP TABLE IF EXISTS "genre" CASCADE;
DROP TABLE IF EXISTS "genre_game_platform_assignment" CASCADE;
DROP TABLE IF EXISTS "publisher" CASCADE;
DROP TABLE IF EXISTS "developer" CASCADE;
DROP TABLE IF EXISTS "tag" CASCADE;
DROP TABLE IF EXISTS "tag_game_platform_assignment" CASCADE;
DROP TABLE IF EXISTS "game_platform_assignment" CASCADE;
DROP TABLE IF EXISTS "platform" CASCADE;
DROP TABLE IF EXISTS "developer_game_assignment" CASCADE;
DROP TABLE IF EXISTS "publisher_game_assignment" CASCADE;
DROP TABLE IF EXISTS "age_rating" CASCADE;

-- Creating all of the tables

CREATE TABLE "game"(
    "game_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "game_name" VARCHAR(100) NOT NULL,
    "game_image" VARCHAR(255) NOT NULL,
    "age_rating_id" SMALLINT NOT NULL,
    "is_nsfw" BOOLEAN NOT NULL
);

CREATE TABLE "genre"(
    "genre_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "genre_name" VARCHAR(50) NOT NULL
);

CREATE TABLE "genre_game_platform_assignment"(
    "genre_game_platform_assignment_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "genre_id" SMALLINT NOT NULL,
    "platform_assignment_id" SMALLINT NOT NULL
);

CREATE TABLE "publisher"(
    "publisher_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "publisher_name" VARCHAR(150) NOT NULL
);

CREATE TABLE "developer"(
    "developer_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "developer_name" VARCHAR(150) NOT NULL
);

CREATE TABLE "tag"(
    "tag_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "tag_name" VARCHAR(50) NOT NULL
);

CREATE TABLE "tag_game_platform_assignment"(
    "tag_game_platform_assignment_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "tag_id" SMALLINT NOT NULL,
    "platform_assignment_id" SMALLINT NOT NULL
);

CREATE TABLE "game_platform_assignment"(
    "platform_assignment_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "game_id" SMALLINT NOT NULL,
    "platform_id" SMALLINT NOT NULL,
    "platform_release_date" DATE NOT NULL,
    "platform_score" SMALLINT NOT NULL,
    "platform_price" SMALLINT NOT NULL,
    "platform_discount" SMALLINT NOT NULL,
    "platform_url" VARCHAR(255) NOT NULL
);

CREATE TABLE "platform"(
    "platform_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "platform_name" VARCHAR(20) NOT NULL
);

CREATE TABLE "developer_game_assignment"(
    "developer_game_assignment_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "developer_id" SMALLINT NOT NULL,
    "game_id" SMALLINT NOT NULL
);

CREATE TABLE "publisher_game_assignment"(
    "publisher_game_assignment_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "publisher_id" SMALLINT NOT NULL,
    "game_id" SMALLINT NOT NULL
);

-- Creating the Age Rating Table
CREATE TABLE "age_rating"(
    "age_rating_id" SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    "age_rating_name" VARCHAR(25) NOT NULL
);

-- Adding all of the constraints for each table

-- Developer Game Assignment
ALTER TABLE "developer_game_assignment" 
    ADD CONSTRAINT "developer_game_assignment_game_id_foreign" 
    FOREIGN KEY("game_id") REFERENCES "game"("game_id");

ALTER TABLE "developer_game_assignment" 
    ADD CONSTRAINT "developer_game_assignment_developer_id_foreign" 
    FOREIGN KEY("developer_id") REFERENCES "developer"("developer_id");

-- Tag Game Platform Assignment
ALTER TABLE "tag_game_platform_assignment" 
    ADD CONSTRAINT "tag_game_platform_assignment_platform_assignment_id_foreign" 
    FOREIGN KEY("platform_assignment_id") REFERENCES "game_platform_assignment"("platform_assignment_id");

ALTER TABLE "tag_game_platform_assignment" 
    ADD CONSTRAINT "tag_game_platform_assignment_tag_id_foreign" 
    FOREIGN KEY("tag_id") REFERENCES "tag"("tag_id");

-- Genre Game Platform Assignment
ALTER TABLE "genre_game_platform_assignment" 
    ADD CONSTRAINT "genre_game_platform_assignment_genre_id_foreign" 
    FOREIGN KEY("genre_id") REFERENCES "genre"("genre_id");

ALTER TABLE "genre_game_platform_assignment" 
    ADD CONSTRAINT "genre_game_platform_assignment_platform_assignment_id_foreign" 
    FOREIGN KEY("platform_assignment_id") REFERENCES "game_platform_assignment"("platform_assignment_id");

-- Game Platform Assignment
ALTER TABLE "game_platform_assignment" 
    ADD CONSTRAINT "game_platform_assignment_platform_id_foreign" 
    FOREIGN KEY("platform_id") REFERENCES "platform"("platform_id");

ALTER TABLE "game_platform_assignment" 
    ADD CONSTRAINT "game_platform_assignment_game_id_foreign" 
    FOREIGN KEY("game_id") REFERENCES "game"("game_id");

-- Publisher Game Assignment
ALTER TABLE "publisher_game_assignment" 
    ADD CONSTRAINT "publisher_game_assignment_game_id_foreign" 
    FOREIGN KEY("game_id") REFERENCES "game"("game_id");

ALTER TABLE "publisher_game_assignment" 
    ADD CONSTRAINT "publisher_game_assignment_publisher_id_foreign" 
    FOREIGN KEY("publisher_id") REFERENCES "publisher"("publisher_id");

-- Seeding all of the data
INSERT INTO "platform" ("platform_name") 
VALUES
    ('Steam'),
    ('Epic Games Store'),
    ('GOG');

INSERT INTO "age_rating" ("age_rating_name")
VALUES
    ('PEGI 3'),
    ('PEGI 7'),
    ('PEGI 12'),
    ('PEGI 16'),
    ('PEGI 18'),
    ('Not Assigned');
