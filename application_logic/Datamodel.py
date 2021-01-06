# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

# Copyright (c) CompuCom, All Rights Reserved

from sqlalchemy import create_engine

class TechnologyStackModel:

    def __init__(self, technology_stack_id:int, technology_stack_name:str, technology_capability_id:int):
        self.technology_stack_id =  technology_stack_id
        self.technology_stack_name =  technology_stack_name
        self.technology_capability_id =  technology_capability_id
    
    def transform(self):
        return (self.technology_stack_id, self.technology_stack_name, self.technology_capability_id)

    def __repr__(self):
        return f'{self.technology_stack_id}, {self.technology_stack_name}, {self.technology_capability_id}'

class TechnologyCapability:
    def __init__(self, technology_capability_id:int, technology_capability_name:str):
        self.technology_capability_id = technology_capability_id
        self.technology_capability_name = technology_capability_name
    
    def transform(self):
        return (self.technology_capability_id, self.technology_capability_name)

class DataLoader:

    def __init__(self, registry:dict):
        self.__registry = registry
        self.__engine = create_engine(
                'snowflake://{user}:{password}@{account}/{database_name}/{schema_name}?warehouse={warehouse_name}&role={role_name}'.format(
                    user=self.__registry['user'],
                    password=self.__registry['password'],
                    account=self.__registry['account'],
                    database_name=self.__registry['database_name'],
                    schema_name=self.__registry['schema_name'],
                    warehouse_name=self.__registry['warehouse_name'],
                    role_name=self.__registry['role_name']
                )
            )
    
    def __load_data_from_database(self, query):
        try:
            connection = self.__engine.connect()
            return connection.execute(query).fetchall()
        except Exception as e:
            print(e)
        finally:
            connection.close()
            #self.__engine.dispose()
    
    def __put_data_to_database(self, query):
        try:
            connection = self.__engine.connect()
            connection.execute(query)
            connection.execute("COMMIT")
        except Exception as e:
            print(e)
        finally:
            connection.close()
    
    def get_technology_stack(self):
        return [TechnologyStackModel(*row).transform() for row in self.__load_data_from_database('SELECT * FROM TECHNOLOGY_STACK')]

    def put_technology_stack(self, **kargs)->None:
        query = "CALL SPW_INSERT_TECHNOLOGY_STACK('{technology_stack_name}', {technology_capability_id})".format(technology_stack_name=kargs.get('tsn'), technology_capability_id=kargs.get('tci'))
        self.__put_data_to_database(query)

    def get_technology_capability(self):
        return [TechnologyCapability(*row).transform() for row in self.__load_data_from_database('SELECT * FROM TECHNOLOGY_CAPABILITY')]