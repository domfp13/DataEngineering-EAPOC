# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

from Snowflake import DataLoader
from GenericFunctions import getCredentials

if __name__ == "__main__":
    
    data_loader = DataLoader(getCredentials())
    for element in data_loader.get_technology_stack():
        print(element)
