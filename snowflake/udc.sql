-- -*- coding: utf-8 -*-
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

CREATE OR REPLACE TABLE EMPLOYEE (
  name VARCHAR(25) NOT NULL,
  last_name VARCHAR(25) NOT NULL,
  title VARCHAR(25) NOT NULL, 
  inserted_date DATE NOT NULL
);

BEGIN TRANSACTION NAME t1;

    SELECT current_transaction();
    
    INSERT INTO EMPLOYEE (name, last_name, title, inserted_date) VALUES 
        ('Luis', 'Fuentes', 'Business Systems III', to_date('2020.12.13', 'YYYY.MM.DD')),
        ('Ana', 'Espadas', 'Portfolio Advisor III', current_date());
COMMIT;


ALTER USER IF EXISTS AESPADAS SET DEFAULT_ROLE = 'SYSADMIN';
ALTER USER IF EXISTS AESPADAS SET DEFAULT_WAREHOUSE = 'UDC_XS';
ALTER USER IF EXISTS AESPADAS SET DEFAULT_NAMESPACE = 'UDC';

-- 1.- Creating tables for data model

-- Creating file format
CREATE OR REPLACE FILE FORMAT FILE_T_STG_S3 
    TYPE = 'JSON' 
    --COMPRESSION = 'AUTO ' 
    ENABLE_OCTAL = TRUE 
    ALLOW_DUPLICATE = TRUE 
    STRIP_OUTER_ARRAY = TRUE 
    STRIP_NULL_VALUES = TRUE 
    IGNORE_UTF8_ERRORS = FALSE;
    
SHOW FILE FORMATS;

-- Creating stage
-- REMOVE @T_STG_S3;
CREATE OR REPLACE STAGE T_STG_S3 url='s3://domfp13-s3-bucket/network/'
  credentials=(aws_key_id='' aws_secret_key='')
  FILE_FORMAT = FILE_T_STG_S3;

SHOW STAGES;

-- Creating Table with no fail safe
CREATE OR REPLACE TABLE T_LINKS_STG (
    V VARIANT,
    file_name VARCHAR(100) NOT NULL  
);

CREATE OR REPLACE TABLE T_NODES_STG (
    V VARIANT,
    file_name VARCHAR(100) NOT NULL  
);

LIST @T_STG_S3;

-- Loading data
BEGIN
  
  TRUNCATE TABLE T_LINKS_STG;
  
  COPY INTO T_LINKS_STG(V, file_name)
    FROM (SELECT t.$1 AS V, 'LINKS' AS file_name FROM @T_STG_S3 t)
    --PATTERN = 'links/links.json'
    ON_ERROR = 'skip_file'
    PURGE = FALSE;
   
  TRUNCATE TABLE T_NODES_STG;
   
  COPY INTO T_NODES_STG(V, file_name)
    FROM (SELECT t.$1 AS V, 'NODES' AS file_name FROM @T_STG_S3 t)
    --PATTERN = 'nodes/nodes.json'
    ON_ERROR = 'skip_file'
    PURGE = FALSE;
    
COMMIT;

SELECT * FROM T_LINKS_STG;
SELECT * FROM T_NODES_STG;

CREATE OR REPLACE TABLE T_LINKS AS 
SELECT substr(parse_json($1):source, 0, LEN(parse_json($1):source)) AS sources,
       substr(parse_json($1):target, 0, LEN(parse_json($1):target)) AS target,
       cast(substr(parse_json($1):value, 0, LEN(parse_json($1):value)) AS integer) AS value
FROM T_LINKS_STG;

CREATE OR REPLACE TABLE T_NODES AS 
SELECT substr(parse_json($1):group, 0, LEN(parse_json($1):group)) AS groups,
       substr(parse_json($1):name, 0, LEN(parse_json($1):name)) AS name,
       cast(substr(parse_json($1):nodesize, 0, LEN(parse_json($1):nodesize)) AS integer) AS nodesize
FROM T_NODES_STG;

SELECT * FROM T_LINKS WHERE sources = 'azure';
SELECT * FROM T_NODES;


