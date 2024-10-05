CREATE
OR        REPLACE TABLE type_domain AS
          SELECT    *
          FROM      read_json (
                    'data/type_domain.ndjson',
                    FORMAT = 'newline_delimited'
                    )
          WHERE     value IS NOT NULL;


COPY      type_domain TO 'data/type_domain.parquet'
WITH      (FORMAT 'parquet');


-- SELECT    *
-- FROM      type_domain
-- LIMIT     10;
-- SELECT    DISTINCT provider_name, method
-- FROM      type_domain;
-- SELECT    provider_name, method, count(*) as records
-- FROM      type_domain
-- GROUP BY  provider_name, method;
--
CREATE
OR        REPLACE TABLE overlap AS
          WITH      matches AS (
                    SELECT    provider_name,
                              method,
                              ROW_NUMBER() OVER (
                              PARTITION BY value
                              ) AS value_matches
                    FROM      type_domain
                    )
          SELECT    provider_name,
                    method,
                    MAX(value_matches) AS coincidence
          FROM      matches
          GROUP BY  provider_name,
                    method
          ORDER BY  coincidence DESC;


COPY      overlap TO 'overlap.csv'
WITH      (sep ',', header TRUE);


COPY      (
SELECT    provider_name,
          list (DISTINCT method) AS methods
FROM      type_domain
GROUP BY  provider_name
ORDER BY  provider_name
) TO 'overlap.json'
WITH      (ARRAY TRUE);
