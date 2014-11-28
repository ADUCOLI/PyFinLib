# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 08:47:07 2014

@author: Emanuele Mercuri
"""
from enum import Enum


class OptionType(Enum):
    CALL = 1
    PUT = 2
    STRADDLE = 3
    

class ModelType(Enum):
    NORMAL = 1
    LOGNORMAL = 2