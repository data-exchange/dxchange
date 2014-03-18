"""
.. module:: convert_APS_13BM.py
   :platform: Unix
   :synopsis: Convert APS 13-BM SPE files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import xtomo.xtomo_importer as dx

def main():

    file_name = '/local/dataraid/databank/APS_13_BM/SPE/run2_soln1_2_.SPE'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/APS_13_BM_SPE.h5'

    white_start = 1
    white_end = 8
    white_step = 2
    projections_start = 2
    projections_end = 7
    projections_step = 2

    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            #hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            projections_step = projections_step,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            projections_zeros=False,
                            white_zeros=False,
                            dark_zeros=False,
                            data_type='spe',
                            sample_name = 'Stripe_Solder_Sample_Tip1',
                            log='INFO'
                            )
    
if __name__ == "__main__":
    main()

