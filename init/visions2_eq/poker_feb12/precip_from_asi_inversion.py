#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:58:15 2024

@author: clevenger
"""

import numpy as np
import xarray
#from fac_input_to_matt import fac_input
import gemini3d
import gemini3d.model
import gemini3d.coords
import lompe
from lompe.utils.save_load_utils import load_model

def precip_SCW(pg: xarray.Dataset, Qpeak: float, Qbackground: float):
    mlon_mean = pg.mlon.mean().item()
    mlat_mean = pg.mlat.mean().item()
    
    reconstruction_fn = '/Users/clevenger/Projects/pfisr_synth_data/pygemini_inputs/lompe_run/2023-11-20_225640.nc'
    loaded_model = load_model(reconstruction_fn, time='first')

    # Set some parameters
    centerlon = 105 # the longitudinal cenrte (in degrees) of SCW structure
    width = 90 # longitudinal width in degrees of SCW feature
    #scaling = 10 # increase the resulting FAC magnitudes, since the fitted values are too small (AMPERE does not capture small scale stuff)
    #duration = 200 # duration of time to model, in minutes
    #sigmat = 20 # Sigma of the Gaussian temporal modulation of the pattern [minutes]
    
    # Make evaluation locations
    lt=pg.time.size
    timeref=pg.time[0]
    timesec=np.empty(lt)
    for it in range(0,lt):
        dt=pg.time[it].values-timeref.values
        timesec[it]=dt.astype('timedelta64[s]').item().total_seconds()
    _times = timesec/60    #temporal locations to evaluare for FAC [minuted]
    _mlats=pg.mlat
    _mlons=pg.mlon

    # Discrete auroral precipitation
    times, mlats, mlons = np.meshgrid(_times, _mlats, _mlons, indexing='ij') # make 3D grid of locations
    mlatlist=mlats.flatten()
    mlonlist=mlons.flatten()
    thetat = np.deg2rad(90-mlatlist)
    phit = np.deg2rad(mlonlist)
    [glatlist, glonlist] = gemini3d.coord.geomag2geog(thetat, phit)
    fac = loaded_model.FAC(glonlist, glatlist)
    fac = fac.reshape(mlons.shape)
    #fac = fac_input(times, mlons, mlats, centerlon=centerlon, sigmat=5, width=width, scaling=5, duration=5) # [A/m2]
    facscaled=fac/fac.max()    # scaling for discrete part of precipitation
    
    
    Q_direc = '\path\to\outputs\from\Alexs\tool'
    
    Q=np.empty((lt,_mlons.size,_mlats.size))
    for it in range(0,_times.size):
        Q[it,:,:] = facscaled[it,:,:].transpose((1,0))*Qpeak
        
    Q[Q < Qbackground] = Qbackground
        
    # Auroral oval slowly varying precipitation
    Qoval=5
    for it in range(0,_times.size):
        Q[it,:,:]=Q[it,:,:]+Qoval*np.exp(-(mlats[0,:,:].transpose((1,0))-70.0)**2/2/(4)**2)

    # if "mlon_sigma" in pg.attrs and "mlat_sigma" in pg.attrs:
    #     Q = (
    #         Qpeak
    #         * np.exp(
    #             -((pg.mlon.data[:, None] - mlon_mean) ** 2) / (2 * pg.mlon_sigma**2)
    #         )
    #         * np.exp(
    #             -((pg.mlat.data[None, :] - mlat_mean) ** 2) / (2 * pg.mlat_sigma**2)
    #         )
    #     )
    # elif "mlon_sigma" in pg.attrs:
    #     Q = Qpeak * np.exp(
    #         -((pg.mlon.data[:, None] - mlon_mean) ** 2) / (2 * pg.mlon_sigma**2)
    #     )
    # elif "mlat_sigma" in pg.attrs:
    #     Q = Qpeak * np.exp(
    #         -((pg.mlat.data[None, :] - mlat_mean) ** 2) / (2 * pg.mlat_sigma**2)
    #     )
    # else:
    #     raise LookupError("precipation must be defined in latitude, longitude or both")
        
    return Q