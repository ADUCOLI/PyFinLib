# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 08:47:07 2014

@author: Emanuele Mercuri
"""
import numpy as NP
from enum import Enum

FULL_PRECISION = 1e-16

def DoubleEquals(x,y):
    return NP.abs(x-y)<FULL_PRECISION

    
class OptionType(Enum):
    CALL = 1
    PUT = 2
    STRADDLE = 3
    FORWARD = 4
    

class ModelType(Enum):
    NORMAL = 1
    LOGNORMAL = 2
    
    
def IntrinsicValue(forward,strike,optType):
    price = {
        OptionType.CALL: NP.max(forward-strike,0.),
        OptionType.PUT: NP.max(strike-forward,0.),
        OptionType.STRADDLE: NP.max(forward-strike),
        OptionType.FORWARD: forward-strike
    }
    return price.get(optType,NP.max(forward-strike,0.))        
    