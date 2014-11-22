# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 10:01:27 2014

@author: SYSTEM
"""

import matplotlib.pyplot as plt

import Bootstrap as BT

if __name__=='__main__':
    
    ins = BT.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls')
    eonia = BT.Bootstrap(ins)
    eonia.bootDiscountCurve()
    plt.plot_date(eonia.maturities(),eonia.discountFactors())
    plt.show()