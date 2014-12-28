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
import DateLib as DL
import Calendar as CL
import datetime as DT

###############################################################
########  MAP BBG TICKER TO INSTRUMENT CONVENTIONS  ###########
###############################################################

class InstrumentConvention:
    
    def __init__(self,ticker,theCalendar,periodFromOriginToSpot,periodFromSpotToStart,periodFromStartToEnd,adjustmentRule,dayCountBasis):
        self.Calendar = theCalendar
        self.Ticker = ticker
        self.PeriodFromOriginToSpot = periodFromOriginToSpot
        self.PeriodFromSpotToStart = periodFromSpotToStart
        self.PeriodFromStartToEnd = periodFromStartToEnd
        self.AdjustmentRule = adjustmentRule
        self.DayCountBasis = dayCountBasis

    def ticker(self):
        return self.Ticker
    def periodFromOriginToSpot(self):
        return self.PeriodFromOriginToSpot
    def periodFromSpotToStart(self):
        return self.PeriodFromSpotToStart
    def periodFromStartToEnd(self):
        return self.PeriodFromStartToEnd
    def adjustmentRule(self):
        return self.AdjustmentRule
    def dayCountBasis(self):
        return self.DayCountBasis
        
    def computeDatesDayCountFraction(self,refDate):
        # Return a tuble containing ( spotDate , startDate , endDate , dayCountFraction )
        spotDate = self.Calendar.dateAddPeriod(refDate,self.PeriodFromOriginToSpot,self.AdjustmentRule)
        startDate = self.Calendar.dateAddPeriod(spotDate,self.PeriodFromSpotToStart,self.AdjustmentRule)
        endDate = self.Calendar.dateAddPeriod(startDate,self.PeriodFromStartToEnd,self.AdjustmentRule)
        dayCountFraction = DL.DayCountFraction(startDate,endDate,self.DayCountBasis)
        return (spotDate,startDate,endDate,dayCountFraction)

