# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 12:04:30 2014

@author: Ducoli & Mercuri
"""

import xlrd
import sys
import os

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


class Bootstrap:

    def __init__(self,insSet):
        self.InsSet = insSet        
        self.DiscountCurve = {}
        self.DiscountCurve['Maturities'] = []
        self.DiscountCurve['Rates'] = []

    def maturities(self):
        return self.DiscountCurve['Maturities']
    def discountFactors(self):
        return self.DiscountCurve['Rates']
        
    def bootDiscountCurve(self):
        basis = 'ACT/360'
        cumSum = 0.
        ref_date = self.InsSet.refDate()
        settlement_date = self.InsSet.refDate()
        for i in range(0,self.InsSet.numInstruments()):
            maturity = self.InsSet.maturities()[i]
            self.DiscountCurve['Maturities'].append(maturity)
            dcf_fromRef = DCF.DayCountFraction(ref_date,maturity,basis)
            dcf_i = DCF.DayCountFraction(settlement_date,maturity,basis)            
            mktQuote_i = self.InsSet.marketQuotes()[i]
            if dcf_fromRef <=1.0:
                self.DiscountCurve['Rates'].append( 1./(1+dcf_fromRef*mktQuote_i))
            else:
                self.DiscountCurve['Rates'].append((1.-mktQuote_i*cumSum)/(1+dcf_i*mktQuote_i))
        
            cumSum = cumSum + dcf_i* self.DiscountCurve['Rates'][i]
            settlement_date = maturity