#=======================================================================
# Sample Python code to write Data Exchange Format
#
# Date: 2013-04-21
# 
#=======================================================================

import h5py
import numpy as np

def write_example(filename):

    # --- prepare data ---

    # Generate fake raw data
    rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
    rawdata_white = np.ones(2 * 256 * 256, np.uint16).reshape(2, 256, 256)
    rawdata_dark = np.zeros(10 * 256 * 256, np.uint16).reshape(10, 256, 256)

    # Generate fake normalized data
    normalizeddata = np.ones(180 * 256 * 256, \
                             np.float64).reshape(180, 256, 256)

    # Generate fake reconstructed data
    reconstructeddata = np.ones(256 * 256 * 256, \
                                np.float64).reshape(256, 256, 256)
     
    # x, y and z ranges
    x = np.arange(128)
    y = np.arange(128)
    z = np.arange(180);
    
    # Fabricated theta values
    theta = (z / float(180)) * 180.0
    theta_white = (0.0, 180.0)
    theta_dark = (0.0, 0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0, 180.0, 180.0)

    # Fabricated data_shift_x and data_shift_y value
    data_shift_x = np.random.randint(-100, 100, size=180) 
    data_shift_y = np.random.randint(-100, 100, size=180) 

    # --- create file ---

    # Open HDF5 file
    f = h5py.File(filename, 'w')
        
    # Create basic definitions in root
    ds = f.create_dataset('implements', \
                    data = "exchange:exchange_2:exchange_3:measurement")
      
    # --- exchange definition --- 
    
    # Exchange HDF5 group
    # /exchange
    exchangeGrp = f.create_group("exchange")
    
    # Create core HDF5 dataset in exchange group for 180 deep stack
    # of x,y images /exchange/data
    ds = exchangeGrp.create_dataset('data', data = rawdata, \
                                    compression='gzip', compression_opts=4)
 
    ds.attrs['description'] = "transmission"
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta:y:x"
    ds1 = exchangeGrp.create_dataset('title', \
                                     data = "tomography raw projections")
    
    # Create HDF5 dataset in exchange group for dark data
    # /exchange/data_dark
    ds = exchangeGrp.create_dataset('data_dark', \
                                    data = rawdata_dark, \
                                    compression='gzip', compression_opts=4)
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta_dark:y:x"

    # Create HDF5 dataset in exchange group for white data
    # /exchange/data_white
    ds = exchangeGrp.create_dataset('data_white', \
                                    data = rawdata_white, \
                                    compression='gzip', compression_opts=4)
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta_white:y:x"
    
    # Create HDF5 dataset in exchange group for theta
    # /exchange/theta
    ds = exchangeGrp.create_dataset('theta', data = theta)
    ds.attrs['units'] = "degrees"

    # Create HDF5 dataset in exchange group for theta_dark
    # /exchange/theta_dark
    ds = exchangeGrp.create_dataset('theta_dark', data = theta_dark)
    ds.attrs['units'] = "degrees"

    # Create HDF5 dataset in exchange group for theta_white
    # /exchange/theta_white
    ds = exchangeGrp.create_dataset('theta_white', data = theta_white)
    ds.attrs['units'] = "degrees"

    # Create HDF5 dataset in exchange group for data_shift_x and data_shift_y
    # /exchange/data_shift_x
    # /exchange/data_shift_y
    ds = exchangeGrp.create_dataset('data_shift_x', data = data_shift_x)
    ds = exchangeGrp.create_dataset('data_shift_y', data = data_shift_y)

                  
    # Exchange HDF5 group
    # /exchange_2
    # this will be the out_put of the normalization process
    exchange2Grp = f.create_group("exchange_2")
    ds2 = exchange2Grp.create_dataset('title', \
                            data = "tomography normalized projections")
    
    # Create core HDF5 dataset in exchange group for 180 deep stack
    # of x,y images /exchange_2/data
    ds = exchange2Grp.create_dataset('data', data = normalizeddata, \
                                     compression='gzip', \
                                     compression_opts=4)
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta:y:x"
    # Create HDF5 dataset in exchange_2 group for theta
    # /exchange_2/theta
    ds = exchange2Grp.create_dataset('theta', data = theta)
    ds.attrs['units'] = "degrees"

    # Exchange HDF5 group
    # /exchange_3
    # this will be the out_put of the reconstruction process
    exchange3Grp = f.create_group("exchange_3")
    ds3 = exchange3Grp.create_dataset('title', \
                                      data = "tomography reconstructions")
    
    # Create core HDF5 dataset in exchange group for 180 deep stack of x,y
    # images /exchange_3/data
    ds = exchange3Grp.create_dataset('data', \
                                     data = reconstructeddata, \
                                     compression='gzip', \
                                     compression_opts=4)
    ds.attrs['units'] = "density"
    ds.attrs['axes'] = "z:y:x"

    # Create HDF5 group measurement
    # /measuremen
    measurementGrp = f.create_group("measurement")

    # Create HDF5 subgroup 
    # /measurement/instrument
    instrumentGrp = measurementGrp.create_group("instrument")

    # Create HDF5 subgroup
    # /measurement/instrument/source
    sourceGrp = instrumentGrp.create_group("source")
    sods1 = sourceGrp.create_dataset('name', data = "APS")
    sods2 = sourceGrp.create_dataset('date_time', data = "2012-07-31T21:15:23+0600")

    sods3 = sourceGrp.create_dataset('beamline', data = "2-BM")
    sods4 = sourceGrp.create_dataset('current', data = 101.199, dtype='d')
    sods4.attrs['units'] = "mA"
    sods5 = sourceGrp.create_dataset('energy', data = 7.0, dtype='d')
    sods5.attrs['units'] = "GeV"
    sods6 = sourceGrp.create_dataset('mode', data = "TOPUP")

    # Create HDF5 subgroup
    # /measurement/instrument/attenuator
    attenuatorGrp = instrumentGrp.create_group("attenuator")
    ats1 = attenuatorGrp.create_dataset('thickness', data = 1e-3, \
                                        dtype='d')
    ats2 = attenuatorGrp.create_dataset('type', data = "Al")

    # Create HDF5 subgroup
    # /measurement/instrument/monochromator
    monochromatorGrp = instrumentGrp.create_group("monochromator")
    mds1 = monochromatorGrp.create_dataset('type', data = "Multilayer")
    mds2 = monochromatorGrp.create_dataset('energy', data = 19.26, \
                                           dtype='d')
    mds2.attrs['units'] = "keV"
    mds3 = monochromatorGrp.create_dataset('energy_error', data = 1e-3, \
                                           dtype='d')
    mds3.attrs['units'] = "keV"
    mds4 = monochromatorGrp.create_dataset('mono_stripe', data = "Ru/C")                                                                                                                                                                                                                                                                                                                                                                                                            

    # Create HDF5 subgroup
    # /measurement/instrument/detector
    detectorGrp = instrumentGrp.create_group("detector")

    # define the detector subgroup members of instrument
    dds1 = detectorGrp.create_dataset('manufacturer', \
                                      data = "CooKe Corporation")
    dds2 = detectorGrp.create_dataset('model', data = "pco dimax")
    dds3 = detectorGrp.create_dataset('serial_number', data = "1234XW2")
    dds4 = detectorGrp.create_dataset('bit_depth', data = 12, dtype='i')

    # for x_pixel_size and y_pixel_size if the attributes units is not
    # specified then these are in meters
    dds5 = detectorGrp.create_dataset('x_pixel_size', data = 6.7e-6, \
                                      dtype='f')
    dds6 = detectorGrp.create_dataset('y_pixel_size', data = 6.7e-6, \
                                      dtype='f')
    dds7 = detectorGrp.create_dataset('x_dimentions', data = 2048, \
                                      dtype='i')
    dds8 = detectorGrp.create_dataset('y_dimentions', data = 2048, \
                                      dtype='i')
    dds9 = detectorGrp.create_dataset('x_binning', data = 1, dtype='i')
    dds10 = detectorGrp.create_dataset('y_binning', data = 1, dtype='i')

    # for operating_temperature if the attributes units is not
    # specified then this is in K
    dds11 = detectorGrp.create_dataset('operating_temperature', \
                                       data = 270, dtype='f')

    # for exposure_time the attributes units is specified as ms
    dds12 = detectorGrp.create_dataset('exposure_time', data = 170, \
                                       dtype='d')
    dds12.attrs['units'] = "ms"
    
    dds13 = detectorGrp.create_dataset('frame_rate', data = 3, dtype='i')
    dds14 = detectorGrp.create_dataset('output_data', data = "/exchange")

    roiGrp = detectorGrp.create_group("roi")
    rds1 = roiGrp.create_dataset('name', data = "center third")
    rds2 = roiGrp.create_dataset('x1', data = 256, dtype='i')
    rds3 = roiGrp.create_dataset('y1', data = 256, dtype='i')
    rds4 = roiGrp.create_dataset('x2', data = 1792, dtype='i')
    rds5 = roiGrp.create_dataset('y2', data = 1792, dtype='i')
    
    objectiveGrp = detectorGrp.create_group("objective")
    ods1 = objectiveGrp.create_dataset('manufacturer', data = "Zeiss")
    ods2 = objectiveGrp.create_dataset('model', \
                                       data = "Plan-NEOFLUAR 1004-072")
    ods3 = objectiveGrp.create_dataset('magnification', \
                                       data = 20, dtype='d')
    ods4 = objectiveGrp.create_dataset('numerical_aperture', \
                                       data = 0.5, dtype='d')


    scintillatorGrp = detectorGrp.create_group("scintillator")
    sds1 = scintillatorGrp.create_dataset('manufacturer', data = "Crytur")
    sds2 = scintillatorGrp.create_dataset('serial_number', data = "12")
    sds3 = scintillatorGrp.create_dataset('name', data = "YAG polished")
    sds4 = scintillatorGrp.create_dataset('type', data = "YAG on YAG")
    sds5 = scintillatorGrp.create_dataset('scintillating_thickness', \
                                          data = 5e-6, dtype='d')
    sds6 = scintillatorGrp.create_dataset('substrate_thickness', \
                                          data = 1e-4, dtype='d')


    # Create HDF5 subgroup 
    # /measurement/sample
    sampleGrp = measurementGrp.create_group("sample")
    sads1 = sampleGrp.create_dataset('name', data = "Hornby_b")
    sads2 = sampleGrp.create_dataset('description', data = "test sample")
    sads3 = sampleGrp.create_dataset('preparation_date', \
                                     data = "2011-07-31T21:15:23+0600")
    sads4 = sampleGrp.create_dataset('chemical_formula', data = "unknown")
    sads5 = sampleGrp.create_dataset('mass', data = 0.25, dtype='d')
    sads5.attrs['units'] = "g"
    sads7 = sampleGrp.create_dataset('enviroment', data = "air")
    sads8 = sampleGrp.create_dataset('temperature', data = 120.0, \
                                     dtype='d')
    sads8.attrs['units'] = "Celsius"
    sads9 = sampleGrp.create_dataset('temperature_set', data = 130.0, \
                                     dtype='d')
    sads9.attrs['units'] = "Celsius"

    # Create HDF5 subgroup 
    # /measurement/sample/geometry
    geometryGrp = sampleGrp.create_group("geometry")

    # Create HDF5 subgroup 
    # /measurement/sample/geometry/translation
    translationGrp = geometryGrp.create_group("translation")
    trds1 = translationGrp.create_dataset('distances', \
                                          data = [0, 0, 0], dtype='d')
    trds1.attrs['axes'] = "z:y:x"
    trds1.attrs['units'] = "m"
    
    # Create HDF5 subgroup
    # /measurement/sample/experimenter
    experimenterGrp = sampleGrp.create_group("experimenter")
    exrds1 = experimenterGrp.create_dataset('name', data = "John Doe")
    exrds2 = experimenterGrp.create_dataset('role', data = "Project PI")
    exrds3 = experimenterGrp.create_dataset('affiliation', \
                        data = "University of California, Berkeley")
    exrds4 = experimenterGrp.create_dataset('address', \
                        data = "EPS UC Berkeley CA 94720 4767 USA")
    exrds5 = experimenterGrp.create_dataset('phone', \
                        data = "+1 123 456 0000")
    exrds6 = experimenterGrp.create_dataset('e-mail', \
                        data = "johndoe@berkeley.edu")
    exrds7 = experimenterGrp.create_dataset('facility_user_id', \
                        data = "a123456")

    # Create HDF5 subgroup
    # /measurement/sample/experiment
    experimentGrp = sampleGrp.create_group("experiment")
    exds1 = experimentGrp.create_dataset('proposal', data = "1234")
    exds2 = experimentGrp.create_dataset('activity', data = "e11218")
    exds3 = experimentGrp.create_dataset('safety', data = "9876")

    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('/tmp/python/DataExchange-example5.h5')
#=======================================================================
#
#=======================================================================
