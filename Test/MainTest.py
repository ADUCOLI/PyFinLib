# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 10:01:27 2014

@author: SYSTEM
"""
import matplotlib.pyplot as plt
import Calendar as CL
import Curves as CV

#import VModelUtilities as VMU
#import Definitions as DEF

if __name__=='__main__':
    
    eurCal = CL.EURCalendar()
    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls',eurCal)
    eonia = CV.DiscountCurve(ins)
    eonia.bootstrap()
    plt.plot_date(eonia.maturities(),eonia.discountFactors())
    plt.plot_date(eonia.maturities(),eonia.zeroRates())
    plt.show()
    
#    price = VMU.NormalBlackFormula(0.0888,1.,0.1,0.1,DEF.OptionType.CALL)
#    print VMU.BlackImpliedVol(price,0.0888,1.,0.1,DEF.OptionType.CALL,DEF.ModelType.NORMAL)