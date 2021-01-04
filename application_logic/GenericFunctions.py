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

def decorator_get_secrect_key(function):
    def wrapper():
        from os import environ
        return environ.get('SECRET_KEY')
    return wrapper
#@decorator_get_secrect_key
def get_secret_key()->str:
    """This function grabs the secret key for the application configuration using a decorator, 
       for local testing deactivate the decorator since it is using an environmental value passed to the container at creation time.

    Returns:
        str: [This will be a secret key in form of string]
    """
    return 'dynamoDB@'