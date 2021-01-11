# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Enrique Fuentes Plata

import psycopg2
from application_logic.GenericFunctions import get_db_credentials

class TechnologyCapabilityModel:
    def __init__(self, technology_capability_id:int, technology_capability_name:str):
        self.technology_capability_id = technology_capability_id
        self.technology_capability_name = technology_capability_name
    
    def transform(self)->tuple:
        """Transforms object TechnologyCapabilityModel to a tuple in which every value is part of the self values

        Returns:
            tuple: (self.technology_capability_id, self.technology_capability_name)
        """
        return (self.technology_capability_id, self.technology_capability_name)

class TechnologyStackModel:
    def __init__(self, technology_stack_id:int, technology_stack_name:str, technology_capability_id:int):
        self.technology_stack_id =  technology_stack_id
        self.technology_stack_name =  technology_stack_name
        self.technology_capability_id =  technology_capability_id
    
    def transform(self)->tuple:
        """Transforms object TechnologyStackModel to a tuple in which every value is part of the self values

        Returns:
            tuple: (self.technology_stack_id, self.technology_stack_name, self.technology_capability_id)
        """
        return (self.technology_stack_id, self.technology_stack_name, self.technology_capability_id)

class VStackCapabilityModel:
    def __init__(self, technology_stack_id:int, technology_stack_name:str, technology_capability_name:str):
        self.technology_stack_id = technology_stack_id
        self.technology_stack_name = technology_stack_name
        self.technology_capability_name = technology_capability_name
    
    def transform(self)->tuple:
        """Transforms object VStackCapabilityModel to a tuple in which every value is part of the self values

        Returns:
            tuple: (self.technology_stack_id, self.technology_stack_name, self.technology_capability_name)
        """
        return (self.technology_stack_id, self.technology_stack_name, self.technology_capability_name)

class DataLoader:
    def __init__(self):
        self.__registry = get_db_credentials()
        self.__connection = psycopg2.connect(user=self.__registry['POSTGRES_USER'],
                                        password=self.__registry['POSTGRES_PASSWORD'],
                                        host="db",
                                        port="5432",
                                        database=self.__registry['POSTGRES_DB'])
        
    def __load_data_from_database(self, query:str)->list:
        """This is a private method therefore should not be called direcly. This method connects to the database and pull info
        based on a query.

        Args:
            query (str): String of a query that will be execute by the database engine.

        Returns:
            list: List of tuples containing the results of a query
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            return result
            #conn.close()
    
    def __insert_data_to_database(self, query:str, params:tuple)->None:
        """This is a private method therefore should not be called directly. This method connects to the database and inserts
        data that is past on a query and a tuple of parameters. This methods is run by binding parameters

        Args:
            query (str): Query to be executed
            params (tuple): Tuple containing values
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, params)
            self.__connection.commit()
            # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            #conn.close()
        
    def get_technology_capability(self)->list:
        """Pulls data from webapp.technology_capability and transforms its values to tuples, the following query is run:
            select * from webapp.technology_capability;

        Returns:
            list: List of tuples containing the result of the query 
        """
        return [TechnologyCapabilityModel(*row).transform() for row in self.__load_data_from_database("select * from webapp.technology_capability;")]
    
    def get_technology_stack(self)->list:
        """Pulls data from webapp.technology_stack and transforms its values to tuples, the following query is run:
            select * from webapp.technology_stack;

        Returns:
            list: List of tuples containing the result of the query 
        """
        return [TechnologyStackModel(*row).transform() for row in self.__load_data_from_database("select * from webapp.technology_stack;")]
    
    def get_v_stack_cap(self)->list:
        """Pulls data from webapp.v_stack_cap and transforms its values to tuples, the following query is run:
            select * from webapp.v_stack_cap;

        Returns:
            list: List of tuples containing the result of the query 
        """
        return [VStackCapabilityModel(*row).transform() for row in self.__load_data_from_database("select * from webapp.v_stack_cap;")]

    def insert_data_into_stack(self, query:str, values:tuple)->None:
        """Inserts data into webapp.technology_stack

        Args:
            query (str): INSERT INTO webapp.technology_stack (technology_stack_name, technology_capability_id) VALUES (%s, %s)
            values (tuple): (val_1, val_2)
        """
        self.__insert_data_to_database(query, values)
