WITH rule_changes AS (
    SELECT 
        base_rule_id,
        rule_name,
        rule_code,
        rule_state,
        ROW_NUMBER() OVER (PARTITION BY base_rule_id, rule_name ORDER BY rule_state DESC) AS line_number
    FROM 
        your_table
    WHERE
        rule_state IN ('testing', 'coding', 'production')
),
diffs AS (
    SELECT
        a.base_rule_id,
        a.rule_name,
        CASE
            WHEN a.rule_code IS NULL THEN 'delete'
            WHEN b.rule_code IS NULL THEN 'insert'
            ELSE 'update'
        END AS change_type,
        a.line_number,
        a.rule_state,
        a.rule_code AS line_details
    FROM
        rule_changes a
    FULL OUTER JOIN
        rule_changes b
    ON
        a.base_rule_id = b.base_rule_id
        AND a.rule_name = b.rule_name
        AND a.line_number = b.line_number
        AND a.rule_state = 'testing/coding'
        AND b.rule_state = 'production'
    WHERE
        a.rule_code <> b.rule_code
        OR a.rule_code IS NULL
        OR b.rule_code IS NULL
)
SELECT
    *
FROM
    diffs
ORDER BY
    base_rule_id,
    rule_name,
    line_number;
