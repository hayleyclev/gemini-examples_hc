#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:31:30 2024

@author: clevenger
"""

import xarray
import numpy as np
from lompe.utils.save_load_utils import load_model
import gemini3d
import gemini3d.coord


# thrown into terminal to run - turn into a run script later?
#import matplotlib.pyplot as plt
#import gemini3d
#import gemini3d.model
#gemini3d.model.setup('./config.nml', '/Users/clevenger/Simulations/poker_feb12')

def lompe_fac(E: xarray.Dataset, gridflag: int, flagdip: bool) -> xarray.Dataset:
    """
    for 3D sim, FAC up/down 0.5 degree FWHM
    """
    
    reconstruction_fn = '/Users/clevenger/Projects/data_assimilation/feb_12/lompe_outputs/509_runs/pfisr_superdarn_supermag/large/2023-02-12_102500.nc'
    loaded_model = load_model(reconstruction_fn, time='first')

    if E.mlon.size == 1 or E.mlat.size == 1:
        raise ValueError("for 3D sims only")
    
    # Make evaluation locations
    lt=E.time.size
    timeref=E.time[0]
    timesec=np.empty(lt)
    for it in range(0,lt):
        dt=E.time[it].values-timeref.values
        timesec[it]=dt.astype('timedelta64[s]').item().total_seconds()
    _times = timesec/60    #temporal locations to evaluare for FAC [minuted]
    _mlats=E.mlat
    _mlons=E.mlon
    

    
    #_mlats = np.linspace(50, 85, 800) # mlats to evaluate [degrees]
    #_mlons = np.linspace(centerlon-width*0.5, centerlon+width*0.5, 100) # mlons to evaluate [degrees]
    #shape = (_times.size, _mlats.size, _mlons.size)
    #times, mlats, mlons = np.meshgrid(_times, _mlats, _mlons, indexing='ij') # make 3D grid of locations
    mlats, mlons = np.meshgrid(_mlats, _mlons, indexing='ij') # make 3D grid of locations
    mlatlist=mlats.flatten()
    mlonlist=mlons.flatten()
    thetat = np.deg2rad(90-mlatlist)
    phit = np.deg2rad(mlonlist)
    [glatlist, glonlist] = gemini3d.coord.geomag2geog(thetat, phit)
    fac = loaded_model.FAC(glonlist, glatlist)
    fac = fac.reshape(mlons.shape)
    print("fac shape: ", fac.shape)
    
    fac[np.isnan(fac)] = 0

    #aux=E.time[1:]
    #auxlength=aux.shape[0]
    #auxlengthcenter=np.floor(aux.shape[0]/4)
    #auxtime=E.time[int(np.floor(auxlength))]

    for t in range(0,E.time.size):
        E["flagdirich"].loc[E.time[0]] = 0
        k = "Vminx1it" if gridflag == 1 else "Vmaxx1it"
    
        #breakpoint()

        E[k].loc[E.time[t]] = fac.transpose((1,0))    # order as mlon, mlat for GEMINI
    #    if t>(auxlengthcenter):
    #        E[k].loc[E.time[t]] = E.Jtarg * shapelon * shapelat
    #    else: 
    #        E[k].loc[E.time[t]] = E.Jtarg * shapelon * shapelat * (1/(auxlengthcenter) * (t-1))
    
    #breakpoint()

    return E
