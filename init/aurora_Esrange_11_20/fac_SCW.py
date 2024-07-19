#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 17:41:38 2024

@author: zettergm
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 08:16:33 2023
 
@author: zettergm
"""
 
import xarray
import numpy as np
#from fac_input_to_matt import fac_input
 
def fac_SCW(E: xarray.Dataset, gridflag: int, flagdip: bool) -> xarray.Dataset:
    """
    for 3D sim, FAC up/down 0.5 degree FWHM
    """
 
    if E.mlon.size == 1 or E.mlat.size == 1:
        raise ValueError("for 3D sims only")

    mlat0=65.1
    mlon0=116.9

    mlon=E.mlon
    mlat=E.mlat
    
    
    MLON,MLAT = np.meshgrid(mlon,mlat,indexing="ij")
    wavelength=1
    wavevec=2*np.pi/wavelength

    
    #idx = abs(mlat-mlat0) < wavelength/2.0
    
    
    
    time=E.time
    fac = np.zeros( (time.size,mlon.size,mlat.size) ) 
    
    for t in range(0,E.time.size):
        for i in range(0, mlon.size):
          for j in range(0, mlat.size):  
              if abs(mlat[j]-mlat0) < wavelength/2.0:
                  fac[t,i,j] = ( 1e-6*np.sin(wavevec*(MLAT[i,j]-mlat0))*
                            np.exp(-(MLON[i,j]-mlon0)**2/2.0/5**2) )
            

    for t in range(0,E.time.size):
        E["flagdirich"].loc[E.time[t]] = 0
        k = "Vminx1it" if gridflag == 1 else "Vmaxx1it"
 
        E[k].loc[E.time[t]] = fac[t,:,:]    # order as mlon, mlat for GEMINI
    #    if t>(auxlengthcenter):
    #        E[k].loc[E.time[t]] = E.Jtarg * shapelon * shapelat
    #    else:
    #        E[k].loc[E.time[t]] = E.Jtarg * shapelon * shapelat * (1/(auxlengthcenter) * (t-1))
 
    return E

