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

import xlrd
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
    
    singleData[Id] ={}
    
    singleData[Id]['Forward'] = EX.xl_Get_Data(xl_Name, 8, startRow+1, 2, startRow+1, 2)
       
    singleData[Id]['Expiry'] = DT.datetime.strptime(EX.xl_Get_Data(xl_Name, 8, startRow+4, 2, startRow+4, 2)[0], '%m/%d/%Y')
    
    singleData[Id]['Strikes'] = EX.xl_Get_Data(xl_Name, 8, startRow, 7, startRow, 19)

    singleData[Id]['CallBid'] = EX.xl_Get_Data(xl_Name, 8, startRow+1, 7, startRow+1, 19)
    
    singleData[Id]['CallAsk'] = EX.xl_Get_Data(xl_Name, 8, startRow+2, 7, startRow+2, 19)
    
    singleData[Id]['PutBid'] = EX.xl_Get_Data(xl_Name, 8, startRow+3, 7, startRow+3, 19)
    
    singleData[Id]['PutAsk'] = EX.xl_Get_Data(xl_Name, 8, startRow+4, 7, startRow+4, 19)
    
    return singleData    
    

if __name__=='__main__':
    
    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls')
    eonia = CV.DiscountCurve(ins)
    eonia.bootstrap()
    #plt.plot(eonia.dayCountFractions(),eonia.discountFactors())
    #plt.plot(eonia.dayCountFractions(),eonia.zeroRates())

    eur3M = CV.ForwardCurve(ins)
    eur3M.bootstrap()
    #plt.plot(eur3M.dayCountFractions(),eur3M.discountFactors(),'-o')
    #plt.plot(eur3M.dayCountFractions(),eur3M.zeroRates(),'-o')
    
    # Database test    
    
    #dbConfig = DB.DataBaseConfiguration('testDB')
    
    #db = DB.DataBaseHdf5(dbConfig)
    
    #db.saveCurveData(eonia.dictDataToStore())
    
    #data = readSingleStirData('\MarketdataCurve.xlsm',2)
    
    #print data    
    
    #db.saveFuturesData(data)