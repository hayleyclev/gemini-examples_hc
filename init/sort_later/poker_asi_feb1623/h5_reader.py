#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:43:40 2024

@author: clevenger
"""

import h5py

# Replace 'your_output_file.h5' with the actual file path
with h5py.File('/Users/clevenger/Desktop/dasc_test/20230216_100010.h5', 'r') as hdf:
    print("Q data:", hdf['Q'][:])
    print("E0 data:", hdf['E0'][:])
