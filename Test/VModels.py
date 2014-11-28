# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 08:38:53 2014

@author: Emanuele Mercuri
"""
from abc import ABCMeta, abstractmethod
import VModelUtilities as VMU
import Definitions as DEF

class I_VModel:
    __metaclass__ = ABCMeta

    @abstractmethod        
    def exerciseTime(self): pass

    @abstractmethod        
    def forward(self): pass

    @abstractmethod        
    def optionFwdPrice(self,strike,optType): pass

#    @abstractmethod
#    def pdf(self,strike): pass

    def equivalentLognormalVol(self,strike):
        fwd = self.forward();
        if strike>fwd:
            optType = DEF.OptionType.CALL
        else:
            optType = DEF.OptionType.PUT
	otmOptionValue = self.optionFwdPrice(strike, optType);
	return VMU.BlackImpliedVol(otmOptionValue,fwd,strike,optType,DEF.ModelType.LOGNORMAL)        


    def equivalentNormalVol(self,strike):
        fwd = self.forward();
        if strike>fwd:
            optType = DEF.OptionType.CALL
        else:
            optType = DEF.OptionType.PUT
	otmOptionValue = self.optionFwdPrice(strike, optType);            
	return VMU.BlackImpliedVol(otmOptionValue,fwd,strike,optType,DEF.ModelType.NORMAL)


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

    def optionFwdPrice(self,strike,optType):
        price = {
            DEF.ModelType.NORMAL: VMU.NormalBlackFormula(self.Forward,self.ExerciseTime,self.Volatility,strike,optType),
            DEF.ModelType.LOGNORMAL: VMU.LogNormalBlackFormula(self.Forward,self.ExerciseTime,self.Volatility,strike,optType)
        }
        return price.get(self.ModelType,VMU.LogNormalBlackFormula(self.Forward,self.ExerciseTime,self.Volatility,strike,optType))