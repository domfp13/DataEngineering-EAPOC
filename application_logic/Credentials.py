# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

def decoratorGetCredentials(function):
    def wrapper():
        from os import environ
        return environ.get('USERNAME')
    return wrapper
#@decoratorGetUserName
def getCredentials()->dict:
    """This is a decorator function, it is use in dev to pass the hardcoded credentials in order to connect to Snowflake
    
    Arguments:
        None
    Returns: 
        (str)
    """
    return {
            'user':'', 
            'password':'', 
            'account':'', 
            'database_name':'', 
            'schema_name':'', 
            'warehouse_name':'', 
            'role_name':''
            }
