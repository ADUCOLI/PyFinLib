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
    'Futures'
]

###############################################################################
###############################################################################

SubGrouops ={
    'Curves' : ['Eonia','Eur3m','Eur6m'],
    'Futures' : ['Eur3m']
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
        
        if os.path.exists(self.fileName) is False:
        
            self.createDataBaseHdf5()
        
        self.open = False
        
    def createDataBaseHdf5(self):
        
        print ('Created : ' + self.fileName)
                
        f = h5py.File(self.fileName)
        
        f.flush()
        
        f.close()
        
    def openDB(self):
        
        if self.open is True:
            print ('DB already open!')
            return
        self.store = pd.HDFStore(self.fileName)
        self.open = True
        return
        
    def closeDB(self):
        
        if self.open is False:
            print ('DB already closed!')
            return
        self.store.close()
        self.open = False
        return
        
    def saveCurveData(self, dictData):

        if type(dictData) is dict:
            
            panelData = pd.Panel(dictData) 

        else:

            print ('Invalid type in input' + str(type(dictData)))
            return            
            
        self.openDB()
            
        try:

            self.checkInputData(panelData,'Curve')
            curvePanel = self.store['Curve']
            curvePanel = curvePanel.join(panelData)
            self.store.remove('Curve')
            self.store['Curve'] = curvePanel    

        except:
            
            print ('New table Curve initialized!')
            self.store['Curve'] = panelData
        
        self.store.flush()
        self.closeDB()
        
    def saveFuturesData(self, dictData):
        
        if type(dictData) is dict:
            
            panelData = pd.Panel(dictData) 

        else:

            print ('Invalid type in input' + str(type(dictData)))
            return            
            
        self.openDB()
        
        try:

            self.checkInputData(panelData, 'Futures')
            futuresPanel = self.store['Futures']
            futuresPanel = futuresPanel.join(panelData)
            self.store.remove('Futures')
            self.store['Futures'] = futuresPanel    

        except:
            
            print ('New table Curve initialized!')
            self.store['Futures'] = panelData
        
        self.store.flush()
        self.closeDB()
       
    def checkInputData(self, panelData, panelName):
        
        if self.store.keys() is 0:
            return
        
        currentPanel = self.store[panelName]
        
        currentPanel_maxDate = max(currentPanel.keys())
        data_minDate = min(panelData.keys())
        if currentPanel_maxDate < data_minDate:
            return
        
        datesToBeDeleted = pd.bdate_range(data_minDate,currentPanel_maxDate)
        
        for date in datesToBeDeleted:
            dateStr_i = str(date)[:10].replace('-','/')
            self.deleteCurveData(dateStr_i)
        
        return

    def deleteCurveData(self, dateToDelete):
        
        if self.open is False:
            self.openDB()
            
        try:

            curvePanel = self.store['Curve']
            del curvePanel[dateToDelete]
            print ('I am deleting data referring to ' + dateToDelete)            
            self.store.remove('Curve')
            self.store['Curve'] = curvePanel   

        except:
            
            print ('Empty data, table or date not found!')
            
        self.store.flush()
        
        if self.open is False: 
            self.closeDB()
        return
        
    def getStoreCurve(self):
        
        self.openDB()
        curvePanel = self.store['Curve']  
        self.closeDB()
        return curvePanel
    
    def refreshFile(self):

        if self.open is False:
            self.openDB()

        curvePanel = self.store['Curve']
        self.closeDB()
        
        os.remove(self.fileName)      
        self.store = pd.HDFStore(self.fileName)
        self.store['Curve'] = curvePanel
        self.store.close()