import xarray
import numpy as np
from lompe.utils.save_load_utils import load_model
import gemini3d
import gemini3d.coord
import os
import re

def lompe_fac(E: xarray.Dataset, gridflag: int, flagdip: bool) -> xarray.Dataset:
    """
    for 3D sim, FAC up/down 0.5 degree FWHM
    """
    
    fac_direc = '/Users/clevenger/Projects/paper01/events/20230227/lompe/outputs/cases/17/'
    
    fn_convention = r'(\d{4}-\d{2}-\d{2})_(\d{6})\.nc'

    # Collect and sort reconstruction files
    grouped_files = [fn for fn in os.listdir(fac_direc) if re.match(fn_convention, fn)]
    grouped_files.sort()

    for t_idx, (file_name, time_step) in enumerate(zip(grouped_files, E.time)):
        file_path = os.path.join(fac_direc, file_name)
        print(f"Processing time step {t_idx+1}/{len(grouped_files)}: {file_name}")

        # Load the corresponding model
        loaded_model = load_model(file_path, time='first')

        if E.mlon.size == 1 or E.mlat.size == 1:
            raise ValueError("E.mlon and E.mlat must have size > 1 for 3D simulations.")

        # Evaluation locations
        _mlats = E.mlat
        _mlons = E.mlon
        mlats, mlons = np.meshgrid(_mlats, _mlons, indexing='ij')
        mlatlist = mlats.flatten()
        mlonlist = mlons.flatten()
        thetat = np.deg2rad(90 - mlatlist)
        phit = np.deg2rad(mlonlist)
        glatlist, glonlist = gemini3d.coord.geomag2geog(thetat, phit)

        # Calculate FAC
        fac = loaded_model.FAC(glonlist, glatlist).reshape(mlons.shape)
        fac[np.isnan(fac)] = 0

        # Assign FAC to the dataset
        E["flagdirich"].loc[time_step] = 0
        k = "Vminx1it" if gridflag == 1 else "Vmaxx1it"
        E[k].loc[time_step] = fac.transpose((1, 0))  # GEMINI expects (mlon, mlat) ordering

        print(f"Completed FAC processing for time step: {time_step.values}")

    return E
