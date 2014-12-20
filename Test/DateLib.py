# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 10:04:18 2014

@author: Ducoli & Mercuri
"""

import Calendar as CL
import datetime as DT
import math

def DayCountFraction(startDate,endDate,basis):
    dcf = {
     'ACT/365': (endDate-startDate).days/365.,
     'ACT/360': (endDate-startDate).days/360.
    }
    return dcf.get(basis,(endDate-startDate).days/365.)
	

class IMMFutureDate:
    
    def __init__(self,theCalendar,thefutureNumber=1,theResetLead=2):
        self.TgtCalendar = theCalendar
        self.FutureNumber = thefutureNumber #Front Month = 1
        self.ResetLead = theResetLead
        
    @staticmethod
    def IMMFutureContractDate(year,month):
        #Compute the third wednesday of a selected month
        immStartDate = DT.datetime(year,month,15)
        dayInWeek=4-(immStartDate.weekday()+2)%7
        if (dayInWeek<0):
            dayInWeek = dayInWeek+7
        else:
            dayInWeek = dayInWeek%7
        return DT.datetime(year,month,15+dayInWeek)

    def IMMFutureContractLastTradingDate(self,year,month):
        #Usually two calendar business date before ContractDate
        immStartDate = IMMFutureDate.IMMFutureContractDate(year,month)
        return self.TgtCalendar.dateAddNumberOfDays(immStartDate,-self.ResetLead)

    def getContractDate(self,refDate):
        #Returns the IMM date for the selected contract
        immNextLastTradingDate = refDate
        for i in range(0,self.FutureNumber):
            immNextLastTradingDate = self.IMMNextFutureContractDate(immNextLastTradingDate)
            if(i+1<self.FutureNumber):
                immNextLastTradingDate = DT.datetime(immNextLastTradingDate.year,immNextLastTradingDate.month,immNextLastTradingDate.day+1)
        return immNextLastTradingDate
        
    def IMMNextFutureContractDate(self,refDate):
        adjNextImmMonth = int(math.ceil(float(refDate.month)/3)*3) - refDate.month
        moveRefDate = self.TgtCalendar.dateAddNumberOfMonths(refDate,adjNextImmMonth)
        immLastTradingDate = self.IMMFutureContractLastTradingDate(moveRefDate.year,moveRefDate.month)
        if((adjNextImmMonth==0) & (moveRefDate.day > immLastTradingDate.day)):
            moveImmDate = self.TgtCalendar.dateAddNumberOfMonths(immLastTradingDate,3)
            immLastTradingDate = self.IMMFutureContractLastTradingDate(moveImmDate.year,moveImmDate.month)
        return immLastTradingDate