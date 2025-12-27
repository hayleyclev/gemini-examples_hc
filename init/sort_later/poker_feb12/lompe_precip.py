#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:51:03 2024

@author: clevenger
"""

import numpy as np
import xarray as xr

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float, SigP: np.ndarray, SigH: np.ndarray):
    
    # Load the Q and E0 data from the output file
    data = xr.open_dataset("/Users/clevenger/Projects/asi_inversion/asispectralinversion/src/asispectralinversion/output_Q_E0.nc")

    # Extract Q and E0 values
    Q = data["Q"].values
    
    Q[Q < Qbackground] = Qbackground

    # Add contribution from characteristic energy and conductances
    Q += Q * (SigH / SigP)

    # Auroral oval slowly varying precipitation
    Qoval = 5
    for it in range(0, Q.shape[0]):
        Q[it, :, :] = Q[it, :, :] + Qoval * np.exp(-(pg.latitude.values - 70.0) ** 2 / 2 / (4) ** 2)

    return Q
