#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:51:03 2024

@author: clevenger
"""

import numpy as np
import xarray as xr

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):
    
    # Load the Q and E0 data from the output file
    data = xr.open_dataset("/Users/clevenger/Projects/asi_inversion/asispectralinversion/src/asispectralinversion/output_Q_E0_SigP_SigH.nc")

    # Extract Q and E0 values
    Q = data["Q"].values
    Q[Q < Qbackground] = Qbackground
    
    SigP = data["SigP"].values
    SigH = data["SigH"].values
    
    # Add contribution from characteristic energy and conductances
    Q += Q * (SigH / SigP)
    
    print("Shape of Q:", Q.shape)
    
    # Define latitude values
    latitudes = np.linspace(-90, 90, Q.shape[1])  # Assuming latitude varies along the second dimension of Q
    
    # Auroral oval slowly varying precipitation
    Qoval = 5
    for it in range(Q.shape[0]):
        Q[it, :] = Q[it, :] + Qoval * np.exp(-((latitudes - 70.0) ** 2) / (2 * (4) ** 2))

    return Q






