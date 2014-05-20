#!/usr/bin/env python

import numpy as np
import h5py
import time
import os
import sys
import re

## Federica: se data_exchange e` nella tua working directory cambia:
from dataexchange.xtomo.data_exchange import DataExchangeFile, DataExchangeEntry
## in
##from data_exchange import DataExchangeFile, DataExchangeEntry

#import wx
#from tifffile import tifffile

# --------------------------------- Functions --------------------------------------#
def show_help():
        print "USAGE"
        print "Input parameters"
        print "   $0  = tifdir"
        print "   tif2h5.py <tifdir>"
        print ""
        print ""
        print "   ARGUMENTS"
        print "     tifdir       Directory with original projections"
        print ""
        print ""
        print "EXAMPLE"
        print "   tif2h5.py /sls/X02DA/data/e11218/Data1/choco/tif "
        print ""
        print ""
        sys.exit(0)

# -------------------------------- Main ----------------------------------#
def main():
##path_arg_at=0
##if len(sys.argv) != 2 or sys.argv[1]=='-h':
##        show_help()
##        sys.exit(1)
##else:
##        path_arg_at=1
##
##if path_arg_at>0:

        # tifdir
##        tifdir = sys.argv[path_arg_at+0]
        # Set logdir and samplename
##        os.chdir(tifdir)
##        tifdir = os.getcwd()
##        os.chdir(os.pardir)
##        basename = os.getcwd()
##        samplename = os.path.basename(basename)
##        imageFileFullPath = basename + "/" + samplename + ".h5"

        imageFileFullPath = "/Users/decarlo/Desktop/DPC/BG_API.h5"

        samplename = "sample_name"

        if os.path.exists(imageFileFullPath):
                print "File exists, exiting"
                sys.exit()

        # Open DataExchange file
        f = DataExchangeFile(imageFileFullPath, mode='a')

        f.add_entry( DataExchangeEntry.sample(name={'value': samplename}))
                                                    
        # Create HDF5 subgroup
        # /measurement/instrument/source
        f.add_entry( DataExchangeEntry.source(name={'value': 'SLS'},
                                              beamline={'value': "TOMCAT"},
                                              energy={'value': 11.1, 'units':'keV', 'dataset_opts': {'dtype': 'd'}}
                                              )
                     )

        grid_steps=1	
