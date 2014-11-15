# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 11:56:20 2014

@author: gianca
"""


import datetime as DT
import workdays as WD

def periodParser(period):
    index = 0
    for i in range(0,len(period)):
        if period[i].isalpha():
            index = i
            break
    
    print index
    out = {}
    out['Number'] = int(period[:index])
    out['strPeriod'] = period[index:]
    return out

#def dateAddPeriod(date,period):
    
if __name__=='__main__':
    
    out = periodParser('180bd')
    print out
    

