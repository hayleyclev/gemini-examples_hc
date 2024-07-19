#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:45:56 2024

@author: clevenger
"""

import numpy as np
import xarray as xr
from fac_input_to_matt import fac_input
from lompe.utils.save_load_utils import load_model
import gemini3d
import gemini3d.coord

def precip_SCW(pg: xr.Dataset, Qpeak: float, Qbackground: float, SigP: np.ndarray, SigH: np.ndarray):
    
    reconstruction_fn = '/Users/clevenger/Projects/data_assimilation/feb_12/lompe_outputs/509_runs/pfisr_supermag/large/nc_files/2023-02-12_121000.nc'
    loaded_model = load_model(reconstruction_fn, time='first')
    
    # Load the Q and E0 data from the output file
    data = xr.open_dataset("output_Q_E0.nc")

    # Extract Q and E0 values
    Q = data["Q"].values
    E0 = data["E0"].values
    
    mlon_mean = pg.longitude.mean().item()
    mlat_mean = pg.latitude.mean().item()

    # Set some parameters
    centerlon = 105  # the longitudinal center (in degrees) of SCW structure
    width = 90  # longitudinal width in degrees of SCW feature

    # Make evaluation locations
    lt = pg.time.size
    timeref = pg.time[0]
    timesec = np.empty(lt)
    for it in range(0, lt):
        dt = pg.time[it].values - timeref.values
        timesec[it] = dt.astype('timedelta64[s]').item().total_seconds()
    _times = timesec / 60  # temporal locations to evaluate for FAC [minutes]
    _mlats = pg.latitude
    _mlons = pg.longitude

    # Discrete auroral precipitation
    mlats, mlons = np.meshgrid(_times, _mlats, _mlons, indexing='ij')  # make 3D grid of locations
    #fac = fac_input(times, mlons, mlats, centerlon=centerlon, sigmat=5, width=width, scaling=5, duration=5)  # [A/m2]
    mlatlist=mlats.flatten()
    mlonlist=mlons.flatten()
    thetat = np.deg2rad(90-mlatlist)
    phit = np.deg2rad(mlonlist)
    [glatlist, glonlist] = gemini3d.coord.geomag2geog(thetat, phit)
    fac = loaded_model.FAC(glonlist, glatlist)
    facscaled = fac / fac.max()  # scaling for discrete part of precipitation
    Q = np.empty((lt, _mlons.size, _mlats.size))
    for it in range(0, _times.size):
        Q[it, :, :] = facscaled[it, :, :].transpose((1, 0)) * Qpeak

    Q[Q < Qbackground] = Qbackground

    # Add contribution from characteristic energy and conductances
    Q += Q * (SigH / SigP)

    # Auroral oval slowly varying precipitation
    Qoval = 5
    for it in range(0, _times.size):
        Q[it, :, :] = Q[it, :, :] + Qoval * np.exp(-(mlats[0, :, :].transpose((1, 0)) - 70.0) ** 2 / 2 / (4) ** 2)

    return Q



