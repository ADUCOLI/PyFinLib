# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 10:01:27 2014

@author: SYSTEM
"""
import matplotlib.pyplot as plt
import Calendar as CL
import Curves as CV
import DataBase as DB

import VModelUtilities as VMU
import Definitions as DEF

import sys
import os

import ExcelLib as EX
import datetime as DT

def readSingleStirData(name,startRow):
    
    currentDir = os.getcwd()
    sys.path.append(currentDir)
    xl_Name = currentDir + name
        
    singleData = {}
    
    Id = EX.xl_Get_Data_ToUpperCaseString(xl_Name, 8, startRow, 6, startRow, 6)[0]
    print Id    
    
    singleData[Id] ={}
    
    singleData[Id]['Forward'] = EX.xl_Get_Data(xl_Name, 8, startRow+1, 2, startRow+1, 2)
    
    singleData[Id]['Expiry'] = (EX.xl_Get_Data(xl_Name, 8, startRow+4, 2, startRow+4, 2))
#        DT.datetime(
    singleData[Id]['Strikes'] = EX.xl_Get_Data(xl_Name, 8, startRow, 7, startRow, 19)

    singleData[Id]['CallBid'] = EX.xl_Get_Data(xl_Name, 8, startRow+1, 7, startRow+1, 19)
    
    singleData[Id]['CallAsk'] = EX.xl_Get_Data(xl_Name, 8, startRow+2, 7, startRow+2, 19)
    
    singleData[Id]['PutBid'] = EX.xl_Get_Data(xl_Name, 8, startRow+3, 7, startRow+3, 19)
    
    singleData[Id]['PutAsk'] = EX.xl_Get_Data(xl_Name, 8, startRow+4, 7, startRow+4, 19)
    
    return singleData

#def readStirData(name):
#    
#    data = {}    
#    
#    data['forward']EX.xl_Get_Data(name, num_Sheet, row_start, col_start, row_end, col_end)
    
    

if __name__=='__main__':
    
#    eurCal = CL.EURCalendar()
#    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls',eurCal)
#    eonia = CV.DiscountCurve(ins)
#    eonia.bootstrap()
#    plt.plot_date(eonia.maturities(),eonia.discountFactors())
#    plt.plot_date(eonia.maturities(),eonia.zeroRates())
#    plt.show()
#    
#    fwd = 0.0088
#    T = 1.
#    K = 0.1
#    vol = 0.3456712
#    optType = DEF.OptionType.CALL
#    price = VMU.NormalBlackFormula(fwd,T,vol,K,DEF.OptionType.CALL)
#    vol = VMU.BlackImpliedVol(price,fwd,T,K,DEF.OptionType.CALL,DEF.ModelType.NORMAL)

    # Database test    
    
#    dbConfig = DB.DataBaseConfiguration('testDB')
#    
#    db = DB.DataBaseHdf5(dbConfig)
#    
#    eurCal = CL.EURCalendar()
#    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls',eurCal)
#    eonia = CV.DiscountCurve(ins)
#    eonia.bootstrap()
#
#    db.saveCurveData(eonia.dictDataToStore())
    
    data = readSingleStirData('\MarketdataCurve.xlsm',2)
    
    print data