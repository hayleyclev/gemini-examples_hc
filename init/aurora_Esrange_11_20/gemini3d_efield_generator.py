#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:41:24 2024

@author: clevenger
"""

import gemini3d.model
import matplotlib.pyplot as plt
from fac_SCW import fac_SCW



gemini3d.model.setup('./config.nml', '/Users/clevenger/Simulations/aurora_Esrange_11_20')

for t in range (0,E.time.size):
    plt.pcolormesh(fac[t,:,:])