import h5py
import xarray as xr
import numpy as np
import os
import re

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):
    """
    Read multiple HDF5 files containing precipitation data and populate the
    Q and E0 arrays in the provided xarray Dataset.
    
    Parameters:
        pg: xr.Dataset - Dataset to populate with Q and E0.
        asi_direc: str - Directory containing the HDF5 files.

    Returns:
        Q: np.ndarray - The populated Q array.
        E0: np.ndarray - The populated E0 array.
    """
    asi_direc = '/Users/clevenger/Desktop/dasc_test/'
    # List of files in the data directory that match the expected naming pattern
    fn_convention = r'(\d{8})_(\d{6})\.h5'  # Adjust regex based on your file naming pattern
    grouped_files = []

    for fn in os.listdir(asi_direc):
        if re.match(fn_convention, fn):
            grouped_files.append(fn)

    # Sort files by timestamp (assuming they are in the format YYYYMMDD_HHMMSS)
    grouped_files.sort()

    num_files = len(grouped_files)
    print(f"Found {num_files} files matching the pattern.")

    # Initialize Q and E0 arrays with the shape of the time dimension from pg
    Q = np.zeros((num_files, pg["Q"].shape[1], pg["Q"].shape[2]))
    E0 = np.zeros((num_files, pg["E0"].shape[1], pg["E0"].shape[2]))

    # Read data from each file and populate Q and E0
    for i, file_name in enumerate(grouped_files):
        file_path = os.path.join(asi_direc, file_name)

        with h5py.File(file_path, "r") as h5:
            Q_temp = h5['Q'][:]
            E0_temp = h5['E0'][:]
        
        # Replace NaNs with 0
        Q_temp[np.isnan(Q_temp)] = 0
        E0_temp[np.isnan(E0_temp)] = 0
        
        # Ensure E0 values meet a minimum threshold
        E0_temp[E0_temp < 1000] = 1000
        
        # Populate the arrays for the corresponding time index
        Q[i, :, :] = Q_temp
        E0[i, :, :] = E0_temp

    print(f"Final Q shape: {Q.shape}")
    print(f"Final E0 shape: {E0.shape}")
    
    return Q, E0