MapTickerToInstrumentConventions = {
    'EUSWE1Z' : InstrumentConvention("EUSWE1Z",CL.EURCalendar(),"2BD","0BD","1W","MF","ACT/360"),
    'EUSWE2Z' : InstrumentConvention("EUSWE2Z",CL.EURCalendar(),"2BD","0BD","2W","MF","ACT/360"),
    'EUSWE3Z' : InstrumentConvention("EUSWE3Z",CL.EURCalendar(),"2BD","0BD","3W","MF","ACT/360"),
    'EUSWEA' : InstrumentConvention("EUSWEA",CL.EURCalendar(),"2BD","0BD","1M","MF","ACT/360"),
    'EUSWEB' : InstrumentConvention("EUSWEB",CL.EURCalendar(),"2BD","0BD","2M","MF","ACT/360"),
    'EUSWEC' : InstrumentConvention("EUSWEC",CL.EURCalendar(),"2BD","0BD","3M","MF","ACT/360"),
    'EUSWED' : InstrumentConvention("EUSWED",CL.EURCalendar(),"2BD","0BD","4M","MF","ACT/360"),
    'EUSWEE' : InstrumentConvention("EUSWEE",CL.EURCalendar(),"2BD","0BD","5M","MF","ACT/360"),
    'EUSWEF' : InstrumentConvention("EUSWEF",CL.EURCalendar(),"2BD","0BD","6M","MF","ACT/360"),
    'EUSWEG' : InstrumentConvention("EUSWEG",CL.EURCalendar(),"2BD","0BD","7M","MF","ACT/360"),
    'EUSWEH' : InstrumentConvention("EUSWEH",CL.EURCalendar(),"2BD","0BD","8M","MF","ACT/360"),
    'EUSWEI' : InstrumentConvention("EUSWEI",CL.EURCalendar(),"2BD","0BD","9M","MF","ACT/360"),
    'EUSWEJ' : InstrumentConvention("EUSWEJ",CL.EURCalendar(),"2BD","0BD","10M","MF","ACT/360"),
    'EUSWEK' : InstrumentConvention("EUSWEK",CL.EURCalendar(),"2BD","0BD","11M","MF","ACT/360"),
    'EUSWE1' : InstrumentConvention("EUSWE1",CL.EURCalendar(),"2BD","0BD","1Y","MF","ACT/360"),
    'EUSWE1C' : InstrumentConvention("EUSWE1C",CL.EURCalendar(),"2BD","0BD","15M","MF","ACT/360"),
    'EUSWE1F' : InstrumentConvention("EUSWE1F",CL.EURCalendar(),"2BD","0BD","18M","MF","ACT/360"),
    'EUSWE1I' : InstrumentConvention("EUSWE1I",CL.EURCalendar(),"2BD","0BD","21M","MF","ACT/360"),
    'EUSWE2' : InstrumentConvention("EUSWE2",CL.EURCalendar(),"2BD","0BD","2Y","MF","ACT/360"),
    'EUSWE3' : InstrumentConvention("EUSWE3",CL.EURCalendar(),"2BD","0BD","3Y","MF","ACT/360"),
    'EUSWE4' : InstrumentConvention("EUSWE4",CL.EURCalendar(),"2BD","0BD","4Y","MF","ACT/360"),
    'EUSWE5' : InstrumentConvention("EUSWE5",CL.EURCalendar(),"2BD","0BD","5Y","MF","ACT/360"),
    'EUSWE6' : InstrumentConvention("EUSWE6",CL.EURCalendar(),"2BD","0BD","6Y","MF","ACT/360"),
    'EUSWE7' : InstrumentConvention("EUSWE7",CL.EURCalendar(),"2BD","0BD","7Y","MF","ACT/360"),
    'EUSWE8' : InstrumentConvention("EUSWE8",CL.EURCalendar(),"2BD","0BD","8Y","MF","ACT/360"),
    'EUSWE9' : InstrumentConvention("EUSWE9",CL.EURCalendar(),"2BD","0BD","9Y","MF","ACT/360"),
    'EUSWE10' : InstrumentConvention("EUSWE10",CL.EURCalendar(),"2BD","0BD","10Y","MF","ACT/360"),
    'EUSWE11' : InstrumentConvention("EUSWE11",CL.EURCalendar(),"2BD","0BD","11Y","MF","ACT/360"),
    'EUSWE12' : InstrumentConvention("EUSWE12",CL.EURCalendar(),"2BD","0BD","12Y","MF","ACT/360"),
    'EUSWE13' : InstrumentConvention("EUSWE13",CL.EURCalendar(),"2BD","0BD","13Y","MF","ACT/360"),
    'EUSWE14' : InstrumentConvention("EUSWE14",CL.EURCalendar(),"2BD","0BD","14Y","MF","ACT/360"),
    'EUSWE15' : InstrumentConvention("EUSWE15",CL.EURCalendar(),"2BD","0BD","15Y","MF","ACT/360"),
    'EUSWE16' : InstrumentConvention("EUSWE16",CL.EURCalendar(),"2BD","0BD","16Y","MF","ACT/360"),
    'EUSWE17' : InstrumentConvention("EUSWE17",CL.EURCalendar(),"2BD","0BD","17Y","MF","ACT/360"),
    'EUSWE18' : InstrumentConvention("EUSWE18",CL.EURCalendar(),"2BD","0BD","18Y","MF","ACT/360"),
    'EUSWE19' : InstrumentConvention("EUSWE19",CL.EURCalendar(),"2BD","0BD","19Y","MF","ACT/360"),
    'EUSWE20' : InstrumentConvention("EUSWE20",CL.EURCalendar(),"2BD","0BD","20Y","MF","ACT/360"),
    'EUSWE21' : InstrumentConvention("EUSWE21",CL.EURCalendar(),"2BD","0BD","21Y","MF","ACT/360"),
    'EUSWE22' : InstrumentConvention("EUSWE22",CL.EURCalendar(),"2BD","0BD","22Y","MF","ACT/360"),
    'EUSWE23' : InstrumentConvention("EUSWE23",CL.EURCalendar(),"2BD","0BD","23Y","MF","ACT/360"),
    'EUSWE24' : InstrumentConvention("EUSWE24",CL.EURCalendar(),"2BD","0BD","24Y","MF","ACT/360"),
    'EUSWE25' : InstrumentConvention("EUSWE25",CL.EURCalendar(),"2BD","0BD","25Y","MF","ACT/360"),
    'EUSWE26' : InstrumentConvention("EUSWE26",CL.EURCalendar(),"2BD","0BD","26Y","MF","ACT/360"),
    'EUSWE27' : InstrumentConvention("EUSWE27",CL.EURCalendar(),"2BD","0BD","27Y","MF","ACT/360"),
    'EUSWE28' : InstrumentConvention("EUSWE28",CL.EURCalendar(),"2BD","0BD","28Y","MF","ACT/360"),
    'EUSWE29' : InstrumentConvention("EUSWE29",CL.EURCalendar(),"2BD","0BD","29Y","MF","ACT/360"),
    'EUSWE30' : InstrumentConvention("EUSWE30",CL.EURCalendar(),"2BD","0BD","30Y","MF","ACT/360"),
    'EUSWE50' : InstrumentConvention("EUSWE50",CL.EURCalendar(),"2BD","0BD","50Y","MF","ACT/360"),
    'EUR003M' : InstrumentConvention("EUR003M",CL.EURCalendar(),"2BD","0BD","3M","MF","ACT/360"),
    'EUFR0AD' : InstrumentConvention("EUFR0AD",CL.EURCalendar(),"2BD","1M","4M","MF","ACT/360"),
    'EUFR0BE' : InstrumentConvention("EUFR0BE",CL.EURCalendar(),"2BD","2M","5M","MF","ACT/360"),
    'EUFR0CF' : InstrumentConvention("EUFR0CF",CL.EURCalendar(),"2BD","3M","6M","MF","ACT/360"),
    'EUFR0DG' : InstrumentConvention("EUFR0DG",CL.EURCalendar(),"2BD","4M","7M","MF","ACT/360"),
    'EUFR0EH' : InstrumentConvention("EUFR0EH",CL.EURCalendar(),"2BD","5M","8M","MF","ACT/360"),
    'EUFR0FI' : InstrumentConvention("EUFR0FI",CL.EURCalendar(),"2BD","6M","9M","MF","ACT/360"),
    'EUFR0GJ' : InstrumentConvention("EUFR0GJ",CL.EURCalendar(),"2BD","7M","10M","MF","ACT/360"),
    'EUFR0HK' : InstrumentConvention("EUFR0HK",CL.EURCalendar(),"2BD","8M","11M","MF","ACT/360"),
    'EUFR0I1' : InstrumentConvention("EUFR0I1",CL.EURCalendar(),"2BD","9M","12M","MF","ACT/360")
}


