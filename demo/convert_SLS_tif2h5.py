#!/usr/bin/env python

import numpy as np
import h5py
import time
import os
import sys
import wx
from tifffile import tifffile

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
path_arg_at=0
if len(sys.argv) != 2 or sys.argv[1]=='-h':
        show_help()
        sys.exit(1)
else:
        path_arg_at=1

if path_arg_at>0:

        # tifdir
        tifdir = sys.argv[path_arg_at+0]

        # Set logdir and samplename
        os.chdir(tifdir)
        tifdir = os.getcwd()
        os.chdir(os.pardir)
        basename = os.getcwd()
        samplename = os.path.basename(basename)
        imageFileFullPath = basename + "/" + samplename + ".h5"
        if os.path.exists(imageFileFullPath):
                print "File exists, exiting"
                sys.exit()

        # Open HDF5 file
        imageFile = h5py.File(imageFileFullPath, 'w') 

        # Create basic definitions in root
        Implements = imageFile.create_dataset('implements', data = "exchange:measurement")

        # Exchange HDF5 group
        exchangeGrp = imageFile.create_group("exchange")

        # Measurement group
        measurementGrp = imageFile.create_group("measurement")

        # Sample group
        sampleGrp = measurementGrp.create_group("sample")
        sampleGrp.create_dataset('name', data = samplename)
        experimentGrp = sampleGrp.create_group("experiment")

        # Instrument group
        instGrp = measurementGrp.create_group("instrument")
        sourceGrp = instGrp.create_group("source")
        sourceGrp.create_dataset('name', data = "SLS")
        sourceGrp.create_dataset('beamline', data = "TOMCAT")
        energy=sourceGrp.create_dataset('energy', data = float(11.1))
        energy.attrs['units'] = "keV"
        monoGrp = instGrp.create_group("monochromator")
        detectorGrp = instGrp.create_group("detector")
        roiGrp=detectorGrp.create_group("roi")
        acqGrp = instGrp.create_group("acquisition")
        setupGrp = instGrp.create_group("setup")

        grid_steps=1	

        # Read info and userID from log file
        os.chdir(tifdir)
        filename0 = samplename + ".log"
        filename1 = samplename + "0001.tif"
        filename_image = os.path.join(tifdir,filename1)
        filename = os.path.join(tifdir,filename0)
        image = wx.Image(filename_image)
        height = int(image.GetHeight())
        width = int(image.GetWidth())

        FILE = open(filename,"r")
        for line in FILE:
                linelist=line.split()
                if len(linelist)>1:

                        # Sample

                        if (linelist[0]=="User" and linelist[1]=="ID"):
                                experimentGrp.create_dataset('activity', data = linelist[3])
		   
                        # Beamline settings
		   	
                        elif (linelist[0]=="Ring" and linelist[1]=="current"):
                                current=sourceGrp.create_dataset('current', data = float(linelist[4]))
                                current.attrs['units'] = "mA"
                        elif (linelist[0]=="Beam" and linelist[1]=="energy"):
                                energy=monoGrp.create_dataset('energy', data = float(linelist[4]))
                                energy.attrs['units'] = "keV"
                        elif (linelist[0]=="Monostripe"):
                                monoGrp.create_dataset('mono_stripe', data = linelist[2])
                        elif (linelist[0]=="FE-Filter"):
                                attenuator1Grp = instGrp.create_group("attenuator_1")
                                attenuator1Grp.create_dataset('type', data = linelist[0])
                                attenuator1Grp.create_dataset('thickness', data = ' '.join(linelist[2:]))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="1"):
                                attenuator2Grp = instGrp.create_group("attenuator_2")
                                attenuator2Grp.create_dataset('type', data = ' '.join(linelist[0:2]))
                                attenuator2Grp.create_dataset('thickness', data = ' '.join(linelist[3:]))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="2"):
                                attenuator3Grp = instGrp.create_group("attenuator_3")
                                attenuator3Grp.create_dataset('type', data = ' '.join(linelist[0:2]))
                                attenuator3Grp.create_dataset('thickness', data = ' '.join(linelist[3:]))
                        elif (linelist[0]=="OP-Filter" and linelist[1]=="3"):
                                attenuator4Grp = instGrp.create_group("attenuator_4")
                                attenuator4Grp.create_dataset('type', data = ' '.join(linelist[0:2]))
                                attenuator4Grp.create_dataset('thickness', data = ' '.join(linelist[3:]))


                        # Detector settings

                        elif (linelist[0]=="Camera"):
                                camera=detectorGrp.create_dataset('model', data = ' '.join(linelist[2:]))
                        elif (linelist[0]=="Microscope"):
                                microscope=detectorGrp.create_dataset('microscope', data = ' '.join(linelist[2:]))
                        elif (linelist[0]=="Magnification"):
                                objGrp=detectorGrp.create_group("objective")
                                objGrp.create_dataset('magnification', data = float(linelist[2]))
                        elif (linelist[0]=="Scintillator"):
                                scintGrp=detectorGrp.create_group("scintillator")
                                scintGrp.create_dataset('type', data = ' '.join(linelist[2:]))
                        elif (linelist[0]=="Exposure" and linelist[1]=="time"):
                                exp=detectorGrp.create_dataset('exposure_time', data = float(linelist[4]))
                                exp.attrs['units'] = "ms"
                        elif (linelist[0]=="Delay" and linelist[1]=="time"):
                                delay=detectorGrp.create_dataset('delay_time', data = float(linelist[4]))
                                delay.attrs['units'] = "ms"
                        elif (linelist[0]=="Stabilization" and linelist[1]=="time"):
                                stabilization=detectorGrp.create_dataset('stabilization_time', data = float(linelist[4]))
                                stabilization.attrs['units'] = "ms"
                        elif (linelist[0]=="Actual" and linelist[1]=="pixel"):
                                xActualPixelSize=detectorGrp.create_dataset('x_actual_pixel_size', data = float(linelist[5]))
                                xActualPixelSize.attrs['units'] = "micron"
                                yActualPixelSize=detectorGrp.create_dataset('y_actual_pixel_size', data = float(linelist[5]))
                                yActualPixelSize.attrs['units'] = "micron"
                        elif (linelist[0]=="Millisecond"):
                                shutterGrp = instGrp.create_group("shutter")
                                shutterGrp.create_dataset('name', data = "Millisecond shutter")
                                shutterGrp.create_dataset('status', data = ' '.join(linelist[4:]))			
                        elif (linelist[0]=="X-ROI"):
                                roiGrp.create_dataset('x1', data = int(linelist[2]))
                                roiGrp.create_dataset('x2', data = int(linelist[4]))
                        elif (linelist[0]=="Y-ROI"):
                                roiGrp.create_dataset('y1', data = int(linelist[2]))
                                roiGrp.create_dataset('y2', data = int(linelist[4]))


                        elif (linelist[0]=="X-coordinate"):
                                x=setupGrp.create_dataset('sample_x', data = float(linelist[2]))
                                x.attrs['units'] = "micron"
                        elif (linelist[0]=="Y-coordinate"):
                                y=setupGrp.create_dataset('sample_y', data = float(linelist[2]))
                                y.attrs['units'] = "micron"
                        elif (linelist[0]=="Z-coordinate"):
                                z=setupGrp.create_dataset('sample_z', data = float(linelist[2]))
                                z.attrs['units'] = "micron"
                        elif (linelist[0]=="XX-coordinate"):
                                xx=setupGrp.create_dataset('sample_xx', data = float(linelist[2]))
                                xx.attrs['units'] = "micron"
                        elif (linelist[0]=="ZZ-coordinate"):
                                zz=setupGrp.create_dataset('sample_zz', data = float(linelist[2]))
                                zz.attrs['units'] = "micron"

                        # Scan settings
                           
                        elif (linelist[1]=="scan" and linelist[2]=="of"):
                                acqGrp.create_dataset('type', data = linelist[0])
                                startdate= linelist[7] + " " + linelist[8] + " " + linelist[9] + " " + linelist[10] + " " + linelist[11]		
                                acqGrp.create_dataset('start_date', data = startdate)
                        elif (linelist[1]=="SCAN" and linelist[2]=="FINISHED"):
                                enddate= linelist[4] + " " + linelist[5] + " " + linelist[6] + " " + linelist[7] + " " + linelist[8]		
                                acqGrp.create_dataset('end_date', data = enddate)
                        elif (linelist[0]=="Number" and linelist[2]=="projections"):
                                nprj=int(linelist[4])
                                acqGrp.create_dataset('number_of_projections', data = int(linelist[4]))
                        elif (linelist[0]=="Number" and linelist[2]=="darks"):
                                ndrk=int(linelist[4])
                                acqGrp.create_dataset('number_of_darks', data = int(linelist[4]))
                        elif (linelist[0]=="Number" and linelist[2]=="flats"):
                                nflt=int(linelist[4])
                                acqGrp.create_dataset('number_of_flats', data = int(linelist[4]))
                        elif (linelist[0]=="Sample" and linelist[1]=="In"):
                                sampleIn=acqGrp.create_dataset('sample_in', data = float(linelist[4]))
                                sampleIn.attrs['units'] = "micron"
                        elif (linelist[0]=="Sample" and linelist[1]=="Out"):
                                sampleOut=acqGrp.create_dataset('sample_out', data = float(linelist[4]))
                                sampleOut.attrs['units'] = "micron"
                        elif (linelist[0]=="Rot" and linelist[2]=="min"):
                                rotmin = float(linelist[6])
                                acqGrp.create_dataset('rotation_start_angle', data = float(linelist[6]))
                        elif (linelist[0]=="Rot" and linelist[2]=="max"):
                                rotmax = float(linelist[6])
                                acqGrp.create_dataset('rotation_end_angle', data = float(linelist[6]))
                        elif (linelist[0]=="Angular" and linelist[1]=="step"):
                                angularStep = float(linelist[4])
                                acqGrp.create_dataset('angular_step', data = float(linelist[4]))

                        # Interferometer settings

                        elif (linelist[0]=="Grid" and linelist[1]=="start"):
                                interferometerGrp = setupGrp.create_group("interferometer")
                                interferometerGrp.create_dataset('grid_start', data = float(linelist[5]))
                        elif (linelist[0]=="Grid" and linelist[1]=="end"):
                                interferometerGrp.create_dataset('grid_end', data = float(linelist[5]))
                        elif (linelist[0]=="Grid" and linelist[1]=="step"):
                                grid_steps = int(linelist[3])+1
                                interferometerGrp.create_dataset('number_of_grid_steps', data = int(linelist[3]))
                        elif (linelist[0]=="Grid" and linelist[1]=="period"):
                                grid_periods = int(linelist[3])
                                interferometerGrp.create_dataset('number_of_grid_periods', data = int(linelist[3]))
		
        FILE.close()
	
        imageAs2DArray = np.zeros((height,width), dtype=np.uint16)
                
        starttime = time.clock()
        darkImagesDataset = exchangeGrp.create_dataset('data_dark', (ndrk, height, width), 'uint16') # Create dataset
        darkThetaDataset = exchangeGrp.create_dataset('theta_dark', (ndrk,), 'float') # Create dataset
        for darkImageCounter in range(0, ndrk):
                print "Dark " + str(darkImageCounter)
                darkThetaDataset[darkImageCounter] = rotmin
                darkImageName = samplename + str(darkImageCounter +1).zfill(4) + "." + "tif"
                darkImageFullPath = tifdir + "/" + darkImageName
                with tifffile(darkImageFullPath) as tif:
                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
                        darkImagesDataset[darkImageCounter, :, :] = imageAs2DArray # Fill dataset

        flatImagesDataset = exchangeGrp.create_dataset('data_white', (2*nflt*grid_steps, height, width), 'uint16')
        flatThetaDataset = exchangeGrp.create_dataset('theta_flat', (2*nflt*grid_steps,), 'float') # Create dataset
        for flatImageCounter in range(0, 2*nflt*grid_steps):
                print "Flat " + str(flatImageCounter)
                if flatImageCounter < nflt*grid_steps:
                        offset = ndrk
                        flatThetaDataset[flatImageCounter] = rotmin
                else:
                        offset = ndrk+nprj*grid_steps
                        flatThetaDataset[flatImageCounter] = rotmax
                flatImageName = samplename + str(flatImageCounter +offset +1).zfill(4) + "." + "tif"
                flatImageFullPath = tifdir + "/" + flatImageName
                with tifffile(flatImageFullPath) as tif:
                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
                        flatImagesDataset[flatImageCounter, :, :] = imageAs2DArray

        rawImagesDataset = exchangeGrp.create_dataset('data', (nprj*grid_steps, height, width), 'uint16')
        dataThetaDataset = exchangeGrp.create_dataset('theta_data', (nprj*grid_steps,), 'float') # Create dataset
        for rawDataImageCounter in range(0, nprj*grid_steps):
                #print rawDataImageCounter//grid_steps
                dataThetaDataset[rawDataImageCounter] = rotmin+(rawDataImageCounter//grid_steps)*angularStep
                print "Projection " + str(rawDataImageCounter)
                rawDataImageName = samplename + str(rawDataImageCounter +ndrk +nflt*grid_steps +1).zfill(4) + "." + "tif"
                rawDataImageFullPath = tifdir + "/" + rawDataImageName
                with tifffile(rawDataImageFullPath) as tif:
                        imageAs2DArray = tif.asarray()  # image is a np.ndarray
                        rawImagesDataset[rawDataImageCounter, :, :] = imageAs2DArray

        imageFile.close() # Close file
        endtime = time.clock()
        print "time to write", str(endtime - starttime), "sec"
        print "speed", 2*(20+400+1441)*2048*2048/((endtime - starttime)*1000000000), "Gigabyte/s"

