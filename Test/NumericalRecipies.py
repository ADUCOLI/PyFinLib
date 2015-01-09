# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 17:52:31 2014

@author: Emanuele Mercuri
"""

import numpy as NP

###############################################################
########  BRENT ROOT SOLVER  ##################################
###############################################################

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
            
            if (D != 0):
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
    
    
    
###############################################################
########  CATMULL-ROM SPLINE  #################################
## http://en.wikipedia.org/wiki/Cubic_Hermite_spline        ###
###############################################################

def CatmullRomSpline(fun,x,nodes):
    # fun vector of function values to be interpolated
    # x axis nodes
    # nodes target nodes to interpolate
    
    N, NN = len(x), len(nodes)
    
    def h00(t): return (2.0*t*t*t - 3.0*t*t +1.)
    def h01(t): return (t*t*t - 2.0*t*t +t)
    def h10(t): return (-2.0*t*t*t + 3.0*t*t)
    def h11(t): return (t*t*t - t*t)
    def map(x,xk1,xk): return ((x-xk)/(xk1-xk))
    interpolation = NP.zeros(NN)

    for i in range(0,NN):
        node_tgt = nodes[i]
        values = NP.array(NP.abs(node_tgt-x))
        look_for = values.min()
        for j in range(0,N):
            if(values[j] == look_for):
                if(node_tgt-x[j]<=0.0):
                    K = j-1
                else:
                    K = j
                break

        if(K<=0):
            interpolation[i] = fun[1]
            continue
        if(K+2>=N):
            interpolation[i] = fun[N-2]
            continue
        
        xK_1, fK_1 = x[K-1], fun[K-1]
        xK, fK = x[K], fun[K]
        xK1, fK1 = x[K+1], fun[K+1]
        xK2, fK2 = x[K+2], fun[K+2]
        y_tgt = map(node_tgt,xK1,xK)

        alphaK_1 = -(xK1-xK)/(xK1-xK_1)*h01(y_tgt)
        alphaK = h00(y_tgt) - (xK1-xK)/(xK2-xK)*h11(y_tgt)
        alphaK1 = h10(y_tgt) + (xK1-xK)/(xK1-xK_1)*h01(y_tgt)
        alphaK2 = (xK1-xK)/(xK2-xK)*h11(y_tgt)

        interpolation[i] = alphaK_1*fK_1 + alphaK*fK + alphaK1*fK1 + alphaK2*fK2
    return interpolation

###############################################################
########  NEWTON LAGRANGE POLYNOMIAL INTERPOLATION  ###########
    ### http://en.wikipedia.org/wiki/Newton_polynomial ###
###############################################################

def NewtonLinearInterpol(x,y,z):
    
    m,n = y.shape
    
    a = NP.zeros((max(m,n),max(m,n)))
    f = NP.array(NP.zeros(z.shape))    
    
    for j in range(m):
        a[:,0] = (y[j,:]).transpose()
        
        for i in range(1,n):
            a[i:n,i] = (a[i:n,i-1] - a[i-1,i-1])/(x[j,i:n]-x[j,i-1]).transpose()

        f[j,:] = a[n-1,n-1]*(z-x[j,n-2]) + a[n-2,n-2]
        
        for i in range(2,n):
            f[j,:] = f[j,:]*(z-x[j,n-1-i]) + a[n-1-i,n-1-i]
            
    return f
    
###############################################################
########  HERMITE LAGRANGE POLYNOMIAL INTERPOLATION  ###########
    ### http://en.wikipedia.org/wiki/Newton_polynomial ###
###############################################################
    
def HermiteLinearInterpol(x,y,dy,z):
    
    n = max(x.shape)
    m = max(z.shape)
    herm = []
    
    for j in range(m):
        xx = z[:,j] 
        hxv = 0
        for i in range(n):
            den = 1 
            num = 1 
            xn = x[:,i] 
            derLi = 0
            for k in range(n):
                if k is not i: 
                    num = num*(xx-x[:,k]) 
                    arg = xn-x[:,k];
                    den = den*arg 
                    derLi = derLi+1/arg
                
            Lix2 = pow((num/den),2) 
            p = (1-2*(xx-xn)*derLi)*Lix2;
            q = (xx-xn)*Lix2 
            hxv = hxv+(y[:,i]*p+dy[:,i]*q)
        herm.append(hxv)
    return NP.array(herm).transpose()




    
