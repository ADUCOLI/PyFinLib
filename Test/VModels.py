# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 08:38:53 2014

@author: Emanuele Mercuri
"""
from abc import ABCMeta, abstractmethod
import VModelUtilities as VMU
import Definitions as DEF
import numpy as NP

class I_VModel:
    __metaclass__ = ABCMeta

    @abstractmethod        
    def exerciseTime(self): pass

    @abstractmethod        
    def forward(self): pass

    @abstractmethod        
    def optionFwdPrice(self,strike,optType): pass

    def pdf(self,strike):
        bump = 1.0e-5
        fwd = self.forward()
        if strike>fwd:
            optType = DEF.OptionType.CALL
        else:
            optType = DEF.OptionType.PUT
        up = self.optionFwdPrice(strike+bump, optType)
        mid = self.optionFwdPrice(strike, optType)
        down = self.optionFwdPrice(strike-bump, optType)
        return (up + down - 2.0 * mid) / (bump*bump);
        

    def digitalOptFwdPrice(self,strike,optType):
        fwd = self.forward()
        if optType == DEF.OptionType.FORWARD:
            return fwd
        bump = 1.0e-5
        if strike>fwd:
            optType = DEF.OptionType.CALL
            U = 1.0
        else:
            optType = DEF.OptionType.PUT
            U = 0.0
        up = self.optionFwdPrice(strike+bump, optType)
        down = self.optionFwdPrice(strike-bump, optType)
        U += 0.5 * (up - down) / bump;

        price = {
            DEF.OptionType.CALL: NP.max(NP.min(1.0 - U, 1.0), 0.0),
            DEF.OptionType.PUT: NP.max(NP.min(U, 1.0), 0.0),
            DEF.OptionType.STRADDLE: NP.max(NP.min(1.0 - 2.0 * U, 1.0), -1.0)
        }
        return price[optType]


    def equivalentLognormalVol(self,strike):
        fwd = self.forward()
        if strike>fwd:
            optType = DEF.OptionType.CALL
        else:
            optType = DEF.OptionType.PUT
        otmOptionValue = self.optionFwdPrice(strike, optType)
        return VMU.BlackImpliedVol(otmOptionValue,fwd,strike,optType,DEF.ModelType.LOGNORMAL)        


    def equivalentNormalVol(self,strike):
        fwd = self.forward()
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
        return price[self.ModelType]