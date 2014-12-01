# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 17:52:31 2014

@author: Emanuele Mercuri
"""

def BrentRootSolver(f,args,brack,TOLL=0.0000001,MAX_ITER = 100):
            
    #Set extremes of the interval
    a,b = brack[0], brack[1]
    f_a, f_b = f(a,*args),f(b,*args)
    if (f_a * f_b > 0.) :
        return a
    
    x1 = 0.5*(a+b)
    f_x1 = f(x1,*args)
    
    if f_a * f_x1 < 0.0:
        if abs(f_x1) > abs(f_b):
            temp, f_temp = b, f_b
            b, f_b = x1, f_x1
            x1, f_x1 = temp, f_temp
    else:
        temp, f_temp = b, f_b
        b, f_b = b, f_b
        a, f_a = temp, f_temp
        if abs(f_x1) > abs(f_b):
            temp, f_temp = b, f_b
            b, f_b = x1, f_x1
            x1, f_x1 = temp, f_temp
    x2, f_x2, x3 = a, f_a, a
    
    stepBeforeBisect = False
    for count in range(0,MAX_ITER):
        dX = 0
        #INVERSE QUADRATIC POLYNOMIAL
        if (f_x1 != 0.0) & (f_x2 != 0.0):
            R = f_a / f_x1
            T = f_a / f_x2
            U = f_x2 / f_x1
            
            D = (T - 1) * (R - 1) * (U - 1)
            N = U * R * (T - 1) * x1 - T * (R - 1) * x2 + (U - 1) * a
            
            if (D <> 0):
              s = N / D
              dX = s - x1
        #SECANT
        if (dX == 0):
            D = f_x1 - f_a
            N = -f_x1 * (x1 - a)
            if (D != 0.0):
              dX = N / D
              s = x1 + dX
        #BISECTION
        notValid = (s < (3.0 * a + x1) / 4.0) | (s > x1)
        if stepBeforeBisect:
            if not(notValid):
                notValid = (abs(x1 - x2) <= TOLL) | (abs(s - x1) >= 0.5 * abs(x1 - x2))
        else:
            if count > 0:
                if not(notValid):
                    notValid = (abs(x2 - x3) <= TOLL) | (abs(s - x1) >= 0.5 * abs(x2 - x3))
        
        if notValid:
            s = 0.5 * (a + x1)
            stepBeforeBisect = True
        else:
            stepBeforeBisect = False
        
        f_s = f(s,*args)

        if (f_a * f_s > 0):
            x2, f_x2 = a, f_a
            a, f_a = x1, f_x1            
        else:
            x2, f_x2 = x1, f_x1
        
        x1, f_x1 = s, f_s
        
        if (abs(f_x1) < TOLL):
            return s
    return x1