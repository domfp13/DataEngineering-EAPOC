-- -*- coding: utf-8 -*-
-- This is the database model
-- Created by Luis Enrique Fuentes Plata

USE UDC;

CREATE WAREHOUSE UDC_XS WITH 
    WAREHOUSE_SIZE = 'XSMALL' 
    WAREHOUSE_TYPE = 'STANDARD' 
    AUTO_SUSPEND = 60 
    AUTO_RESUME = TRUE 
    MIN_CLUSTER_COUNT = 1 
    MAX_CLUSTER_COUNT = 2 
    SCALING_POLICY = 'ECONOMY' 
    COMMENT = 'X-Small VW with mximum of 2 servers, Scaling policy: Economy, Auto Suspend: 1 min';

USE WAREHOUSE UDC_XS;

CREATE SCHEMA WEBAPP;

USE SCHEMA WEBAPP;

-- 1.- Creating Tables
CREATE OR REPLACE TABLE TECHNOLOGY_CAPABILITY (
    technology_capability_id NUMBER(38,0) IDENTITY NOT NULL PRIMARY KEY,
    technology_capability_name VARCHAR(50) NOT NULL
)

CREATE OR REPLACE TABLE TECHNOLOGY_STACK (
    technology_stack_id NUMBER(38,0) IDENTITY NOT NULL PRIMARY KEY,
    technology_stack_name VARCHAR(40) NOT NULL,
    technology_capability_id NUMBER(38,0) NOT NULL,
    CONSTRAINT fkey_1 FOREIGN KEY (technology_capability_id) REFERENCES TECHNOLOGY_CAPABILITY (technology_capability_id) ENFORCED
)

-- 2.- Inserting data into tables
BEGIN TRANSACTION NAME t1;

    INSERT INTO TECHNOLOGY_CAPABILITY (technology_capability_name) 
     VALUES ('Backend'),('Infrastructure'),('Data');
    
COMMIT;

BEGIN TRANSACTION NAME t2;

    INSERT INTO TECHNOLOGY_STACK (technology_stack_name, technology_capability_id) 
     VALUES ('Docker',2),('AWS',2),('Nginx',2);
    
COMMIT;

SELECT * FROM TECHNOLOGY_CAPABILITY;
SELECT * FROM TECHNOLOGY_STACK;

-- 3.- Stored Procedure to insert data into TECHNOLOGY_STACK
CREATE OR REPLACE PROCEDURE SPW_INSERT_TECHNOLOGY_STACK(technology_stack_name STRING, technology_capability_id FLOAT)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS
$$

// 01.- Setting up operation variables
var technology_stack_name_t = TECHNOLOGY_STACK_NAME;
var technology_capability_id_t = TECHNOLOGY_CAPABILITY_ID;
var return_value = "";
var col_value;

// 02- Inner logic
try {

    // 03.- Getting the number of rows that match
    cmd = "SELECT COUNT(*)\
           FROM TECHNOLOGY_STACK\
           WHERE technology_stack_name = :1\
            AND technology_capability_id = :2\
          ";
    stmt = snowflake.createStatement(
            {
            sqlText: cmd, binds: [technology_stack_name_t, technology_capability_id_t]
            }
        );
    rs = stmt.execute();

    while (rs.next()) {

        col_value = rs.getColumnValue(1);

        // 04.- Checking if the row was already added
        if (col_value == 0) {
            insert_cmd = "INSERT INTO TECHNOLOGY_STACK (technology_stack_name, technology_capability_id) VALUES(:1, :2)";
            snowflake.execute(
                {
                    sqlText: insert_cmd,
                    binds: [technology_stack_name_t, technology_capability_id_t]
                }
            );
            
            return_value = "INSERT";
        } else {
            return_value = "NO-ACTION";
        }
    }

} catch (err) {
    return_value = "FAIL";
}

return return_value;

$$
;

CALL SPW_INSERT_TECHNOLOGY_STACK('Python', 1);

-- Selecting some of the data from the db
SELECT * FROM TECHNOLOGY_CAPABILITY;
SELECT * FROM TECHNOLOGY_STACK;

-- 4.- Dashboard PowerBi
SELECT s.technology_stack_name,
       c.technology_capability_name
FROM TECHNOLOGY_STACK s
LEFT JOIN TECHNOLOGY_CAPABILITY c
 ON s.technology_capability_id = c.technology_capability_id;
 
