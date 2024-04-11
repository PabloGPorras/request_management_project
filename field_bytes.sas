/* Set up the Snowflake ODBC connection */
libname mydblib odbc dsn='your_dsn' user='your_username' password='your_password';

/* Define the table and date range */
%let table_name = transaction_table;
%let start_date = '2023-03-01';
%let end_date = '2023-03-31';

/* Create a result table in Snowflake */
proc sql;
    connect to odbc (dsn='your_dsn' user='your_username' password='your_password');
    execute (
        create or replace table byte_analysis_results (
            field_name varchar(255),
            byte_position int,
            byte_value varchar(1),
            occurrence_count int
        )
    ) by odbc;
    disconnect from odbc;
quit;

/* Fetch the list of fields */
proc sql noprint;
    connect to odbc (dsn='your_dsn' user='your_username' password='your_password');
    create table fields as select * from connection to odbc (
        select column_name, character_maximum_length 
        from information_schema.columns 
        where table_name = '" || trim(&table_name) || "'

    );
    disconnect from odbc;
quit;

/* Loop through fields and byte positions */
data _null_;
    set fields;
    if character_maximum_length > 0 then do; /* Check that character_maximum_length is positive */
        do byte_position = 1 to character_maximum_length;
            query = cats(
                "insert into byte_analysis_results (field_name, byte_position, byte_value, occurrence_count) ",
                "select '", column_name, "' as field_name, ", byte_position, " as byte_position, byte_substr(", column_name, ", ", byte_position, ", 1) as byte_value, count(*) as occurrence_count ",
                "from ", symget('table_name'), " ",  /* Use symget to retrieve the macro variable value */
                "where transaction_date between '", symget('start_date'), "' and '", symget('end_date'), "' ",
                "group by byte_value order by byte_value"
            );
            /* Store the query for later execution */
            call symputx(cats('query',byte_position), query);
        end;
    end;
    else put "WARNING: Invalid character_maximum_length for field " column_name;
run;


/* Execute the stored queries */
%macro execute_queries;
    %do i = 1 %to &sqlobs;
        %let current_query = &&query&i;
        proc sql;
            connect to odbc (dsn='your_dsn' user='your_username' password='your_password');
            execute (&current_query) by odbc;
            disconnect from odbc;
        quit;
    %end;
%mend execute_queries;

%execute_queries;
