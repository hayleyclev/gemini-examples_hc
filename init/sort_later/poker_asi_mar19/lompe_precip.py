import h5py
import xarray as xr
import numpy as np

def lompe_precip(pg: xr.Dataset, Qpeak: float, Qbackground: float):

    asifn = '/Users/clevenger/Projects/asi_inversion/hc_fork/asi_inversion_outputs/single_frame/mar_19/gemini_Q_E0_mlat_mlon.h5'

    with h5py.File(asifn,"r") as h5:
        #lat = h5['gemini_mag_lat'][:]
        #lon = h5['gemini_mag_lon'][:]
        #MLATi = h5['MLATi'][:]
        #MLONi = h5['MLONi'][:]
        Q_temp = h5['Q'][:]
        E0_temp = h5['E0'][:]
        
        
    Q = np.zeros(pg["Q"].shape)
    E0 = np.zeros(pg["E0"].shape)
    
    Q_temp[np.isnan(Q_temp)] = 0
    E0_temp[np.isnan(E0_temp)] = 0
    
    E0_temp[E0_temp<1000]=1000
        
    for i in range(pg["Q"].shape[0]):
        Q[i, :, :] = Q_temp
        E0[i, :, :] = E0_temp

    return Q, E0
