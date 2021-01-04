# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

#from Datamodel import DataLoader
#from GenericFunctions import getCredentials
def my_testing(*args):
    """
    docstring
    """
    print(*args[0][0])

if __name__ == "__main__":

    my_testing(['One','Two'])
    
    # data_loader = DataLoader(getCredentials())
    # for element in data_loader.get_technology_capability():
    #     print(element)
