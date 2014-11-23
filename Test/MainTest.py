# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 10:01:27 2014

@author: SYSTEM
"""
import matplotlib.pyplot as plt

import Curves as CV

if __name__=='__main__':
    
    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls')
    eonia = CV.DiscountCurve(ins)
    eonia.bootstrap()
    plt.plot_date(eonia.maturities(),eonia.discountFactors())
    plt.plot_date(eonia.maturities(),eonia.zeroRates())
    plt.show()