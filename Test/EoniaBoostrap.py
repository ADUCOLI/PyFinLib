# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 10:01:27 2014

@author: SYSTEM
"""

import xlrd

def xl_Get_Data(xl_Name, num_Sheet, row_start, col_start, row_end, col_end):
    
    # Open the workbook
    try:
        xl_workbook = xlrd.open_workbook(xl_Name)
    except NameError:
        print('uncorected name: ' + xl_Name)
        
    xl_sheet = xl_workbook.sheet_by_index(num_Sheet)

    # Prepare Data
    data = []    
    
    if(row_start==row_end)&(col_start==col_end):
        cell_obj = xl_sheet.cell(row_end, col_end)
        data.append(cell_obj.value)
        return data
    
    # Case row vector:
    if(row_start==row_end):
        for col_idx in range(col_start, col_end):
            cell_obj = xl_sheet.cell(row_start, col_idx)
            data.append(cell_obj.value)
        return data
    
    # Case cols vector:
    if(col_start==col_end):
        for row_idx in range(row_start, row_end):
            cell_obj = xl_sheet.cell(row_idx, col_start)
            data.append(cell_obj.value)
        return data

    data_matrix = []        
        
    for row_idx in range(row_start, row_end):
        data = []
        for col_idx in range(col_start, col_end):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            data.append(cell_obj.value) 
        data_matrix.append(data)
            
    return data_matrix
    
if __name__=='__main__':
    
    import sys
    import os
    currentDir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(currentDir)
    
    Data = {}
    
    #xl_Name = 'C:\Users\Ducoli\Documents\PyFinLib\Test\Eonia_20130927_MktData.xls'
    xl_Name = currentDir+'/Eonia_20130927_MktData.xls'
    
    Data['Maturities'] = xl_Get_Data(xl_Name, 0, 5, 2, 52, 2)
    
    Data['Rates'] = xl_Get_Data(xl_Name, 0, 5, 3, 52, 3)
    
    Data['Spot_Date'] = xl_Get_Data(xl_Name, 0, 1, 3, 1, 3)
    Data['Ref_Date'] = xl_Get_Data(xl_Name, 0, 0, 3, 0, 3)
    
    print Data
    