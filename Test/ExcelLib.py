# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 10:16:55 2014

@author: Ducoli & Mercuri
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

    
def xl_Get_Data_ToUpperCaseString(xl_Name, num_Sheet, row_start, col_start, row_end, col_end):
    
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
        # put 'u in front of the string
        # data.append(cell_obj.value.upper().encode('ascii','ignore'))
        data.append(cell_obj.value.upper())
        return data
    
    # Case row vector:
    if(row_start==row_end):
        for col_idx in range(col_start, col_end):
            cell_obj = xl_sheet.cell(row_start, col_idx)
            data.append(cell_obj.value.upper())
        return data
    
    # Case cols vector:
    if(col_start==col_end):
        for row_idx in range(row_start, row_end):
            cell_obj = xl_sheet.cell(row_idx, col_start)
            data.append(cell_obj.value.upper())
        return data

    data_matrix = []        
        
    for row_idx in range(row_start, row_end):
        data = []
        for col_idx in range(col_start, col_end):
            cell_obj = xl_sheet.cell(row_idx, col_idx)
            data.append(cell_obj.value.upper())
        data_matrix.append(data)
            
    return data_matrix