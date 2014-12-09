# -*- coding: utf-8 -*-
"""
Created on Sat Dec 06 15:48:27 2014

@author: Andrea E Emanuele
"""

import h5py
import os
import time
import pandas as pd

###############################################################################
###############################################################################
   
ModeOptions = {
    'ReadOnlyExistingFile' : 'r',
    'ReadWriteExistingFile' : 'r+',
    'CreateFile' : 'w', 
    'CreateFileFailIfExists' : 'w-',
    'ReadWriteCreate' : 'a'
}

###############################################################################
###############################################################################

Groups = [
    'Curves',
    'VolCapFloor'
]

###############################################################################
###############################################################################

SubGrouops ={
    'Curves' : ['Eonia','Eur3m','Eur6m']
#    'VolCapFloor' : ['Normal Vols','Black Vols']
}

###############################################################################
###############################################################################
    
class DataBaseConfiguration():
    
    def __init__(self, name= None, path = None, modeString = None):
        
        if path is None:
            
            path = os.getcwd()
            
        if name is None:
            
            name = 'db_' + time.strftime("%Y%m%d_%H_%M_%S")
            
        if modeString is None:
            
            self.mode = 'a'
        
        else:
        
            self.mode = ModeOptions[modeString]
            
        self.path = path
        self.name = name
        
    def name(self):
        
        return self.name

    def path(self):
        
        return self.path
        
    def mode(self):
        
        return self.mode
        
    def totalPath(self):
        
        return os.path.join(self.path, self.name)

###############################################################################
###############################################################################
        
class DataBaseHdf5():
    
    def __init__(self,dbConfiguration):
        
        self.dbConfiguration = dbConfiguration
        
        self.fileName = dbConfiguration.totalPath() + '.hdf5'
        
        self.createDataBaseHdf5()
        
        self.isLocked = False
        
    def createDataBaseHdf5(self):
        
        print 'Created : ' + self.fileName
                
        f = h5py.File(self.fileName)
        
        f.flush()
        
        f.close()
        
    def saveCurveData(self, dictData):

        if type(dictData) is dict:
            
            panelData = pd.Panel(dictData) 

        else:

            print 'Invalid type in input'
            return            
            
        store = pd.HDFStore(self.fileName)
            
        try:

            curvePanel = store['Curve']
            curvePanel = curvePanel.join(panelData)
            store['Curve'] = curvePanel     

        except:

            store['Curve'] = panelData
            
        store.flush()
        store.close()

    def deleteCurveData(self, dateToDelete):
        
        store = pd.HDFStore(self.fileName)
                         
        try:

            curvePanel = store['Curve']
            del curvePanel[dateToDelete]
            store['Curve'] = curvePanel     

        except:
            
            print 'Empty data, table or date not found!'
            
        store.close()


if __name__ == "__main__":
    
    import Calendar as CL
    import Curves as CV
    import sys
    
    sys.path.append('C:\Users\Andrea\Documents\Python\Test')
    sys.path.append('C:\Users\Andrea\Documents\PyFinLib\Test')
    
    dbConfig = DataBaseConfiguration('testDB_2')
    
    db = DataBaseHdf5(dbConfig)
    
    eurCal = CL.EURCalendar()
    ins = CV.BootstrapIntrumentSet('/Eonia_20130927_MktData.xls',eurCal)
    eonia = CV.DiscountCurve(ins)
    eonia.bootstrap()


    db.saveCurveData(eonia.dictDataToStore())
    
#    db.deleteCurveData('2014-09-27')
    
    
