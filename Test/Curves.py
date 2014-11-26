# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 12:04:30 2014

@author: Ducoli & Mercuri
"""

import xlrd
import sys
import os
import math
import numpy
from abc import ABCMeta, abstractmethod
from scipy import interpolate

import ExcelLib as EL
import DayCountFraction as DCF
import datetime as DT

class BootstrapIntrumentSet:
    
    def __init__(self,fileName,calendar):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(currentDir)
        xl_Name = currentDir + fileName
        
        self.Data = {}
        self.Data['Ref_Date'] = DT.datetime(*xlrd.xldate_as_tuple(EL.xl_Get_Data(xl_Name, 0, 0, 3, 0, 3)[0], 0))
        self.Data['Spot_Date'] = DT.datetime(*xlrd.xldate_as_tuple(EL.xl_Get_Data(xl_Name, 0, 1, 3, 1, 3)[0], 0))    
        self.Data['Periods'] = EL.xl_Get_Data_ToUpperCaseString(xl_Name, 0, 5, 2, 53, 2)
        self.Data['MarketQuotes'] = EL.xl_Get_Data(xl_Name, 0, 5, 3, 53, 3)
        
        self.calendar = calendar
        self.Data['Maturities'] = []
        for idx in range(0, len(self.Data['Periods'])):
            self.Data['Maturities'].append(self.calendar.dateAddPeriod(self.Data['Ref_Date'],self.Data['Periods'][idx]))
            
    def refDate(self):
        return self.Data['Ref_Date']
    def spotDate(self):
        return self.Data['Spot_Date']
    def periods(self):
        return self.Data['Periods']
    def maturities(self):
        return self.Data['Maturities']        
    def marketQuotes(self):
        return self.Data['MarketQuotes']
    def numInstruments(self):
        return len(self.Data['Periods'])


class Curve:
    __metaclass__ = ABCMeta

    def __init__(self,insSet):
        self.InsSet = insSet
        self.DayCountFractions = []

    def refDate(self):
        return self.InsSet.refDate()
    def spotDate(self):
        return self.InsSet.spotDate()
    def periods(self):
        return self.InsSet.periods()
    def marketQuotes(self):
        return self.InsSet.marketQuotes()
    def numPillars(self):
        return self.InsSet.numInstruments()
    def maturities(self):
        return self.InsSet.maturities()
    def dayCountFractions(self):
        return self.DayCountFractions

    @abstractmethod        
    def bootstrap(self): pass
            

class DiscountCurve(Curve):

    def __init__(self,insSet):
        super(DiscountCurve, self).__init__(insSet)
        self.name = 'EONIA'
        self.basis = 'ACT/360'
        self.DiscountFactors = []
        self.ZeroRates = []

    def name(self):
        return self.name
    def discountFactors(self):
        return self.DiscountFactors
    def zeroRates(self):
        return self.ZeroRates

    def bootstrap(self):
        cumSum = 0.
        ref_date = self.refDate()
        settlement_date = ref_date
        for i in range(0,self.numPillars()):
            maturity = self.maturities()[i]
            dcfFromRefDate = DCF.DayCountFraction(ref_date,maturity,self.basis)
            self.DayCountFractions.append(dcfFromRefDate)
            dcf_i = DCF.DayCountFraction(settlement_date,maturity,self.basis)            
            mktQuote_i = self.InsSet.marketQuotes()[i]
            if dcfFromRefDate <=1.0:
                df = 1./(1+dcfFromRefDate*mktQuote_i)
            else:
                df = (1.-mktQuote_i*cumSum)/(1+dcf_i*mktQuote_i)
        
            zeroRate = -math.log(df)/dcfFromRefDate
            cumSum = cumSum + dcf_i* df
            settlement_date = maturity
            
            self.DiscountFactors.append(df)
            self.ZeroRates.append(zeroRate)
        self.Interpolator = interpolate.Akima1DInterpolator(numpy.array(self.DayCountFractions),numpy.array(self.ZeroRates))
    
    def getDiscountFactor(self,fixingDate):
        dcf = DCF.DayCountFraction(self.refDate(),fixingDate,self.basis)
        zero_rate = self.Interpolator(dcf)
        return math.exp(-zero_rate*dcf)