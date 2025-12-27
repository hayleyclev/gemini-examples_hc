import h5py
import xarray as xr
import numpy as np
import os
import re

def asi_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):
    """
    Purpose:
        - read in h5 files that are output from the asispectralinversion process
        - populate Q and E0 arrays to create precip inputs for GEMINI
    
    Parameters:
        - pg: xr.Dataset - Dataset to populate with Q and E0

    Returns:
        - Q: np.ndarray - Q array
        - E0: np.ndarray - E0 array
    """
    
    # user input (only need the path to the asispectralinversion outputs)
    asi_direc = '/Users/clevenger/Projects/paper01/events/20230227/gemini_inputs/asi/'
    
    # the timing info is in the name of each file, so need to establish file naming convention
    fn_convention = r'(\d{8})_(\d{6})\.h5'  # files are in YYYYMMDD_HHMMSS.h5 format
    grouped_files = [] # empty array of directory of files

    # pull each file from directory
    for fn in os.listdir(asi_direc):
        if re.match(fn_convention, fn):
            grouped_files.append(fn)

    # sort files by timestamp (earliest to latest)
    grouped_files.sort()
    num_files = len(grouped_files)

    # initialize Q and E0 arrays
    Q = np.zeros(pg["Q"].shape)
    E0 = np.zeros(pg["E0"].shape)

    # read data from each file and populate Q and E0
    for i, file_name in enumerate(grouped_files):
        file_path = os.path.join(asi_direc, file_name)

        with h5py.File(file_path, "r") as h5:
            Q_temp = h5['Q'][:]
            E0_temp = h5['E0'][:]
        
        # replace NaNs with 0
        Q_temp[np.isnan(Q_temp)] = 0
        E0_temp[np.isnan(E0_temp)] = 0
        
        # ensure E0 values meet minimum threshold eV
        E0_temp[E0_temp < 1000] = 1000
        
        # populate the arrays for the corresponding time index
        Q[i, :, :] = Q_temp
        E0[i, :, :] = E0_temp

    print(f"Q shape: {Q.shape}")
    print(f"E0 shape: {E0.shape}")
    
    return Q, E0
