-- -*- coding: utf-8 -*-
-- Created by Luis Enrique Fuentes Plata

-- creating new schema
create schema webapp;

-- Creating tables
create table webapp.TECHNOLOGY_CAPABILITY (
	technology_capability_id serial not null primary key, 
	technology_capability_name varchar(50) not null
);
    
create table webapp.TECHNOLOGY_STACK
( 
  technology_stack_id serial not null primary key,
  technology_stack_name varchar(40) not null,
  technology_capability_id integer not null, 
  constraint fk_technology_cap_id foreign key (technology_capability_id) REFERENCES webapp.TECHNOLOGY_CAPABILITY (technology_capability_id)
);

-- Inserting data
BEGIN;

    INSERT INTO webapp.TECHNOLOGY_CAPABILITY (technology_capability_name) 
     VALUES ('Backend'),('Infrastructure'),('Data');
    
COMMIT;

BEGIN;

    INSERT INTO webapp.TECHNOLOGY_STACK (technology_stack_name, technology_capability_id) 
     VALUES ('Docker',2),('AWS',2),('Nginx',2);
    
COMMIT;

-- Creating view webapp.v_stack_cap
create view webapp.v_stack_cap as
  select ts.technology_stack_id, 
      ts.technology_stack_name,
      tc.technology_capability_name 
  from webapp.technology_stack ts 
  inner join webapp.technology_capability tc 
  on ts.technology_capability_id  = tc.technology_capability_id;

COMMIT;
