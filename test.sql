WITH RulePairs AS (
    SELECT
        base_rule_id,
        rule_name,
        MAX(CASE WHEN rule_state = 'production' THEN rule_code ELSE NULL END) AS prod_code,
        MAX(CASE WHEN rule_state IN ('coding', 'testing') THEN rule_code ELSE NULL END) AS test_code
    FROM
        your_table
    GROUP BY
        base_rule_id,
        rule_name
    HAVING
        COUNT(DISTINCT rule_state) = 2
),
CodeDiffs AS (
    SELECT
        base_rule_id,
        rule_name,
        SPLIT_PART(prod_code, '\n', seq) AS prod_line,
        SPLIT_PART(test_code, '\n', seq) AS test_line,
        seq AS line_number
    FROM
        RulePairs,
        TABLE(FLATTEN(INPUT => SEQ8(), OUTER => TRUE)) seq8
    WHERE
        seq8.seq <= GREATEST(ARRAY_SIZE(SPLIT(prod_code, '\n')), ARRAY_SIZE(SPLIT(test_code, '\n')))
)
SELECT
    base_rule_id,
    rule_name,
    IFF(prod_line IS NULL, 'inserts', IFF(test_line IS NULL, 'deletes', 'updates')) AS change_type,
    IFF(prod_line IS NULL, CONCAT('new line ', line_number, ': ', test_line),
        IFF(test_line IS NULL, CONCAT('deleted line ', line_number, ': ', prod_line),
            CONCAT('previous line ', line_number, ': ', prod_line, '\nnew line ', line_number, ': ', test_line)
        )
    ) AS change_details
FROM
    CodeDiffs
WHERE
    prod_line IS DISTINCT FROM test_line
ORDER BY
    base_rule_id,
    line_number;
