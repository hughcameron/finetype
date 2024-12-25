
CREATE    TABLE type_domain AS
SELECT    *,
          ROW_NUMBER() OVER (
          PARTITION BY label
          ) AS id
FROM      read_json (
          'labels/learning_data/type_domain.ndjson',
          FORMAT = 'newline_delimited',
          COLUMNS = {"label": "string", "provider": "string", "method": "string", "locale": "string", "value": "string"}
          );


COPY      (
SELECT    label,
          provider,
          method,
          locale,
          value
FROM      type_domain
WHERE     id % 5 != 1
) TO 'labels/learning_data/train.parquet'
WITH      (FORMAT 'parquet');


COPY      (
SELECT    label,
          provider,
          method,
          locale,
          value
FROM      type_domain
WHERE     id % 5 = 1
) TO 'labels/learning_data/test.parquet'
WITH      (FORMAT 'parquet');


-- Export to SQLite

INSTALL sqlite;
LOAD sqlite;

ATTACH 'database.sqlite' AS fifa (TYPE sqlite);
USE fifa;
