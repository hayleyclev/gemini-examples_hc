#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:06:32 2024

@author: clevenger
"""

import numpy as np
import h5py
import xarray as xr

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):

    asifn = '/Users/clevenger/Projects/asi_inversion/hc_fork/asi_inversion_outputs/single_frame/gemini_Q_E0.h5'

    with h5py.File(asifn,"r") as h5:
        #lat = h5['gemini_mag_lat'][:]
        #lon = h5['gemini_mag_lon'][:]
        #MLATi = h5['MLATi'][:]
        #MLONi = h5['MLONi'][:]
        Q_temp = h5['Q_gridded'][:]
        E0_temp = h5['E0_gridded'][:]
        
    for i in range(pg["Q"].shape[0]):
        pg["Q"][i, :, :] = Q_temp
        pg["E0"][i, :, :] = E0_temp
    
        
    
    # Load the Q and E0 data from the output file

    
    # make dt object for each frame from file - aka ascribe a time to each frame
    
    # add overarching time loop to complete process below for each frame
    
    # read in E0 instead of trying to solve
    
    #if isfield(p, "Qprecip_function")
    #Qfunc = str2func(p.Qprecip_function);
    #else
    #Qfunc = str2func("gemini3d.particles.gaussian2d");
    #end

    #if isfield(p, "E0precip_function")
    #Efunc = str2func(p.E0precip_function);
    #end

    #for i = i_on:i_off
    #precip.Qit(:,:,i) = Qfunc(precip,p.Qprecip,p.Qprecip_background);
    #% precip.E0it(:,:,i) = p.E0precip;
    #precip.E0it(:,:,i) = Efunc(precip,p.E0precip,p.E0precip_background);
    #end

    # Extract Q and E0 values
    #Q = data["Q"].values
    #Q[Q < Qbackground] = Qbackground
    
    #E0 = data["E0"].values
    
    #SigP = data["SigP"].values
    #SigH = data["SigH"].values
    
    # Add contribution from characteristic energy and conductances
    #Q += Q * (SigH / SigP)
    
    #print("Shape of Q:", Q.shape)
    
    # Define latitude values
    #latitudes = np.linspace(-90, 90, Q.shape[1])  # Assuming latitude varies along the second dimension of Q
    
    # Auroral oval slowly varying precipitation
    #Qoval = 5
    #for it in range(Q.shape[0]):
        #Q[it, :] = Q[it, :] + Qoval * np.exp(-((latitudes - 70.0) ** 2) / (2 * (4) ** 2))

    return pg["Q"], pg["E0"]