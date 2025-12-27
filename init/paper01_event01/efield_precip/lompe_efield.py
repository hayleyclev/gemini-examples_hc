from __future__ import annotations
import numpy as np
import xarray as xr
from lompe.utils.save_load_utils import load_model
import gemini3d
import gemini3d.coord

def lompe_efield(
    E: xr.Dataset,
    xg,
    lx1,
    lx2,
    lx3,
    gridflag: int,
    flagdip: bool,
) -> xr.Dataset:
    """
    Apply Lompe electric field to GEMINI boundary conditions.
    """

    efield_fn = (
        "/Users/clevenger/Projects/paper01/events/20230227/"
        "lompe/outputs/cases/17/2023-02-27_083500.nc"
    )

    # Load Lompe outputs
    loaded_model = load_model(efield_fn, time="first")

    if E.mlon.size == 1 or E.mlat.size == 1:
        raise ValueError("lompe_efield2 only valid for 3D GEMINI simulations")

    # set up gridding for GEMINI
    mlats = E.mlat.values
    mlons = E.mlon.values
    MLAT, MLON = np.meshgrid(mlats, mlons, indexing="ij")
    mlatlist = MLAT.flatten()
    mlonlist = MLON.flatten()
    thetat = np.deg2rad(90.0 - mlatlist)
    phit = np.deg2rad(mlonlist)
    glatlist, glonlist = gemini3d.coord.geomag2geog(thetat, phit)
    E_E, E_N = loaded_model.E(glonlist, glatlist)

    # Reshape to GEMINI grid
    E_E = E_E.reshape(MLON.shape)
    print("efield E shape: ", E_E.shape)
    E_N = E_N.reshape(MLON.shape)
    print("efield N shape: ", E_N.shape)
    E_E[np.isnan(E_E)] = 0.0
    E_N[np.isnan(E_N)] = 0.0

    for t in range(E.time.size):
        E["flagdirich"].loc[E.time[0]] = 0
        # k = "Vminx1it" if gridflag == 1 else "Vmaxx1it"
        # E[k].loc[E.time[t]] = Phi.T
        E["Exit"][t, :, :] = E_E.T
        E["Eyit"][t, :, :] = E_N.T

    return E
