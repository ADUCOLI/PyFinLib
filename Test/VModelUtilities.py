# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 09:31:15 2014

@author: Emanuele Mercuri
"""

from scipy.stats import norm
from scipy.optimize import brent
import math
import Definitions as DEF    

def LogNormalBlackFormula(fwd,T,vol,K,optType):
    if optType == DEF.OptionType.FORWARD:
        return fwd
    vol_t = vol*math.sqrt(T)
    if DEF.DoubleEquals(vol_t,0.):
        return DEF.IntrinsicValue(fwd,K,optType)
    d1 = (math.log(fwd/K))/vol_t + 0.5*vol_t
    d2 = d1 - vol_t
    price = {
        DEF.OptionType.CALL: fwd*norm.cdf(d1)-K*norm.cdf(d2),
        DEF.OptionType.PUT: K*norm.cdf(-d2)-fwd*norm.cdf(-d1),
        DEF.OptionType.STRADDLE: fwd*(2.*norm.cdf(d1)-1.0)-K*(2.*norm.cdf(d2)-1.0)
    }
    return price.get(optType,fwd*norm.cdf(d1)-K*norm.cdf(d2))    

    
def NormalBlackFormula(fwd,T,vol,K,optType):
    if optType == DEF.OptionType.FORWARD:
        return fwd        
    vol_t = vol*math.sqrt(T)
    if DEF.DoubleEquals(vol_t,0.):
        return DEF.IntrinsicValue(fwd,K,optType)
    d = (fwd-K)/vol_t
    price = {
        DEF.OptionType.CALL: (fwd-K)*norm.cdf(d)+vol_t*norm.pdf(d),
        DEF.OptionType.PUT: vol_t*norm.pdf(d)-(fwd-K)*norm.cdf(-d),
        DEF.OptionType.STRADDLE: (fwd-K)*(2.*norm.cdf(d)-1)+2.*vol_t*norm.pdf(d)
    }
    return price.get(optType,(fwd-K)*norm.cdf(d)+vol_t*norm.pdf(d))

def BlackImpliedVol(price,fwd,K,T,optType,modelType):
    args = (price,fwd,T,K,optType,modelType)
    def f(x,*args):
        price,fwd,K,T,optType,modelType = args
        fval = {
            DEF.ModelType.NORMAL: NormalBlackFormula(fwd,T,x,K,optType) - price,
            DEF.ModelType.LOGNORMAL: LogNormalBlackFormula(fwd,T,x,K,optType) - price
        }
        return abs(fval.get(modelType,LogNormalBlackFormula(fwd,T,x,K,optType) - price))
    toll = 1e-10
    brack = (toll,10.)
    return brent(f,args,brack,toll)