###############################################################
########  Intrument Set  ######################################
###############################################################

class BootstrapIntrumentSet:
    
    def __init__(self,fileName):
        currentDir = os.getcwd()
        sys.path.append(currentDir)
        xl_Name = currentDir + fileName
        
        self.Data = {}
        self.Data['Ref_Date'] = DT.datetime(*xlrd.xldate_as_tuple(EL.xl_Get_Data(xl_Name, 0, 0, 3, 0, 3)[0], 0))
        self.Data['Tickers'] = EL.xl_Get_Data_ToUpperCaseString(xl_Name, 0, 5, 2, 48, 2)
        self.Data['MarketQuotes'] = EL.xl_Get_Data(xl_Name, 0, 5, 3, 48, 3)
        
        self.Data['InstrumentsConventions'] = []
        for idx in range(0, len(self.Data['Tickers'])):
            instConvention = MapTickerToInstrumentConventions.get(self.Data['Tickers'][idx])
            if(instConvention is None):
                raise ValueError('Null instrument convention from input data')
            self.Data['InstrumentsConventions'].append(instConvention)
            
    def refDate(self):
        return self.Data['Ref_Date']
    def tickers(self):
        return self.Data['Tickers']
    def instrumentsConventions(self):
        return self.Data['InstrumentsConventions']
    def instrumentConvention(self,ticker):
        instConventions = self.Data['InstrumentsConventions']
        for idx in range(0, len(instConventions)):
            instConvention = instConventions[idx]
            if(ticker == instConvention.ticker()):
                return instConvention
        raise ValueError('Ticker not found in InstrumentsConventions list')
        
    def marketQuotes(self):
        return self.Data['MarketQuotes']
    def numInstruments(self):
        return len(self.Data['InstrumentsConventions'])


class Curve:
    __metaclass__ = ABCMeta

    def __init__(self,insSet):
        self.InsSet = insSet
        self.DayCountFractions = []
        self.Maturities = []

    def refDate(self):
        return self.InsSet.refDate()
    def instrumentsConventions(self):
        return self.InsSet.instrumentsConventions()
    def marketQuotes(self):
        return self.InsSet.marketQuotes()
    def numPillars(self):
        return self.InsSet.numInstruments()
    def maturities(self):
        return self.Maturities
    def dayCountFractions(self):
        return self.DayCountFractions

    @abstractmethod        
    def bootstrap(self): pass
            

class DiscountCurve(Curve):

    def __init__(self,insSet):
        super(DiscountCurve, self).__init__(insSet)
        self.name = 'EONIA'
        self.DiscountFactors = []
        self.ZeroRates = []

    def name(self):
        return self.name
    def discountFactors(self):
        return self.DiscountFactors
    def zeroRates(self):
        return self.ZeroRates
    def numPillars(self):
        return 33        
    def dictDataToStore(self):
        data = {}        
        data[self.name] = {
            'RefDate' : self.refDate(),
            'Discount' : self.DiscountFactors,
            'Zero Rate' : self.ZeroRates,
            'Maturities' : self.maturities()
            }
        dataToStore = {self.refDate():data}
        return dataToStore

    def bootstrap(self):
        cumSum = 0.
        ref_date = self.refDate()
        settlement_date = ref_date
        for i in range(0,self.numPillars()):
            instConvention = self.instrumentsConventions()[i]
            (spotDate,startDate,maturity,dayCountFraction) = instConvention.computeDatesDayCountFraction(ref_date)
            dcfFromRefDate = DL.DayCountFraction(ref_date,maturity,instConvention.dayCountBasis)

            self.Maturities.append(maturity)
            self.DayCountFractions.append(dcfFromRefDate)
            
            dcf_i = DL.DayCountFraction(settlement_date,maturity,instConvention.dayCountBasis)
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
        dcf = DL.DayCountFraction(self.refDate(),fixingDate,self.basis)
        zero_rate = self.Interpolator(dcf)
        return math.exp(-zero_rate*dcf)