-- Create new schema
-- move tables to that shema
ALTER TABLE "UDC"."PUBLIC"."T_NODES" RENAME TO "UDC"."WEBAPP"."T_NODES";


SHOW TABLES LIKE '%%' IN udc.public;


CREATE OR REPLACE VIEW POC
AS
SELECT A.BUSINESS_CAPABILITY_NAME, 
	   B.BUSINESS_CAPABILITY_GROUP_NAME,
	   B.BUSINESS_CAPABILITY_GROUP_OWNER,
	   C.CAPABILITY_CENTER_NAME,
	   C.CAPABILITY_CENTER_OWNER,
	   COUNT(*) AS COUNTER
FROM "PUBLIC".BUSINESS_CAPABILITY A
LEFT JOIN "PUBLIC".BUSINESS_CAPABILITY_GROUP B
 ON A.BUSINESS_CAPABILITY_GROUP_ID  = B.BUSINESS_CAPABILITY_GROUP_ID 
LEFT JOIN "PUBLIC".CAPABILITY_CENTER C
 ON B.CAPABILITY_CENTER_ID  = C.CAPABILITY_CENTER_ID
GROUP BY 1,2,3,4,5;


--WORKING TABLE SO WE DO NOT AFFECT TE MODEL

USE UDC;
USE WAREHOUSE UDC_XS;
USE SCHEMA WEBAPP;

CREATE OR REPLACE TABLE TECHNOLOGY_STACK (
    technology_stack_id NUMBER(38,0) IDENTITY NOT NULL PRIMARY KEY,
    technology_stack_name VARCHAR(40) NOT NULL
)

BEGIN TRANSACTION NAME t1;

    INSERT INTO TECHNOLOGY_STACK (technology_stack_name) 
     VALUES ('MySQL'),('Snowflake'),('Redis');
    
COMMIT;

CREATE OR REPLACE TABLE TECHNOLOGY_CAPABILITY (
    technology_capability_id NUMBER(38,0) IDENTITY NOT NULL PRIMARY KEY,
    technology_capability_name VARCHAR(50) NOT NULL
)

BEGIN TRANSACTION NAME t2;

    INSERT INTO TECHNOLOGY_CAPABILITY (technology_capability_name) 
     VALUES ('Backend'),('Infrastructure'),('Data');
    
COMMIT;

CREATE OR REPLACE TABLE TECHNOLOGY_STACK_CAPABILITY (
    technology_stack_id NUMBER(38,0),
    technology_capability_id NUMBER(38,0),
    CONSTRAINT pkey_1 PRIMARY KEY (technology_stack_id, technology_capability_id) NOT ENFORCED,
    CONSTRAINT fkey_1 FOREIGN KEY (technology_stack_id) REFERENCES TECHNOLOGY_STACK (technology_stack_id) NOT ENFORCED,
    CONSTRAINT fkey_2 FOREIGN KEY (technology_capability_id) REFERENCES TECHNOLOGY_CAPABILITY (technology_capability_id) NOT ENFORCED
)

BEGIN TRANSACTION NAME t3;

    INSERT INTO TECHNOLOGY_STACK_CAPABILITY (technology_stack_id, technology_capability_id) 
     VALUES (1,1),(2,2),(3,2),(4,3),(5,3),(6,3);
    
COMMIT;

SELECT s.technology_stack_name,
       c.technology_capability_name,
       COUNT(*) OVER
         (PARTITION BY c.technology_capability_name) AS count_by_capability
FROM TECHNOLOGY_STACK s
LEFT JOIN TECHNOLOGY_STACK_CAPABILITY sc
 ON s.technology_stack_id = sc.technology_stack_id
LEFT JOIN TECHNOLOGY_CAPABILITY c
 ON sc.technology_capability_id = c.technology_capability_id

SELECT * FROM TECHNOLOGY_STACK
SELECT * FROM TECHNOLOGY_CAPABILITY
SELECT * FROM TECHNOLOGY_STACK_CAPABILITY
