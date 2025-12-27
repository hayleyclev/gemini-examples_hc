import h5py
import xarray as xr
import numpy as np

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):
    
    asi_direc = '/Users/clevenger/Desktop/dasc_test/'
    
    fn_convention = r'grouped_\d+geodetic_Q_E0\.h5'
    asi_fn_list = []

    for file_name in os.listdir(asi_direc):
        if re.match(fn_convention, file_name):
            asi_fn_list.append(os.path.join(asi_direc, file_name))

    # Initialize Q and E0 arrays based on the number of files and pg dimensions
    no_files = len(asi_fn_list)
    Q_shape = pg["Q"].shape  # Assuming pg["Q"].shape is (time, lat, lon)
    Q = np.zeros((no_files, *Q_shape[1:]))
    E0 = np.zeros((no_files, *Q_shape[1:]))

    # Loop through each file to read Q and E0 data
    for i, asi_fn in enumerate(asi_fn_list):
        with h5py.File(asi_fn, "r") as h5:
            Q_temp = h5['Q'][:]
            E0_temp = h5['E0'][:]
        
        # Handle NaN values and set minimum threshold for E0
        Q_temp[np.isnan(Q_temp)] = 0
        E0_temp[np.isnan(E0_temp)] = 0
        E0_temp[E0_temp < 1000] = 1000
        
        # Fill the Q and E0 arrays for the current time slice
        Q[i, :, :] = Q_temp
        E0[i, :, :] = E0_temp

    return Q, E0
