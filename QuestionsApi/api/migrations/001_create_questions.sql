CREATE TABLE categories (
    name TEXT PRIMARY KEY
);

CREATE TABLE questions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category TEXT NOT NULL REFERENCES categories (name),
    question TEXT NOT NULL
);

CREATE INDEX questions_category_idx ON questions (category);
