CREATE TABLE
    IF NOT EXISTS image_metadata (
        id serial PRIMARY KEY,
        extension text NOT NULL,
        width integer NOT NULL,
        height integer NOT NULL,
        created_at timestamptz NOT NULL
    )