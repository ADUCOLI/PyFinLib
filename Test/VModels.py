# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 08:38:53 2014

@author: Emanuele Mercuri
"""
from abc import ABCMeta, abstractmethod

class I_VModel:
    __metaclass__ = ABCMeta

    @abstractmethod        
    def exerciseTime(self): pass

    @abstractmethod        
    def forward(self): pass

    @abstractmethod        
    def optionFwdPrice(self,strike,optType): pass

    @abstractmethod
    def pdf(self,strike): pass

    @abstractmethod
    def equivalentLognormalVol(self,strike): pass

    @abstractmethod
    def equivalentNormalVol(self,strike): pass


class BlackModel(I_VModel):
    
    def __init__(self,forward,exerciseTime,volatility,modelType):
        self.Forward = forward
        self.ExerciseTime = exerciseTime
        self.Volatility = volatility
        self.ModelType = modelType

    def exerciseTime(self):
        return self.ExerciseTime
            
    def forward(self):
        return self.Forward
