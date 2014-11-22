# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 12:04:30 2014

@author: Ducoli & Mercuri
"""

import xlrd
import sys
import os
from abc import ABCMeta, abstractmethod

import ExcelLib as EL
import DayCountFraction as DCF
import Calendar as CAL
import datetime as DT

class BootstrapIntrumentSet:
    
    def __init__(self,fileName,calendar=CAL.Calendar()):
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
        self.DiscountCurve = []

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
    def discountFactors(self):
        return self.DiscountCurve

    @abstractmethod        
    def bootstrap(self): pass
            
class EoniaCurve(Curve):

    def __init__(self,insSet):
        super(EoniaCurve, self).__init__(insSet)
        self.name = 'EONIA'
        self.basis = 'ACT/360'

    def bootstrap(self):
        cumSum = 0.
        ref_date = self.refDate()
        settlement_date = ref_date
        for i in range(0,self.numPillars()):
            maturity = self.maturities()[i]
            dcf_fromRef = DCF.DayCountFraction(ref_date,maturity,self.basis)
            dcf_i = DCF.DayCountFraction(settlement_date,maturity,self.basis)            
            mktQuote_i = self.InsSet.marketQuotes()[i]
            if dcf_fromRef <=1.0:
                self.DiscountCurve.append( 1./(1+dcf_fromRef*mktQuote_i))
            else:
                self.DiscountCurve.append((1.-mktQuote_i*cumSum)/(1+dcf_i*mktQuote_i))
        
            cumSum = cumSum + dcf_i* self.DiscountCurve[i]
            settlement_date = maturity