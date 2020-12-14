# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

from sqlalchemy import create_engine

class SnowflakeClient:
    
    # Class attribute
    connection = None

    @staticmethod
    def getConnection(registry:dict):
        """Singleton Pattern to create one connection per container

        Args:
            registry (dict): Dictionary with credentials
        
        Returns:
            SnowflakeClient: This method returs an instance connection of a Snowflake connection.
        """
        if SnowflakeClient.connection == None:
            SnowflakeClient(registry)
        
        return SnowflakeClient.connection
    
    def __init__(self, registry:dict):
        if SnowflakeClient.connection != None:
            raise Exception("This a singleton object")
        else:
            self.__engine = create_engine(
                'snowflake://{user}:{password}@{account}/{database_name}/{schema_name}?warehouse={warehouse_name}&role={role_name}'.format(
                    user=registry['user'],
                    password=registry['password'],
                    account=registry['account'],
                    database_name=registry['database_name'],
                    schema_name=registry['schema_name'],
                    warehouse_name=registry['warehouse_name'],
                    role_name=registry['role_name']
                )
            )
            SnowflakeClient.connection = self.__engine.connect()
    
    def __del__(self):
        SnowflakeClient.connection.close()
        self.__engine.dispose()
        print("Connection Deleted!")