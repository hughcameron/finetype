INSTALL sqlite;
LOAD sqlite;


CREATE TABLE type_domain AS
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY
        tag
    ) AS split,
    DENSE_RANK() OVER (
        ORDER BY
        tag
    ) - 1 AS label
FROM
read_json (
    'labels/learning_data/type_domain.ndjson',
    FORMAT = 'newline_delimited',
    COLUMNS = {"tag": "string", "provider": "string", "method": "string", "locale": "string", "text": "string"});

-- Attach the SQLite database
ATTACH '/Users/hugh/.cache/burn-dataset/hughcameronfinetype_01.db' AS finetype (TYPE SQLITE);

CREATE TABLE train AS
SELECT
    ROW_NUMBER() OVER () AS row_id,
    label,
    tag,
    provider,
    method,
    locale,
    text
FROM
    type_domain
    WHERE split % 5 != 1
    ;

CREATE TABLE test AS
SELECT
    ROW_NUMBER() OVER () AS row_id,
    label,
    tag,
    provider,
    method,
    locale,
    text
FROM
    type_domain
    WHERE split % 5 = 1
    ;


CREATE
OR REPLACE TABLE finetype.test (
    row_id INTEGER,
    label INTEGER,
    tag VARCHAR,
    provider VARCHAR,
    method VARCHAR,
    locale VARCHAR,
    text VARCHAR
);

-- Insert data from the DuckDB table into the SQLite table
INSERT INTO
    finetype.test
SELECT
    *
FROM
    test;


CREATE
    OR REPLACE TABLE finetype.train (
        row_id INTEGER,
        label INTEGER,
        tag VARCHAR,
        provider VARCHAR,
        method VARCHAR,
        locale VARCHAR,
        text VARCHAR
    );


INSERT INTO
    finetype.train
SELECT
    *
FROM
    train;


CREATE
    OR REPLACE TABLE finetype.labels (
        label INTEGER,
        tag VARCHAR
    );


INSERT INTO
    finetype.labels
SELECT
distinct
    label,
    tag
    from type_domain;

COPY (
    SELECT
        *
    FROM
        train
) TO 'labels/learning_data/train.parquet'
WITH
    (FORMAT 'parquet');

COPY (
    SELECT
        *
    FROM
        test
) TO 'labels/learning_data/test.parquet'
WITH
    (FORMAT 'parquet');


COPY (select distinct label, tag from type_domain order by label)
TO 'labels/learning_data/labels.parquet' WITH (FORMAT 'parquet')
;
