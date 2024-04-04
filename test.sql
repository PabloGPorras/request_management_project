WITH rule_lines AS (
    SELECT 
        base_rule_id,
        rule_name,
        rule_state,
        line_number,
        line AS rule_code
    FROM 
        your_table,
        LATERAL SPLIT_TO_TABLE(rule_code, '\n') as t(line_number, line)
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
        rule_lines a
    FULL OUTER JOIN
        rule_lines b
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
