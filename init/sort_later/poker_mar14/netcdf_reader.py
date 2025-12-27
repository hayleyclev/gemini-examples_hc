#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 16:23:14 2024

@author: clevenger
"""

from matplotlib import pyplot as plt
import pandas as pd
import netCDF4

nc_fn='/Users/clevenger/Projects/asi_inversion/asispectralinversion/src/asispectralinversion/output_Q_E0.nc'

nc = netCDF4.Dataset(nc_fn)

plt.imshow(nc['Q'][0])
plt.show()

plt.imshow(nc['E0'][0])
plt.show()

#plt.imshow(nc['SigP'][:,:,:])
#plt.show()

#plt.imshow(nc['SigH'][:,:,:])
#plt.show()

