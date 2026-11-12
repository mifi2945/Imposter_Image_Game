CREATE TABLE categories (
    name TEXT PRIMARY KEY
);

INSERT INTO categories (name)
SELECT DISTINCT category
FROM questions;

ALTER TABLE questions
ADD CONSTRAINT questions_category_fkey
FOREIGN KEY (category) REFERENCES categories (name);

CREATE INDEX questions_category_idx ON questions (category);
