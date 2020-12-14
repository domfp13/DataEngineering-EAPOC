# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

from application_logic.Snowflake import SnowflakeClient
from application_logic.Credentials import getCredentials
from dataclasses import dataclass
from datetime import date

@dataclass
class Employee:
    """Represents an Employee instance of the application."""
    name: str
    last_name: str
    title: str
    inserted_date: date
    
    def __init__(self, name: str, last_name: str, title: str, inserted_date: date):
        """Initializes the Object.

        Args:
            name (str): containing the name of the employee
            last_name (str): containing the last name of the employee
            title (str): containing the title of the employee
        """
        super(Employee, self).__init__()

        self.name = name
        self.last_name = last_name
        self.title = title
        self.inserted_date = inserted_date

class DataLoader:
    """The DataLoader is responsible to load all entities from the database. """
    
    def __init__(self):
        """Initializes the DataLoader.
        """
        super(DataLoader, self).__init__()
        self.client = SnowflakeClient.getConnection(getCredentials())
    
    def __load_data_from_database(self, query:str)->list:
        """Load the requested data from the database.

        This method is private and should therefore not be called directly.

        Args:
            query (str): Query to be executed.
        
        Retuns:
            list: List containing Tuples, each representing one row of a query result.
        """
        result = self.client.execute(query).fetchall()
        return result
    
    def get_employee(self):
        """Loads all Employees from the database.

        Returns:
            list: Returns a list of Employee instances, each containing the data of one Tuple
            of the Employee table.
        """
        return [Employee(*row) for row in self.__load_data_from_database("SELECT * FROM EMPLOYEE")]