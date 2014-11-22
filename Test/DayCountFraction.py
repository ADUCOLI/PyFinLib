# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 10:04:18 2014

@author: Ducoli & Mercuri
"""

def DayCountFraction(startDate,endDate,basis):
    dcf = {
     'ACT/365': (endDate-startDate).days/365.,
     'ACT/360': (endDate-startDate).days/360.,
    }.get('ACT/360',(endDate-startDate).days/360.)
    return dcf