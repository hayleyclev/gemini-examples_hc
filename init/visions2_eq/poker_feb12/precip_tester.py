#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:45:16 2024

@author: clevenger
"""

from 

# Load the Q and E0 data from the output file
data = xr.open_dataset("output_Q_E0.nc")

# Extract Q and E0 values
Q = data["Q"].values
E0 = data["E0"].values

# Assuming you have the SigP and SigH arrays available, you can call the precipitation function
precipitation = precip_SCW(data, Qpeak=10, Qbackground=0.1, SigP=SigP, SigH=SigH)