##
##        # Read info and userID from log file
##        os.chdir(tifdir)
##        filename0 = samplename + ".log"
##        filename1 = samplename + "0001.tif"
##        filename_image = os.path.join(tifdir,filename1)
##        filename = os.path.join(tifdir,filename0)
##        image = wx.Image(filename_image)
##        height = int(image.GetHeight())
##        width = int(image.GetWidth())

        filename = "/Users/decarlo/Desktop/DPC/BG_Fab-1_B1_.log"

        # used later to split strings into text and number 
        r = re.compile("([0-9]+)([a-zA-Z]+)")
        r1 = re.compile("([0-9]+)([%]+)")

        FILE = open(filename,"r")
        for line in FILE:
                linelist=line.split()
                if len(linelist)>1:

                        # Sample

                        if (linelist[0]=="User" and linelist[1]=="ID"):
                                f.add_entry( DataExchangeEntry.experiment(activity={'value':linelist[3]}))
 		   
                        # Beamline settings
		   	
                        elif (linelist[0]=="Ring" and linelist[1]=="current"):
                                f.add_entry( DataExchangeEntry.source(current={'value': float(linelist[4]), 'units':'mA', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Beam" and linelist[1]=="energy"):
                                f.add_entry( DataExchangeEntry.monochromator(energy={'value': float(linelist[4]), 'units':'keV', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Monostripe"):
                                f.add_entry(DataExchangeEntry.monochromator(type={'value': 'Multilayer'}, mono_stripe={'value': linelist[2]}))
                        elif (linelist[0]=="FE-Filter"):
                                m = r1.match(linelist[3])
                                f.add_entry( DataExchangeEntry.attenuator(entry_name="attenuator_1", thickness={'value':float(m.group(1)), 'units': m.group(2), 'dataset_opts':  {'dtype': 'd'}}, type={'value':linelist[2]}))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="1"):
                                m = r.match(linelist[3])
                                f.add_entry( DataExchangeEntry.attenuator(entry_name="attenuator_2", thickness={'value':float(m.group(1)), 'units': m.group(2), 'dataset_opts':  {'dtype': 'd'}}, type={'value':linelist[4]}))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="2"):
                                m = r.match(linelist[3])
                                f.add_entry( DataExchangeEntry.attenuator(entry_name="attenuator_3", thickness={'value':float(m.group(1)), 'units': m.group(2), 'dataset_opts':  {'dtype': 'd'}}, type={'value':linelist[4]}))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="3"):
                                m = r.match(linelist[3])
                                f.add_entry( DataExchangeEntry.attenuator(entry_name="attenuator_4", thickness={'value':float(m.group(1)), 'units': m.group(2), 'dataset_opts':  {'dtype': 'd'}}, type={'value':linelist[4]}))

                        # Detector settings
                        elif (linelist[0]=="Camera"):
                                f.add_entry( DataExchangeEntry.detector(model={'value': ' '.join(linelist[2:])}))
                        elif (linelist[0]=="Microscope"):
                                # I think this should go with the objective list (it is just another lens in the visible light path correct?)
                                f.add_entry(DataExchangeEntry.objective(entry_name="objective_1", model={'value': ' '.join(linelist[2:])}))
                        elif (linelist[0]=="Magnification"):
                                f.add_entry(DataExchangeEntry.objective(entry_name="objective_2",magnification={'value': float(linelist[2]), 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Scintillator"):
                                f.add_entry(DataExchangeEntry.scintillator(type={'value':linelist[2]}, scintillating_thickness={'value':float(linelist[3]), 'units':linelist[4], 'dataset_opts':{'dtype': 'd'}}))
                        elif (linelist[0]=="Exposure" and linelist[1]=="time"):
                                f.add_entry( DataExchangeEntry.detector(exposure_time={'value': float(linelist[4]), 'units':'ms', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Delay" and linelist[1]=="time"):
                                f.add_entry( DataExchangeEntry.detector(delay_time={'value': float(linelist[4]), 'units':'ms', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Stabilization" and linelist[1]=="time"):
                                f.add_entry( DataExchangeEntry.detector(stabilization_time={'value': float(linelist[4]), 'units':'ms', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Actual" and linelist[1]=="pixel"):
                                f.add_entry( DataExchangeEntry.detector(x_actual_pixel_size={'value': float(linelist[5]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                                f.add_entry( DataExchangeEntry.detector(y_actual_pixel_size={'value': float(linelist[5]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Millisecond"):
                                f.add_entry( DataExchangeEntry.shutter(name={'value': "Millisecond shutter"}, status={'value' : ' '.join(linelist[4:]) }))
                        elif (linelist[0]=="X-ROI"):
                                f.add_entry( DataExchangeEntry.roi(x1={'value':int(linelist[2]), 'dataset_opts': {'dtype': 'i'}}, x2={'value':int(linelist[4]), 'dataset_opts': {'dtype': 'i'}}))
                        elif (linelist[0]=="Y-ROI"):
                                f.add_entry( DataExchangeEntry.roi(y1={'value':int(linelist[2]), 'dataset_opts': {'dtype': 'i'}}, y2={'value':int(linelist[4]), 'dataset_opts': {'dtype': 'i'}}))
                        elif (linelist[0]=="X-coordinate"):
                                f.add_entry( DataExchangeEntry.setup(sample_x={'value': float(linelist[2]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Y-coordinate"):
                                f.add_entry( DataExchangeEntry.setup(sample_y={'value': float(linelist[2]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Z-coordinate"):
                                f.add_entry( DataExchangeEntry.setup(sample_z={'value': float(linelist[2]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="XX-coordinate"):
                                f.add_entry( DataExchangeEntry.setup(sample_xx={'value': float(linelist[2]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="ZZ-coordinate"):
                                f.add_entry( DataExchangeEntry.setup(sample_zz={'value': float(linelist[2]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))

                        # Scan settings
                           
                        elif (linelist[1]=="scan" and linelist[2]=="of"):
                                f.add_entry( DataExchangeEntry.acquisition(start_date={'value': (linelist[7] + " " + linelist[8] + " " + linelist[9] + " " + linelist[10] + " " + linelist[11])}))
                        elif (linelist[1]=="SCAN" and linelist[2]=="FINISHED"):
                                f.add_entry( DataExchangeEntry.acquisition(end_date={'value': (linelist[4] + " " + linelist[5] + " " + linelist[6] + " " + linelist[7] + " " + linelist[8])}))
                        elif (linelist[0]=="Number" and linelist[2]=="projections"):
                                nprj=int(linelist[4])
                                f.add_entry( DataExchangeEntry.acquisition(number_of_projections={'value': int(linelist[4]), 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Number" and linelist[2]=="darks"):
                                ndrk=int(linelist[4])
                                f.add_entry( DataExchangeEntry.acquisition(number_of_darks={'value': int(linelist[4]), 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Number" and linelist[2]=="flats"):
                                nflt=int(linelist[4])
                                f.add_entry( DataExchangeEntry.acquisition(number_of_flats={'value': int(linelist[4]), 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Sample" and linelist[1]=="In"):
                                f.add_entry( DataExchangeEntry.acquisition(sample_in={'value': float(linelist[4]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Sample" and linelist[1]=="Out"):
                                f.add_entry( DataExchangeEntry.acquisition(sample_out={'value': float(linelist[4]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Rot" and linelist[2]=="min"):
                                rotmin = float(linelist[6])
                                f.add_entry( DataExchangeEntry.acquisition(rotation_start_angle={'value': float(linelist[6]), 'units':'degree', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Rot" and linelist[2]=="max"):
                                rotmax = float(linelist[6])
                                f.add_entry( DataExchangeEntry.acquisition(rotation_end_angle={'value': float(linelist[6]), 'units':'degree', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Angular" and linelist[1]=="step"):
                                f.add_entry( DataExchangeEntry.acquisition(angular_step={'value': float(linelist[4]), 'units':'degree', 'dataset_opts':  {'dtype': 'd'}}))

                        # Interferometer settings

                        elif (linelist[0]=="Grid" and linelist[1]=="start"):
                                f.add_entry( DataExchangeEntry.interferometer(grid_start={'value': float(linelist[5]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Grid" and linelist[1]=="end"):
                                f.add_entry( DataExchangeEntry.interferometer(grid_end={'value': float(linelist[5]), 'units':'micron', 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Grid" and linelist[1]=="step"):
                                grid_steps = int(linelist[3])+1
                                f.add_entry( DataExchangeEntry.interferometer(number_of_grid_steps={'value': float(linelist[3]), 'dataset_opts':  {'dtype': 'd'}}))
                        elif (linelist[0]=="Grid" and linelist[1]=="period"):
                                f.add_entry( DataExchangeEntry.interferometer(number_of_grid_periods={'value': float(linelist[3]), 'dataset_opts':  {'dtype': 'd'}}))
		
        FILE.close()
	
##        imageAs2DArray = np.zeros((height,width), dtype=np.uint16)

##                
        starttime = time.clock()

        
##        rawImagesDataset = np.ones(nprj * height * width, np.uint16).reshape(nprj, height, width)
##        flatImagesDataset = np.ones(nflt * height * width, np.uint16).reshape(nflt, height, width)
##        darkImagesDataset = np.zeros(ndrk * height * width, np.uint16).reshape(ndrk, height, width)
##
##        dataThetaDataset = np.zeros(nprj, np.float).reshape(nprj)
##        flatThetaDataset = np.zeros(nflt, np.float).reshape(nflt)
##        darkThetaDataset = np.zeros(ndrk, np.float).reshape(ndrk)
##
####        darkImagesDataset = exchangeGrp.create_dataset('data_dark', (ndrk, height, width), 'uint16') # Create dataset
####        darkThetaDataset = exchangeGrp.create_dataset('theta_dark', (ndrk,), 'float') # Create dataset
##
##        for darkImageCounter in range(0, ndrk):
##                print "Dark " + str(darkImageCounter)
##                darkThetaDataset[darkImageCounter] = rotmin
##                darkImageName = samplename + str(darkImageCounter +1).zfill(4) + "." + "tif"
##                darkImageFullPath = tifdir + "/" + darkImageName
##
##                imageAs2DArray = Image.open(darkImageFullPath)
##                darkImagesDataset[darkImageCounter, :, :] = imageAs2DArray
##
####                with tifffile(darkImageFullPath) as tif:
####                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
####                        darkImagesDataset[darkImageCounter, :, :] = imageAs2DArray # Fill dataset
##
####        flatImagesDataset = exchangeGrp.create_dataset('data_white', (2*nflt*grid_steps, height, width), 'uint16')
####        flatThetaDataset = exchangeGrp.create_dataset('theta_flat', (2*nflt*grid_steps,), 'float') # Create dataset
##
##        for flatImageCounter in range(0, 2*nflt*grid_steps):
##                print "Flat " + str(flatImageCounter)
##                if flatImageCounter < nflt*grid_steps:
##                        offset = ndrk
##                        flatThetaDataset[flatImageCounter] = rotmin
##                else:
##                        offset = ndrk+nprj*grid_steps
##                        flatThetaDataset[flatImageCounter] = rotmax
##                flatImageName = samplename + str(flatImageCounter +offset +1).zfill(4) + "." + "tif"
##                flatImageFullPath = tifdir + "/" + flatImageName
##
##                imageAs2DArray = Image.open(flatImageFullPath)
##                flatImagesDataset[flatImageCounter, :, :] = imageAs2DArray
##
####                with tifffile(flatImageFullPath) as tif:
####                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
####                        flatImagesDataset[flatImageCounter, :, :] = imageAs2DArray
##
####        rawImagesDataset = exchangeGrp.create_dataset('data', (nprj*grid_steps, height, width), 'uint16')
####        dataThetaDataset = exchangeGrp.create_dataset('theta_data', (nprj*grid_steps,), 'float') # Create dataset
##
##        for rawDataImageCounter in range(0, nprj*grid_steps):
##                #print rawDataImageCounter//grid_steps
##                dataThetaDataset[rawDataImageCounter] = rotmin+(rawDataImageCounter//grid_steps)*angularStep
##                print "Projection " + str(rawDataImageCounter)
##                rawDataImageName = samplename + str(rawDataImageCounter +ndrk +nflt*grid_steps +1).zfill(4) + "." + "tif"
##                rawDataImageFullPath = tifdir + "/" + rawDataImageName
##
##                imageAs2DArray = Image.open(rawDataImageFullPath)
##                rawImagesDataset[rawDataImageCounter, :, :] = imageAs2DArray
####                with tifffile(rawDataImageFullPath) as tif:
####                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
####                        rawImagesDataset[rawDataImageCounter, :, :] = imageAs2DArray
##
##        f.add_entry( DataExchangeEntry.data(title={'value': 'dpc_tomography'}))
##
####        f.add_entry( DataExchangeEntry.data(data={'value': rawImagesDataset, 'units':'counts', 'description': 'dpc_raw_tomography', 'axes':'theta:y:x',
####                                            'dataset_opts': {'compression': 'gzip', 'compression_opts': 4} })
####        )
####        f.add_entry( DataExchangeEntry.data(data_dark={'value':darkImagesDataset, 'units':'counts', 'axes':'theta_dark:y:x',
####                                            'dataset_opts': {'compression': 'gzip', 'compression_opts': 4} })
####        )
####        f.add_entry( DataExchangeEntry.data(data_white={'value': flatImagesDataset, 'units':'counts', 'axes':'theta_white:y:x',
####                                            'dataset_opts': {'compression': 'gzip', 'compression_opts': 4} })
####        )
####        f.add_entry( DataExchangeEntry.data(theta={'value': dataThetaDataset, 'units':'degrees'}))
####        f.add_entry( DataExchangeEntry.data(theta_dark={'value': darkThetaDataset, 'units':'degrees'}))
####        f.add_entry( DataExchangeEntry.data(theta_white={'value': flatThetaDataset, 'units':'degrees'}))

        f.close()
##        imageFile.close() # Close file
        endtime = time.clock()
        print "time to write", str(endtime - starttime), "sec"
        print "speed", 2*(20+400+1441)*2048*2048/((endtime - starttime)*1000000000), "Gigabyte/s"

if __name__ == "__main__":
    main()

