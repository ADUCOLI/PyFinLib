# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 17:18:23 2014

@author: Emanuele Mercuri
"""
from abc import ABCMeta, abstractmethod
import datetime as DT
import workdays as WD
import calendar as CL

class Calendar:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.Holidays = []

    @abstractmethod        
    def holidays(self): pass
    
    @staticmethod
    def periodParser(period):
        idx = 0
        for i in range(0,len(period)):
            if period[i].isalpha():
                idx = i
                break;
        out = {}
        out['unit'] = int(period[:idx])
        out['period'] = period[idx:].upper()
        return out
        
    def dateAddNumberOfDays(self,startDate,numberOfBD):
        endDate = WD.workday(startDate,numberOfBD,self.Holidays)
        return endDate

    def dateAddNumberOfMonths(self,startDate,numberOfMonths):
        month = startDate.month - 1 + numberOfMonths
        year = startDate.year + month / 12
        month = month % 12 + 1
        day = min(startDate.day,CL.monthrange(year,month)[1])
        endDate = DT.datetime(year,month,day)
        return self.dateAdjust(endDate)
        
    def dateAdjust(self,startDate):
        endDate = startDate
        if (endDate in self.Holidays) or (endDate.weekday() in set([5, 6])):
            endDate = self.dateAddNumberOfDays(startDate,1)
        return endDate        
            
    def dateAddPeriod(self,startDate,period):
        parserResult = Calendar.periodParser(period)
        endDate = {
         'BD': self.dateAddNumberOfDays(startDate,parserResult['unit']),
         'W': self.dateAddNumberOfDays(startDate,parserResult['unit']*5),
         'M': self.dateAddNumberOfMonths(startDate,parserResult['unit']),
         'Y': self.dateAddNumberOfMonths(startDate,parserResult['unit']*12),
        }.get(parserResult['period'], self.dateAddNumberOfDays(startDate,1))        
        return endDate
        
        
class EURCalendar(Calendar):
    
    def __init__(self):
        self.Holidays = [
            DT.datetime(2014,12,25)
            ,DT.datetime(2014,12,26)
            ,DT.datetime(2015,1,1)
            ,DT.datetime(2015,4,3)
            ,DT.datetime(2015,4,6)
            ,DT.datetime(2015,12,25)
            ,DT.datetime(2016,1,1)
            ,DT.datetime(2016,3,25)
            ,DT.datetime(2016,3,28)
            ,DT.datetime(2016,12,26)
            ,DT.datetime(2017,4,14)
            ,DT.datetime(2017,4,17)
            ,DT.datetime(2017,12,25)
            ,DT.datetime(2017,12,26)
            ,DT.datetime(2018,1,1)
            ,DT.datetime(2018,3,30)
            ,DT.datetime(2018,4,2)
            ,DT.datetime(2018,12,25)
            ,DT.datetime(2018,12,26)
            ,DT.datetime(2019,1,1)
            ,DT.datetime(2019,4,19)
            ,DT.datetime(2019,4,22)
            ,DT.datetime(2019,12,25)
            ,DT.datetime(2019,12,26)
            ,DT.datetime(2020,1,1)
            ,DT.datetime(2020,4,10)
            ,DT.datetime(2020,4,13)
            ,DT.datetime(2020,12,25)
            ,DT.datetime(2021,1,1)
            ,DT.datetime(2021,4,2)
            ,DT.datetime(2021,4,5)
            ,DT.datetime(2022,4,15)
            ,DT.datetime(2022,4,18)
            ,DT.datetime(2022,12,26)
            ,DT.datetime(2023,4,7)
            ,DT.datetime(2023,4,10)
            ,DT.datetime(2023,12,25)
            ,DT.datetime(2023,12,26)
            ,DT.datetime(2024,1,1)
            ,DT.datetime(2024,3,29)
            ,DT.datetime(2024,4,1)
            ,DT.datetime(2024,12,25)
            ,DT.datetime(2024,12,26)
            ,DT.datetime(2025,1,1)
            ,DT.datetime(2025,4,18)
            ,DT.datetime(2025,4,21)
            ,DT.datetime(2025,12,25)
            ,DT.datetime(2025,12,26)
            ,DT.datetime(2026,1,1)
            ,DT.datetime(2026,4,3)
            ,DT.datetime(2026,4,6)
            ,DT.datetime(2026,12,25)
            ,DT.datetime(2027,1,1)
            ,DT.datetime(2027,3,26)
            ,DT.datetime(2027,3,29)
            ,DT.datetime(2028,4,14)
            ,DT.datetime(2028,4,17)
            ,DT.datetime(2028,12,25)
            ,DT.datetime(2028,12,26)
            ,DT.datetime(2029,1,1)
            ,DT.datetime(2029,3,30)
            ,DT.datetime(2029,4,2)
            ,DT.datetime(2029,12,25)
            ,DT.datetime(2029,12,26)
            ,DT.datetime(2030,1,1)
            ,DT.datetime(2030,4,19)
            ,DT.datetime(2030,4,22)
            ,DT.datetime(2030,12,25)
            ,DT.datetime(2030,12,26)
            ,DT.datetime(2031,1,1)
            ,DT.datetime(2031,4,11)
            ,DT.datetime(2031,4,14)
            ,DT.datetime(2031,12,25)
            ,DT.datetime(2031,12,26)
            ,DT.datetime(2032,1,1)
            ,DT.datetime(2032,3,26)
            ,DT.datetime(2032,3,29)
            ,DT.datetime(2033,4,15)
            ,DT.datetime(2033,4,18)
            ,DT.datetime(2033,12,26)
            ,DT.datetime(2034,4,7)
            ,DT.datetime(2034,4,10)
            ,DT.datetime(2034,12,25)
            ,DT.datetime(2034,12,26)
            ,DT.datetime(2035,1,1)
            ,DT.datetime(2035,3,23)
            ,DT.datetime(2035,3,26)
            ,DT.datetime(2035,12,25)
            ,DT.datetime(2035,12,26)
            ,DT.datetime(2036,1,1)
            ,DT.datetime(2036,4,11)
            ,DT.datetime(2036,4,14)
            ,DT.datetime(2036,12,25)
            ,DT.datetime(2036,12,26)
            ,DT.datetime(2037,1,1)
            ,DT.datetime(2037,4,3)
            ,DT.datetime(2037,4,6)
            ,DT.datetime(2037,12,25)
            ,DT.datetime(2038,1,1)
            ,DT.datetime(2038,4,23)
            ,DT.datetime(2038,4,26)
            ,DT.datetime(2039,4,8)
            ,DT.datetime(2039,4,11)
            ,DT.datetime(2039,12,26)
            ,DT.datetime(2040,3,30)
            ,DT.datetime(2040,4,2)
            ,DT.datetime(2040,12,25)
            ,DT.datetime(2040,12,26)
            ,DT.datetime(2041,1,1)
            ,DT.datetime(2041,4,19)
            ,DT.datetime(2041,4,22)
            ,DT.datetime(2041,12,25)
            ,DT.datetime(2041,12,26)
            ,DT.datetime(2042,1,1)
            ,DT.datetime(2042,4,4)
            ,DT.datetime(2042,4,7)
            ,DT.datetime(2042,12,25)
            ,DT.datetime(2042,12,26)
            ,DT.datetime(2043,1,1)
            ,DT.datetime(2043,3,27)
            ,DT.datetime(2043,3,30)
            ,DT.datetime(2043,12,25)
            ,DT.datetime(2044,1,1)
            ,DT.datetime(2044,4,15)
            ,DT.datetime(2044,4,18)
            ,DT.datetime(2044,12,26)
            ,DT.datetime(2045,4,7)
            ,DT.datetime(2045,4,10)
            ,DT.datetime(2045,12,25)
            ,DT.datetime(2045,12,26)
            ,DT.datetime(2046,1,1)
            ,DT.datetime(2046,3,19)
            ,DT.datetime(2046,3,23)
            ,DT.datetime(2046,12,25)
            ,DT.datetime(2046,12,26)
            ,DT.datetime(2047,1,1)
            ,DT.datetime(2047,4,12)
            ,DT.datetime(2047,4,15)
            ,DT.datetime(2047,12,25)
            ,DT.datetime(2047,12,26)
            ,DT.datetime(2048,1,1)
            ,DT.datetime(2048,4,3)
            ,DT.datetime(2048,4,6)
            ,DT.datetime(2048,12,25)
            ,DT.datetime(2049,1,1)
            ,DT.datetime(2049,4,16)
            ,DT.datetime(2049,4,19)
            ,DT.datetime(2050,4,8)
            ,DT.datetime(2050,4,11)
            ,DT.datetime(2050,12,26)
            ,DT.datetime(2051,3,31)
            ,DT.datetime(2051,4,3)
            ,DT.datetime(2051,12,25)
            ,DT.datetime(2051,12,26)
            ,DT.datetime(2052,1,1)
            ,DT.datetime(2052,4,19)
            ,DT.datetime(2052,4,22)
            ,DT.datetime(2052,12,25)
            ,DT.datetime(2052,12,26)
            ,DT.datetime(2053,1,1)
            ,DT.datetime(2053,4,4)
            ,DT.datetime(2053,4,7)
            ,DT.datetime(2053,12,25)
            ,DT.datetime(2053,12,26)
            ,DT.datetime(2054,1,1)
            ,DT.datetime(2054,3,27)
            ,DT.datetime(2054,3,30)
            ,DT.datetime(2054,12,25)
            ,DT.datetime(2055,1,1)
            ,DT.datetime(2055,4,16)
            ,DT.datetime(2055,4,19)
            ,DT.datetime(2056,3,31)
            ,DT.datetime(2056,4,3)
            ,DT.datetime(2056,12,25)
            ,DT.datetime(2056,12,26)
            ,DT.datetime(2057,1,1)
            ,DT.datetime(2057,4,20)
            ,DT.datetime(2057,4,23)
            ,DT.datetime(2057,12,25)
            ,DT.datetime(2057,12,26)
            ,DT.datetime(2058,1,1)
            ,DT.datetime(2058,4,12)
            ,DT.datetime(2058,4,15)
            ,DT.datetime(2058,12,25)
            ,DT.datetime(2058,12,26)
            ,DT.datetime(2059,1,1)
            ,DT.datetime(2059,3,28)
            ,DT.datetime(2059,3,31)
            ,DT.datetime(2059,12,25)
            ,DT.datetime(2059,12,26)
            ,DT.datetime(2060,1,1)
            ,DT.datetime(2060,4,16)
            ,DT.datetime(2060,4,19)
            ,DT.datetime(2061,4,8)
            ,DT.datetime(2061,4,11)
            ,DT.datetime(2061,12,26)
            ,DT.datetime(2062,3,24)
            ,DT.datetime(2062,3,27)
            ,DT.datetime(2062,5,1)
            ,DT.datetime(2062,12,25)
            ,DT.datetime(2062,12,26)
            ,DT.datetime(2063,1,1)
            ,DT.datetime(2063,4,13)
            ,DT.datetime(2063,4,16)
            ,DT.datetime(2063,5,1)
            ,DT.datetime(2063,12,25)
            ,DT.datetime(2063,12,26)
            ,DT.datetime(2064,1,1)
            ,DT.datetime(2064,4,4)
            ,DT.datetime(2064,4,7)
            ,DT.datetime(2064,5,1)
            ,DT.datetime(2064,12,25)
            ,DT.datetime(2064,12,26)
            ,DT.datetime(2065,1,1)
            ,DT.datetime(2065,3,27)
            ,DT.datetime(2065,3,30)
            ,DT.datetime(2065,5,1)
            ,DT.datetime(2065,12,25)
        ]
    
    def holidays(self):
        return self.Holidays
    

class USDCalendar(Calendar):
    
    def __init__(self):
        self.Holidays = [
            DT.datetime(2014,12,25)
            ,DT.datetime(2015,1,1)
            ,DT.datetime(2015,1,19)
            ,DT.datetime(2015,2,16)
            ,DT.datetime(2015,4,3)
            ,DT.datetime(2015,5,25)
            ,DT.datetime(2015,7,3)
            ,DT.datetime(2015,9,7)
            ,DT.datetime(2015,10,12)
            ,DT.datetime(2015,11,11)
            ,DT.datetime(2015,11,26)
            ,DT.datetime(2015,12,25)
            ,DT.datetime(2016,1,1)
            ,DT.datetime(2016,1,18)
            ,DT.datetime(2016,2,15)
            ,DT.datetime(2016,3,25)
            ,DT.datetime(2016,5,30)
            ,DT.datetime(2016,7,4)
            ,DT.datetime(2016,9,5)
            ,DT.datetime(2016,10,10)
            ,DT.datetime(2016,11,11)
            ,DT.datetime(2016,11,24)
            ,DT.datetime(2016,12,26)
            ,DT.datetime(2017,1,2)
            ,DT.datetime(2017,1,16)
            ,DT.datetime(2017,2,20)
            ,DT.datetime(2017,4,14)
            ,DT.datetime(2017,5,29)
            ,DT.datetime(2017,7,4)
            ,DT.datetime(2017,9,4)
            ,DT.datetime(2017,10,9)
            ,DT.datetime(2017,11,10)
            ,DT.datetime(2017,11,23)
            ,DT.datetime(2017,12,25)
            ,DT.datetime(2018,1,1)
            ,DT.datetime(2018,1,15)
            ,DT.datetime(2018,2,19)
            ,DT.datetime(2018,3,30)
            ,DT.datetime(2018,5,28)
            ,DT.datetime(2018,7,4)
            ,DT.datetime(2018,9,3)
            ,DT.datetime(2018,10,8)
            ,DT.datetime(2018,11,12)
            ,DT.datetime(2018,11,22)
            ,DT.datetime(2018,12,25)
            ,DT.datetime(2019,1,1)
            ,DT.datetime(2019,1,21)
            ,DT.datetime(2019,2,18)
            ,DT.datetime(2019,4,19)
            ,DT.datetime(2019,5,27)
            ,DT.datetime(2019,7,4)
            ,DT.datetime(2019,9,2)
            ,DT.datetime(2019,10,14)
            ,DT.datetime(2019,11,11)
            ,DT.datetime(2019,11,28)
            ,DT.datetime(2019,12,25)
            ,DT.datetime(2020,1,1)
            ,DT.datetime(2020,1,20)
            ,DT.datetime(2020,2,17)
            ,DT.datetime(2020,4,10)
            ,DT.datetime(2020,5,25)
            ,DT.datetime(2020,7,3)
            ,DT.datetime(2020,9,7)
            ,DT.datetime(2020,10,12)
            ,DT.datetime(2020,11,11)
            ,DT.datetime(2020,11,26)
            ,DT.datetime(2020,12,25)
            ,DT.datetime(2021,1,1)
            ,DT.datetime(2021,1,18)
            ,DT.datetime(2021,2,15)
            ,DT.datetime(2021,4,2)
            ,DT.datetime(2021,5,31)
            ,DT.datetime(2021,7,5)
            ,DT.datetime(2021,9,6)
            ,DT.datetime(2021,10,11)
            ,DT.datetime(2021,11,11)
            ,DT.datetime(2021,11,25)
            ,DT.datetime(2021,12,24)
            ,DT.datetime(2022,1,17)
            ,DT.datetime(2022,2,21)
            ,DT.datetime(2022,4,15)
            ,DT.datetime(2022,5,30)
            ,DT.datetime(2022,7,4)
            ,DT.datetime(2022,9,5)
            ,DT.datetime(2022,10,10)
            ,DT.datetime(2022,11,11)
            ,DT.datetime(2022,11,24)
            ,DT.datetime(2022,12,26)
            ,DT.datetime(2023,1,2)
            ,DT.datetime(2023,1,16)
            ,DT.datetime(2023,2,20)
            ,DT.datetime(2023,4,7)
            ,DT.datetime(2023,5,29)
            ,DT.datetime(2023,7,4)
            ,DT.datetime(2023,9,4)
            ,DT.datetime(2023,10,9)
            ,DT.datetime(2023,11,10)
            ,DT.datetime(2023,11,23)
            ,DT.datetime(2023,12,25)
            ,DT.datetime(2024,1,1)
            ,DT.datetime(2024,1,15)
            ,DT.datetime(2024,2,19)
            ,DT.datetime(2024,3,29)
            ,DT.datetime(2024,5,27)
            ,DT.datetime(2024,7,4)
            ,DT.datetime(2024,9,2)
            ,DT.datetime(2024,10,14)
            ,DT.datetime(2024,11,11)
            ,DT.datetime(2024,11,28)
            ,DT.datetime(2024,12,25)
            ,DT.datetime(2025,1,1)
            ,DT.datetime(2025,1,20)
            ,DT.datetime(2025,2,17)
            ,DT.datetime(2025,4,18)
            ,DT.datetime(2025,5,26)
            ,DT.datetime(2025,7,4)
            ,DT.datetime(2025,9,1)
            ,DT.datetime(2025,10,13)
            ,DT.datetime(2025,11,11)
            ,DT.datetime(2025,11,27)
            ,DT.datetime(2025,12,25)
            ,DT.datetime(2026,1,1)
            ,DT.datetime(2026,1,19)
            ,DT.datetime(2026,2,16)
            ,DT.datetime(2026,3,26)
            ,DT.datetime(2026,4,3)
            ,DT.datetime(2026,5,25)
            ,DT.datetime(2026,7,3)
            ,DT.datetime(2026,9,7)
            ,DT.datetime(2026,10,12)
            ,DT.datetime(2026,11,11)
            ,DT.datetime(2026,11,26)
            ,DT.datetime(2026,12,25)
            ,DT.datetime(2027,1,1)
            ,DT.datetime(2027,1,18)
            ,DT.datetime(2027,2,15)
            ,DT.datetime(2027,5,31)
            ,DT.datetime(2027,7,5)
            ,DT.datetime(2027,9,6)
            ,DT.datetime(2027,10,11)
            ,DT.datetime(2027,11,11)
            ,DT.datetime(2027,11,25)
            ,DT.datetime(2027,12,24)
            ,DT.datetime(2028,1,17)
            ,DT.datetime(2028,2,21)
            ,DT.datetime(2028,4,14)
            ,DT.datetime(2028,5,29)
            ,DT.datetime(2028,7,4)
            ,DT.datetime(2028,9,4)
            ,DT.datetime(2028,10,9)
            ,DT.datetime(2028,11,10)
            ,DT.datetime(2028,11,23)
            ,DT.datetime(2028,12,25)
            ,DT.datetime(2029,1,1)
            ,DT.datetime(2029,1,15)
            ,DT.datetime(2029,2,19)
            ,DT.datetime(2029,3,30)
            ,DT.datetime(2029,5,28)
            ,DT.datetime(2029,7,4)
            ,DT.datetime(2029,9,3)
            ,DT.datetime(2029,10,8)
            ,DT.datetime(2029,11,12)
            ,DT.datetime(2029,11,22)
            ,DT.datetime(2029,12,25)
            ,DT.datetime(2030,1,1)
            ,DT.datetime(2030,1,21)
            ,DT.datetime(2030,2,18)
            ,DT.datetime(2030,4,19)
            ,DT.datetime(2030,5,27)
            ,DT.datetime(2030,7,4)
            ,DT.datetime(2030,9,2)
            ,DT.datetime(2030,10,14)
            ,DT.datetime(2030,11,11)
            ,DT.datetime(2030,11,28)
            ,DT.datetime(2030,12,25)
            ,DT.datetime(2031,1,1)
            ,DT.datetime(2031,1,20)
            ,DT.datetime(2031,2,17)
            ,DT.datetime(2031,4,11)
            ,DT.datetime(2031,5,26)
            ,DT.datetime(2031,7,4)
            ,DT.datetime(2031,9,1)
            ,DT.datetime(2031,10,13)
            ,DT.datetime(2031,11,11)
            ,DT.datetime(2031,11,27)
            ,DT.datetime(2031,12,25)
            ,DT.datetime(2032,1,1)
            ,DT.datetime(2032,1,19)
            ,DT.datetime(2032,2,16)
            ,DT.datetime(2032,3,26)
            ,DT.datetime(2032,5,31)
            ,DT.datetime(2032,7,5)
            ,DT.datetime(2032,9,6)
            ,DT.datetime(2032,10,11)
            ,DT.datetime(2032,11,11)
            ,DT.datetime(2032,11,25)
            ,DT.datetime(2032,12,24)
            ,DT.datetime(2033,1,17)
            ,DT.datetime(2033,2,21)
            ,DT.datetime(2033,4,15)
            ,DT.datetime(2033,5,30)
            ,DT.datetime(2033,7,4)
            ,DT.datetime(2033,9,5)
            ,DT.datetime(2033,10,10)
            ,DT.datetime(2033,11,11)
            ,DT.datetime(2033,11,24)
            ,DT.datetime(2033,12,26)
            ,DT.datetime(2034,1,2)
            ,DT.datetime(2034,1,16)
            ,DT.datetime(2034,2,20)
            ,DT.datetime(2034,4,7)
            ,DT.datetime(2034,5,29)
            ,DT.datetime(2034,7,4)
            ,DT.datetime(2034,9,4)
            ,DT.datetime(2034,10,9)
            ,DT.datetime(2034,11,23)
            ,DT.datetime(2034,12,25)
            ,DT.datetime(2035,1,1)
            ,DT.datetime(2035,1,15)
            ,DT.datetime(2035,2,19)
            ,DT.datetime(2035,3,23)
            ,DT.datetime(2035,5,28)
            ,DT.datetime(2035,7,4)
            ,DT.datetime(2035,9,3)
            ,DT.datetime(2035,10,8)
            ,DT.datetime(2035,11,12)
            ,DT.datetime(2035,11,22)
            ,DT.datetime(2035,12,25)
            ,DT.datetime(2036,1,1)
            ,DT.datetime(2036,2,18)
            ,DT.datetime(2036,4,11)
            ,DT.datetime(2036,5,26)
            ,DT.datetime(2036,7,4)
            ,DT.datetime(2036,9,1)
            ,DT.datetime(2036,10,13)
            ,DT.datetime(2036,11,11)
            ,DT.datetime(2036,11,27)
            ,DT.datetime(2036,12,25)
            ,DT.datetime(2037,1,1)
            ,DT.datetime(2037,1,19)
            ,DT.datetime(2037,2,16)
            ,DT.datetime(2037,5,25)
            ,DT.datetime(2037,7,3)
            ,DT.datetime(2037,9,7)
            ,DT.datetime(2037,10,12)
            ,DT.datetime(2037,11,11)
            ,DT.datetime(2037,11,26)
            ,DT.datetime(2037,12,25)
            ,DT.datetime(2038,1,18)
            ,DT.datetime(2038,2,15)
            ,DT.datetime(2038,5,31)
            ,DT.datetime(2038,7,5)
            ,DT.datetime(2038,9,6)
            ,DT.datetime(2038,10,11)
            ,DT.datetime(2038,11,11)
            ,DT.datetime(2038,11,25)
            ,DT.datetime(2038,12,24)
            ,DT.datetime(2039,1,17)
            ,DT.datetime(2039,2,21)
            ,DT.datetime(2039,5,30)
            ,DT.datetime(2039,7,4)
            ,DT.datetime(2039,9,5)
            ,DT.datetime(2039,10,10)
            ,DT.datetime(2039,11,11)
            ,DT.datetime(2039,11,24)
            ,DT.datetime(2039,12,26)
            ,DT.datetime(2040,1,2)
            ,DT.datetime(2040,1,16)
            ,DT.datetime(2040,2,20)
            ,DT.datetime(2040,3,30)
            ,DT.datetime(2040,5,28)
            ,DT.datetime(2040,7,4)
            ,DT.datetime(2040,9,3)
            ,DT.datetime(2040,10,8)
            ,DT.datetime(2040,11,12)
            ,DT.datetime(2040,11,22)
            ,DT.datetime(2040,12,25)
            ,DT.datetime(2041,1,1)
            ,DT.datetime(2041,1,21)
            ,DT.datetime(2041,2,18)
            ,DT.datetime(2041,4,19)
            ,DT.datetime(2041,5,27)
            ,DT.datetime(2041,7,4)
            ,DT.datetime(2041,9,2)
            ,DT.datetime(2041,10,14)
            ,DT.datetime(2041,11,11)
            ,DT.datetime(2041,11,28)
            ,DT.datetime(2041,12,25)
            ,DT.datetime(2042,1,1)
            ,DT.datetime(2042,1,20)
            ,DT.datetime(2042,2,17)
            ,DT.datetime(2042,4,4)
            ,DT.datetime(2042,5,26)
            ,DT.datetime(2042,7,4)
            ,DT.datetime(2042,9,1)
            ,DT.datetime(2042,10,13)
            ,DT.datetime(2042,11,11)
            ,DT.datetime(2042,11,27)
            ,DT.datetime(2042,12,25)
            ,DT.datetime(2043,1,1)
            ,DT.datetime(2043,1,19)
            ,DT.datetime(2043,2,16)
            ,DT.datetime(2043,3,27)
            ,DT.datetime(2043,5,25)
            ,DT.datetime(2043,7,3)
            ,DT.datetime(2043,9,7)
            ,DT.datetime(2043,10,12)
            ,DT.datetime(2043,11,11)
            ,DT.datetime(2043,11,26)
            ,DT.datetime(2043,12,25)
            ,DT.datetime(2044,1,1)
            ,DT.datetime(2044,1,18)
            ,DT.datetime(2044,2,15)
            ,DT.datetime(2044,4,15)
            ,DT.datetime(2044,5,30)
            ,DT.datetime(2044,7,4)
            ,DT.datetime(2044,9,5)
            ,DT.datetime(2044,10,10)
            ,DT.datetime(2044,11,11)
            ,DT.datetime(2044,11,24)
            ,DT.datetime(2044,12,26)
            ,DT.datetime(2045,1,2)
            ,DT.datetime(2045,1,16)
            ,DT.datetime(2045,2,20)
            ,DT.datetime(2045,4,7)
            ,DT.datetime(2045,5,29)
            ,DT.datetime(2045,7,4)
            ,DT.datetime(2045,9,4)
            ,DT.datetime(2045,10,9)
            ,DT.datetime(2045,11,10)
            ,DT.datetime(2045,11,23)
            ,DT.datetime(2045,12,25)
            ,DT.datetime(2046,1,1)
            ,DT.datetime(2046,1,15)
            ,DT.datetime(2046,2,19)
            ,DT.datetime(2046,3,23)
            ,DT.datetime(2046,5,28)
            ,DT.datetime(2046,7,4)
            ,DT.datetime(2046,9,3)
            ,DT.datetime(2046,10,8)
            ,DT.datetime(2046,11,12)
            ,DT.datetime(2046,11,22)
            ,DT.datetime(2046,12,25)
            ,DT.datetime(2047,1,1)
            ,DT.datetime(2047,1,21)
            ,DT.datetime(2047,2,18)
            ,DT.datetime(2047,4,12)
            ,DT.datetime(2047,5,27)
            ,DT.datetime(2047,7,4)
            ,DT.datetime(2047,9,2)
            ,DT.datetime(2047,10,14)
            ,DT.datetime(2047,11,11)
            ,DT.datetime(2047,11,28)
            ,DT.datetime(2047,12,25)
            ,DT.datetime(2048,1,1)
            ,DT.datetime(2048,1,20)
            ,DT.datetime(2048,2,17)
            ,DT.datetime(2048,4,3)
            ,DT.datetime(2048,5,25)
            ,DT.datetime(2048,7,3)
            ,DT.datetime(2048,9,7)
            ,DT.datetime(2048,10,12)
            ,DT.datetime(2048,11,11)
            ,DT.datetime(2048,11,26)
            ,DT.datetime(2048,12,25)
            ,DT.datetime(2049,1,1)
            ,DT.datetime(2049,1,18)
            ,DT.datetime(2049,2,15)
            ,DT.datetime(2049,4,16)
            ,DT.datetime(2049,5,31)
            ,DT.datetime(2049,7,5)
            ,DT.datetime(2049,9,6)
            ,DT.datetime(2049,10,11)
            ,DT.datetime(2049,11,11)
            ,DT.datetime(2049,11,25)
            ,DT.datetime(2049,12,24)
            ,DT.datetime(2050,1,17)
            ,DT.datetime(2050,2,21)
            ,DT.datetime(2050,5,30)
            ,DT.datetime(2050,7,4)
            ,DT.datetime(2050,9,5)
            ,DT.datetime(2050,10,10)
            ,DT.datetime(2050,11,11)
            ,DT.datetime(2050,11,24)
            ,DT.datetime(2050,12,26)
            ,DT.datetime(2051,1,2)
            ,DT.datetime(2051,1,16)
            ,DT.datetime(2051,2,20)
            ,DT.datetime(2051,3,30)
            ,DT.datetime(2051,5,29)
            ,DT.datetime(2051,7,4)
            ,DT.datetime(2051,10,9)
            ,DT.datetime(2051,11,22)
            ,DT.datetime(2051,12,25)
            ,DT.datetime(2052,1,1)
            ,DT.datetime(2052,1,15)
            ,DT.datetime(2052,2,19)
            ,DT.datetime(2052,3,22)
            ,DT.datetime(2052,5,27)
            ,DT.datetime(2052,7,4)
            ,DT.datetime(2052,9,2)
            ,DT.datetime(2052,10,7)
            ,DT.datetime(2052,11,12)
            ,DT.datetime(2052,11,21)
            ,DT.datetime(2052,12,25)
            ,DT.datetime(2053,1,1)
            ,DT.datetime(2053,1,20)
            ,DT.datetime(2053,2,17)
            ,DT.datetime(2053,4,18)
            ,DT.datetime(2053,5,26)
            ,DT.datetime(2053,7,4)
            ,DT.datetime(2053,9,1)
            ,DT.datetime(2053,10,13)
            ,DT.datetime(2053,11,11)
            ,DT.datetime(2053,11,27)
            ,DT.datetime(2053,12,25)
            ,DT.datetime(2054,1,1)
            ,DT.datetime(2054,1,19)
            ,DT.datetime(2054,2,16)
            ,DT.datetime(2054,4,3)
            ,DT.datetime(2054,5,25)
            ,DT.datetime(2054,7,3)
            ,DT.datetime(2054,9,7)
            ,DT.datetime(2054,10,12)
            ,DT.datetime(2054,11,11)
            ,DT.datetime(2054,11,26)
            ,DT.datetime(2054,12,25)
            ,DT.datetime(2055,1,1)
            ,DT.datetime(2055,1,18)
            ,DT.datetime(2055,2,15)
            ,DT.datetime(2055,3,26)
            ,DT.datetime(2055,5,31)
            ,DT.datetime(2055,7,5)
            ,DT.datetime(2055,9,6)
            ,DT.datetime(2055,10,11)
            ,DT.datetime(2055,11,11)
            ,DT.datetime(2055,11,25)
            ,DT.datetime(2055,12,24)
            ,DT.datetime(2056,1,17)
            ,DT.datetime(2056,2,21)
            ,DT.datetime(2056,4,14)
            ,DT.datetime(2056,5,29)
            ,DT.datetime(2056,7,4)
            ,DT.datetime(2056,9,4)
            ,DT.datetime(2056,10,9)
            ,DT.datetime(2056,11,10)
            ,DT.datetime(2056,11,23)
            ,DT.datetime(2056,12,25)
            ,DT.datetime(2057,1,1)
            ,DT.datetime(2057,1,15)
            ,DT.datetime(2057,2,19)
            ,DT.datetime(2057,3,30)
            ,DT.datetime(2057,5,28)
            ,DT.datetime(2057,7,4)
            ,DT.datetime(2057,9,3)
            ,DT.datetime(2057,10,8)
            ,DT.datetime(2057,11,12)
            ,DT.datetime(2057,11,22)
            ,DT.datetime(2057,12,25)
            ,DT.datetime(2058,1,1)
            ,DT.datetime(2058,1,21)
            ,DT.datetime(2058,2,18)
            ,DT.datetime(2058,4,19)
            ,DT.datetime(2058,5,27)
            ,DT.datetime(2058,7,4)
            ,DT.datetime(2058,9,2)
            ,DT.datetime(2058,10,14)
            ,DT.datetime(2058,11,11)
            ,DT.datetime(2058,11,28)
            ,DT.datetime(2058,12,25)
            ,DT.datetime(2059,1,1)
            ,DT.datetime(2059,1,20)
            ,DT.datetime(2059,2,17)
            ,DT.datetime(2059,4,11)
            ,DT.datetime(2059,5,26)
            ,DT.datetime(2059,7,4)
            ,DT.datetime(2059,9,1)
            ,DT.datetime(2059,10,13)
            ,DT.datetime(2059,11,11)
            ,DT.datetime(2059,11,27)
            ,DT.datetime(2059,12,25)
            ,DT.datetime(2060,1,1)
            ,DT.datetime(2060,1,19)
            ,DT.datetime(2060,2,16)
            ,DT.datetime(2060,3,26)
            ,DT.datetime(2060,5,31)
            ,DT.datetime(2060,7,5)
            ,DT.datetime(2060,9,6)
            ,DT.datetime(2060,10,11)
            ,DT.datetime(2060,11,11)
            ,DT.datetime(2060,11,25)
            ,DT.datetime(2060,12,24)
            ,DT.datetime(2061,1,17)
            ,DT.datetime(2061,2,21)
            ,DT.datetime(2061,4,15)
            ,DT.datetime(2061,5,30)
            ,DT.datetime(2061,7,4)
            ,DT.datetime(2061,9,5)
            ,DT.datetime(2061,10,10)
            ,DT.datetime(2061,11,11)
            ,DT.datetime(2061,11,24)
            ,DT.datetime(2062,1,2)
            ,DT.datetime(2062,1,16)
            ,DT.datetime(2062,2,20)
            ,DT.datetime(2062,4,14)
            ,DT.datetime(2062,5,29)
            ,DT.datetime(2062,7,5)
            ,DT.datetime(2062,9,4)
            ,DT.datetime(2062,11,23)
            ,DT.datetime(2062,12,25)
            ,DT.datetime(2063,1,1)
            ,DT.datetime(2063,1,15)
            ,DT.datetime(2063,2,19)
            ,DT.datetime(2063,4,6)
            ,DT.datetime(2063,5,28)
            ,DT.datetime(2063,7,4)
            ,DT.datetime(2063,9,3)
            ,DT.datetime(2063,10,8)
            ,DT.datetime(2063,11,12)
            ,DT.datetime(2063,11,22)
            ,DT.datetime(2063,12,25)
            ,DT.datetime(2064,1,1)
            ,DT.datetime(2064,1,21)
            ,DT.datetime(2064,2,18)
            ,DT.datetime(2064,3,21)
            ,DT.datetime(2064,5,26)
            ,DT.datetime(2064,7,4)
            ,DT.datetime(2064,9,1)
            ,DT.datetime(2064,10,13)
            ,DT.datetime(2064,11,11)
            ,DT.datetime(2064,11,27)
            ,DT.datetime(2064,12,25)
            ,DT.datetime(2065,1,1)
            ,DT.datetime(2065,1,19)
            ,DT.datetime(2065,2,16)
            ,DT.datetime(2065,4,9)
            ,DT.datetime(2065,11,11)
            ,DT.datetime(2065,11,25)
            ,DT.datetime(2065,12,24)
            ,DT.datetime(2065,12,25)
            ,DT.datetime(2065,12,31)
            ,DT.datetime(2066,1,1)
            ,DT.datetime(2066,3,25)
            ,DT.datetime(2066,11,11)
            ,DT.datetime(2066,11,24)
            ,DT.datetime(2067,1,17)
            ,DT.datetime(2067,2,21)
            ,DT.datetime(2067,3,25)
            ,DT.datetime(2067,5,30)
            ,DT.datetime(2067,7,4)
            ,DT.datetime(2067,9,5)
            ,DT.datetime(2067,10,10)
            ,DT.datetime(2067,11,11)
            ,DT.datetime(2067,11,24)
            ,DT.datetime(2067,12,26)
            ,DT.datetime(2068,1,2)
            ,DT.datetime(2068,1,16)
            ,DT.datetime(2068,2,20)
            ,DT.datetime(2068,4,13)
            ,DT.datetime(2068,5,28)
            ,DT.datetime(2068,7,4)
            ,DT.datetime(2068,9,3)
            ,DT.datetime(2068,10,8)
            ,DT.datetime(2068,11,12)
            ,DT.datetime(2068,11,22)
            ,DT.datetime(2068,12,25)
            ,DT.datetime(2069,1,1)
            ,DT.datetime(2069,1,21)
            ,DT.datetime(2069,2,18)
            ,DT.datetime(2069,3,21)
            ,DT.datetime(2069,7,4)
            ,DT.datetime(2069,11,11)
            ,DT.datetime(2069,11,27)
            ,DT.datetime(2069,12,25)
            ,DT.datetime(2070,1,1)
            ,DT.datetime(2070,1,20)
            ,DT.datetime(2070,2,17)
            ,DT.datetime(2070,4,18)
            ,DT.datetime(2070,5,26)
            ,DT.datetime(2070,7,4)
            ,DT.datetime(2070,9,1)
            ,DT.datetime(2070,10,13)
            ,DT.datetime(2070,11,11)
            ,DT.datetime(2070,11,27)
            ,DT.datetime(2070,12,25)
            ,DT.datetime(2071,1,1)
            ,DT.datetime(2071,1,20)
            ,DT.datetime(2071,2,17)
            ,DT.datetime(2071,5,26)
            ,DT.datetime(2071,7,3)
            ,DT.datetime(2071,9,1)
            ,DT.datetime(2071,10,13)
            ,DT.datetime(2071,11,11)
            ,DT.datetime(2071,11,26)
            ,DT.datetime(2071,12,25)
            ,DT.datetime(2072,1,1)
            ,DT.datetime(2072,1,20)
            ,DT.datetime(2072,2,17)
            ,DT.datetime(2072,3,25)
            ,DT.datetime(2072,5,31)
            ,DT.datetime(2072,7,4)
            ,DT.datetime(2072,9,1)
            ,DT.datetime(2072,10,11)
            ,DT.datetime(2072,11,11)
            ,DT.datetime(2072,11,24)
            ,DT.datetime(2072,12,26)
            ,DT.datetime(2073,1,2)
            ,DT.datetime(2073,1,16)
            ,DT.datetime(2073,2,20)
            ,DT.datetime(2073,4,14)
            ,DT.datetime(2073,5,29)
            ,DT.datetime(2073,7,4)
            ,DT.datetime(2073,9,4)
            ,DT.datetime(2073,10,9)
            ,DT.datetime(2073,11,10)
            ,DT.datetime(2073,11,23)
            ,DT.datetime(2073,12,25)
            ,DT.datetime(2074,1,1)
            ,DT.datetime(2074,1,15)
            ,DT.datetime(2074,2,19)
            ,DT.datetime(2074,3,30)
            ,DT.datetime(2074,5,28)
            ,DT.datetime(2074,7,4)
            ,DT.datetime(2074,9,3)
            ,DT.datetime(2074,10,8)
            ,DT.datetime(2074,11,12)
            ,DT.datetime(2074,11,22)
            ,DT.datetime(2075,1,1)
            ,DT.datetime(2075,1,21)
            ,DT.datetime(2075,2,18)
            ,DT.datetime(2075,4,19)
            ,DT.datetime(2075,5,27)
            ,DT.datetime(2075,7,4)
            ,DT.datetime(2075,9,2)
            ,DT.datetime(2075,10,14)
            ,DT.datetime(2075,11,11)
            ,DT.datetime(2075,11,28)
            ,DT.datetime(2075,12,25)
            ,DT.datetime(2076,1,1)
            ,DT.datetime(2076,1,20)
            ,DT.datetime(2076,2,17)
            ,DT.datetime(2076,4,10)
            ,DT.datetime(2076,5,25)
            ,DT.datetime(2076,7,3)
            ,DT.datetime(2076,9,7)
            ,DT.datetime(2076,10,12)
            ,DT.datetime(2076,11,11)
            ,DT.datetime(2076,11,26)
            ,DT.datetime(2076,12,25)
            ,DT.datetime(2077,1,1)
            ,DT.datetime(2077,1,20)
            ,DT.datetime(2077,2,17)
            ,DT.datetime(2077,3,25)
            ,DT.datetime(2077,5,25)
            ,DT.datetime(2077,7,5)
            ,DT.datetime(2077,9,7)
            ,DT.datetime(2077,10,12)
            ,DT.datetime(2077,11,11)
            ,DT.datetime(2077,11,26)
            ,DT.datetime(2077,12,24)
            ,DT.datetime(2078,1,17)
            ,DT.datetime(2078,2,21)
            ,DT.datetime(2078,4,22)
            ,DT.datetime(2078,5,30)
            ,DT.datetime(2078,7,4)
            ,DT.datetime(2078,9,5)
            ,DT.datetime(2078,10,10)
            ,DT.datetime(2078,11,11)
            ,DT.datetime(2078,11,24)
            ,DT.datetime(2079,1,2)
            ,DT.datetime(2079,1,16)
            ,DT.datetime(2079,2,13)
            ,DT.datetime(2079,4,14)
            ,DT.datetime(2079,5,29)
            ,DT.datetime(2079,7,4)
            ,DT.datetime(2079,9,4)
            ,DT.datetime(2079,10,9)
            ,DT.datetime(2079,11,10)
            ,DT.datetime(2079,11,23)
            ,DT.datetime(2079,12,25)
            ,DT.datetime(2080,1,1)
            ,DT.datetime(2080,1,15)
            ,DT.datetime(2080,2,19)
            ,DT.datetime(2080,3,29)
            ,DT.datetime(2080,5,28)
            ,DT.datetime(2080,7,4)
            ,DT.datetime(2080,9,3)
            ,DT.datetime(2080,10,8)
            ,DT.datetime(2080,11,12)
            ,DT.datetime(2080,11,21)
            ,DT.datetime(2080,12,25)
        ]
    
    def holidays(self):
        return self.Holidays