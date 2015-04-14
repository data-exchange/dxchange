# 
#   This file is part of Mantis, a Multivariate ANalysis Tool for Spectromicroscopy.
# 
#   Copyright (C) 2011 Mirna Lerotic, 2nd Look
#   http://2ndlookconsulting.com
#   License: GNU GPL v3
#
#   Mantis is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
#   Mantis is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details <http://www.gnu.org/licenses/>.



import numpy as np
import scipy as scy
import struct

import olefile as olef
            
import data_struct



#----------------------------------------------------------------------
class xrm:
    def __init__(self):
        pass
 
 
#----------------------------------------------------------------------
    def read_xrm_fileinfo(self, filename, readimgdata = False): 
        
        if not olef.isOleFile(filename):
            print "File not valid OLE type."
            return
        # Open OLE file:
        ole = olef.OleFileIO(filename)
        
        verbose = True
        
        if ole.exists('ImageInfo/ImagesTaken'):                  
            stream = ole.openstream('ImageInfo/ImagesTaken')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImagesTaken = %i" % nev[0]  
            nimgs = nev[0]
            nimgs = np.int(nimgs)
            
#        if nimgs > 1:
#            print 'This file has more than one image and cannot be used to make a stack.'
#            return 0, 0, 0

                
        if ole.exists('ImageInfo/ImageWidth'):                 
            stream = ole.openstream('ImageInfo/ImageWidth')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageWidth = %i" % nev[0]  
            n_cols = np.int(nev[0])

                
        if ole.exists('ImageInfo/ImageHeight'):                  
            stream = ole.openstream('ImageInfo/ImageHeight')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageHeight = %i" % nev[0]  
            n_rows = np.int(nev[0])
            
        if ole.exists('ImageInfo/Energy'):                  
            stream = ole.openstream('ImageInfo/Energy')
            data = stream.read()
            size = ole.get_size('ImageInfo/Energy')
            struct_fmt = "<{}f".format(size/4)
            eV = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Energy: ",  eV[0] 
            

        if ole.exists('MultiReferenceImage/TotalRefImages'):                  
            stream = ole.openstream('MultiReferenceImage/TotalRefImages')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "MultiReferenceImage/TotalRefImages = %i" % nev[0]  
            #n_rows = np.int(nev[0])
            
        if ole.exists('ReferenceData/Image'):                  
            stream = ole.openstream('ReferenceData/Image')
            data = stream.read()
            size = ole.get_size('ReferenceData/Image')
            struct_fmt = "<{}f".format(size/4)
            eV = struct.unpack(struct_fmt, data)
            if verbose: print "ReferenceData/Image: ",  eV[0] 
            
        if readimgdata == True:
            
            # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
            if ole.exists('ImageInfo/DataType'):                  
                stream = ole.openstream('ImageInfo/DataType')
                data = stream.read()
                struct_fmt = '<1I'
                datatype = struct.unpack(struct_fmt, data)
                datatype = int(datatype[0])
                if verbose: print "ImageInfo/DataType: %f " %  datatype  
            
            npix = n_cols*n_rows
            i = 1
            img_string = "ImageData%i/Image%i" % (np.ceil(i/100.0), i)
            stream = ole.openstream(img_string)
            data = stream.read()
            # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
            if datatype == 10:
                struct_fmt = "<{}f".format(npix)
                imgdata = struct.unpack(npix)
            elif datatype == 5:                   
                struct_fmt = "<{}h".format(npix)
                imgdata = struct.unpack(struct_fmt, data)
            else:                            
                print "Wrong data type"
                return
                         
            
            
        #Energy saved in the file is too coarse - read it from the filename
        filename = str(filename)
        str_list = filename[:-4].split('_')
        try: #look for 'eV' filed in the filename
        #if True:
            for i in range(len(str_list)):
                # In this case energy is stored like this: _0250.52eV_
                if 'eV' in str_list[i]:
                    ind = str_list[i].find('eV')
                    this_ev = (str_list[i])[:ind]
                    if len(this_ev)>0:
                        this_ev = float(this_ev)
                    else:
                        # In this case energy is stored like this: _0250.52_eV_
                        this_ev = str_list[i-1].strip()
                        this_ev = float(this_ev)
                    if verbose: print "Successfully read energy value from file name.", this_ev
                    eV = this_ev
                    break
        except:
            eV = eV[0]
            print 'Using energy stored in the file.', eV
            
        ole.close()
            
        if readimgdata == False:
            return n_cols, n_rows, eV
        else:
            return n_cols, n_rows, eV, imgdata

        
#----------------------------------------------------------------------    
    def read_xrm_list(self, filelist, filepath, ds): 
        
        #Fill the common stack data 
        file1 = os.path.join(filepath, filelist[0])   


        if not olef.isOleFile(file1):
            print "File not valid OLE type."
            return
        # Open OLE file:
        ole = olef.OleFileIO(file1)
        
        verbose = False
        
        
        if ole.exists('Version'):
            stream = ole.openstream('Version')
            data = stream.read()
            version = struct.unpack('<f', data)
            if verbose: print "version = ", version[0]  
                           
        if ole.exists('SampleInfo/Analyst'):
            stream = ole.openstream('SampleInfo/Analyst')
            data = stream.read()
            analyst = struct.unpack('<50s', data)
            analyst = analyst[0]
            if verbose: print "SampleInfo/Analyst = %s" % analyst
            
            
        if ole.exists('SampleInfo/Facility'):
            stream = ole.openstream('SampleInfo/Facility')
            data = stream.read()
            facility = struct.unpack('<50s', data)
            facility = facility[0]
            if verbose: print "SampleInfo/Facility = %s" % facility
                
        if ole.exists('SampleInfo/SampleID'):
            stream = ole.openstream('SampleInfo/SampleID')
            data = stream.read()
            sample = struct.unpack('<50s', data)
            sample = sample[0]
            if verbose: print "SampleInfo/SampleID = %s" % sample
        
            
        if ole.exists('ImageInfo/ImageWidth'):                 
            stream = ole.openstream('ImageInfo/ImageWidth')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageWidth = %i" % nev[0]  
            ncols = np.int(nev[0])

                
        if ole.exists('ImageInfo/ImageHeight'):                  
            stream = ole.openstream('ImageInfo/ImageHeight')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageHeight = %i" % nev[0]  
            nrows = np.int(nev[0])
            
           

        npix = ncols*nrows
        nev = len(filelist)
        absdata = np.zeros((ncols, nrows, nev))
        ev = np.zeros((nev))
        
        
        if ole.exists('ImageInfo/PixelSize'):                  
            stream = ole.openstream('ImageInfo/PixelSize')
            data = stream.read()
            struct_fmt = '<1f'
            pixelsize = struct.unpack(struct_fmt, data)
            pixelsize = pixelsize[0]
            if verbose: print "ImageInfo/PixelSize: %f " %  pixelsize  
            
        if ole.exists('ImageInfo/ImagesTaken'):                  
            stream = ole.openstream('ImageInfo/ImagesTaken')
            data = stream.read()
            data = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImagesTaken = %i" % data[0]  
            nimgs = data[0]
            nimgs = np.int(nimgs)

                
        if ole.exists('ImageInfo/ExpTimes'):                  
            stream = ole.openstream('ImageInfo/ExpTimes')
            data = stream.read()
            struct_fmt = "<{}f".format(nimgs)
            exptimes = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/ExpTimes: \n ",  exptimes
            
                
        # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
        if ole.exists('ImageInfo/DataType'):                  
            stream = ole.openstream('ImageInfo/DataType')
            data = stream.read()
            struct_fmt = '<1I'
            datatype = struct.unpack(struct_fmt, data)
            datatype = int(datatype[0])
            if verbose: print "ImageInfo/DataType: %f " %  datatype  
            
                   
        #Read the image data        
        for j in range(len(filelist)):
            fn = filelist[j]
            filename = os.path.join(filepath, fn)   
            ole = olef.OleFileIO(filename)  
            
            #folder contains 100 images 1-100, 101-200...           
            for i in range(1, nimgs+1):
                img_string = "ImageData%i/Image%i" % (np.ceil(i/100.0), i)
                stream = ole.openstream(img_string)
                data = stream.read()
                # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
                if datatype == 10:
                    struct_fmt = "<{}f".format(npix)
                    imgdata = struct.unpack(npix)
                elif datatype == 5:                   
                    struct_fmt = "<{}h".format(npix)
                    imgdata = struct.unpack(struct_fmt, data)
                else:                            
                    print "Wrong data type"
                    return
                    
            absdata[:,:,j] = np.reshape(imgdata, (ncols, nrows), order='F')
            
                
            ole.close()
            
           
            #Energy saved in the file is too coarse - read it from the filename
            str_list = filename[:-4].split('_')
            try: #look for 'eV' filed in the filename
                for i in range(len(str_list)):
                    # In this case energy is stored like this: _0250.52eV_
                    if 'eV' in str_list[i]:
                        ind = str_list[i].find('eV')
                        this_ev = (str_list[i])[:ind]
                        if len(this_ev)>0:
                            this_ev = float(this_ev)
                        else:
                            # In this case energy is stored like this: _0250.52_eV_
                            this_ev = str_list[i-1]
                            this_ev = float(this_ev)
                        if verbose: print "Successfully read energy value from file name.", this_ev
                        eV = this_ev
                        break
            except:
                eV = eV[0]
                print 'Using energy stored in the file.', eV 
                    
            ev[j] = this_ev
            
            
            
        if ev[-1]<ev[0]:
            ev = ev[::-1]
            absdata = absdata[:,:, ::-1]
       
        
        #Fill the data structure with data: 
        ds.implements = 'information:exchange:spectromicroscopy'
        ds.version = '1.0'
        ds.information.comment = 'Converted from .xrm file list',
        
        import datetime 
        now = datetime.datetime.now()
        ds.information.file_creation_datetime = now.strftime("%Y-%m-%dT%H:%M")

        ds.information.experimenter.name = analyst.replace('\x00', '')
        ds.information.sample.name = sample.replace('\x00', '')
        
        ds.exchange.data = absdata
        ds.exchange.data_signal = 1
        ds.exchange.data_axes='x:y'
        
        ds.exchange.energy=ev
        ds.exchange.energy_units = 'ev'
         
        #Since we do not have a scanning microscope we fill the x_dist and y_dist from pixel_size
        x_dist = np.arange(np.float(ncols))*pixelsize
        y_dist = np.arange(np.float(nrows))*pixelsize
    
        ds.exchange.x = x_dist
        ds.exchange.x_units = 'um'
        ds.exchange.y = y_dist
        ds.exchange.y_units = 'um'     
        
        self.data_dwell = np.ones((nev))*exptimes[0]
        ds.spectromicroscopy.data_dwell = self.data_dwell    
        
        return
    
#----------------------------------------------------------------------
    def read_xrm(self, filename, ds):
            
        if not olef.isOleFile(filename):
            print "File not valid OLE type."
            return
        # Open OLE file:
        ole = olef.OleFileIO(filename)
        # Get list of streams:
        #list = ole.listdir()
        #print list
        
        verbose = False
        

        # Test if known streams/storages exist:
        if ole.exists('Version'):
            stream = ole.openstream('Version')
            data = stream.read()
            version = struct.unpack('<f', data)
            if verbose: print "version = ", version[0]  
                           
        analyst = ''
        if ole.exists('SampleInfo/Analyst'):
            stream = ole.openstream('SampleInfo/Analyst')
            data = stream.read()
            analyst = struct.unpack('<50s', data)
            analyst = analyst[0]
            if verbose: print "SampleInfo/Analyst = %s" % analyst
                
        facility = ''
        if ole.exists('SampleInfo/Facility'):
            stream = ole.openstream('SampleInfo/Facility')
            data = stream.read()
            facility = struct.unpack('<50s', data)
            facility = facility[0]
            if verbose: print "SampleInfo/Facility = %s" % facility
                
        sample =''
        if ole.exists('SampleInfo/SampleID'):
            stream = ole.openstream('SampleInfo/SampleID')
            data = stream.read()
            sample = struct.unpack('<50s', data)
            sample = sample[0]
            if verbose: print "SampleInfo/SampleID = %s" % sample
                
                
                
        datasize = np.empty((3), dtype=np.int)
        if ole.exists('ImageInfo/ImagesTaken'):                  
            stream = ole.openstream('ImageInfo/ImagesTaken')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImagesTaken = %i" % nev[0]  
            nimgs = nev[0]
            datasize[2] = np.int(nimgs)
            self.n_ev = datasize[2]
                
        if ole.exists('ImageInfo/ImageWidth'):                 
            stream = ole.openstream('ImageInfo/ImageWidth')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageWidth = %i" % nev[0]  
            datasize[0] = np.int(nev[0])
            self.n_cols = datasize[0]
                
        if ole.exists('ImageInfo/ImageHeight'):                  
            stream = ole.openstream('ImageInfo/ImageHeight')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageHeight = %i" % nev[0]  
            datasize[1] = np.int(nev[0])
            self.n_rows = datasize[1]
                
        if ole.exists('ImageInfo/Angles'):                  
            stream = ole.openstream('ImageInfo/Angles')
            data = stream.read()
            struct_fmt = "<{}f".format(nimgs)
            angles = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Angles: \n ",  angles  
                
        if ole.exists('ImageInfo/Energy'):                  
            stream = ole.openstream('ImageInfo/Energy')
            data = stream.read()
            size = ole.get_size('ImageInfo/Energy')
            struct_fmt = "<{}f".format(size/4)
            eng = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Energy: \n ",  eng  
            self.ev = np.array(eng)
            
        #Energy saved in the file is too coarse - read it from the filename
        str_list = filename[:-4].split('_')
        try: #look for 'eV' filed in the filename
            ev_ind = str_list.index('eV')
            if verbose: print 'Energy value from filename = ', str_list[ev_ind-1]
            eng = float(str_list[ev_ind-1])
            self.ev = [eng]
        except:
            print 'Using energy stored in the file.'
            
        self.ev = np.array(self.ev)
                
        if ole.exists('ImageInfo/PixelSize'):                  
            stream = ole.openstream('ImageInfo/PixelSize')
            data = stream.read()
            struct_fmt = '<1f'
            pixelsize = struct.unpack(struct_fmt, data)
            pixelsize = pixelsize[0]
            if verbose: print "ImageInfo/PixelSize: %f " %  pixelsize  
                
        if ole.exists('ImageInfo/ExpTimes'):                  
            stream = ole.openstream('ImageInfo/ExpTimes')
            data = stream.read()
            struct_fmt = "<{}f".format(nimgs)
            exptimes = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/ExpTimes: \n ",  exptimes
            
                
        # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
        if ole.exists('ImageInfo/DataType'):                  
            stream = ole.openstream('ImageInfo/DataType')
            data = stream.read()
            struct_fmt = '<1I'
            datatype = struct.unpack(struct_fmt, data)
            datatype = int(datatype[0])
            if verbose: print "ImageInfo/DataType: %f " %  datatype  
         
        
        if verbose: print 'Reading images - please wait...'
        self.absdata = np.empty((self.n_cols, self.n_rows, self.n_ev), dtype=np.float32)
        #Read the images - They are stored in ImageData1, ImageData2... Each
        #folder contains 100 images 1-100, 101-200...           
        for i in range(1, nimgs+1):
            img_string = "ImageData%i/Image%i" % (np.ceil(i/100.0), i)
            stream = ole.openstream(img_string)
            data = stream.read()
            # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
            if datatype == 10:
                struct_fmt = "<{}f".format(self.n_cols*self.n_rows)
                imgdata = struct.unpack(struct_fmt, data)
            elif datatype == 5:                   
                struct_fmt = "<{}h".format(self.n_cols*self.n_rows)
                imgdata = struct.unpack(struct_fmt, data)
            else:                            
                print "Wrong data type"
                return
                    
            self.absdata[:,:,i-1] = np.reshape(imgdata, (self.n_cols, self.n_rows), order='F')
                
        
        if verbose: print 'Finished reading images'
        ole.close()
                
        #Fill the data structure with data: 
        ds.implements = 'information:exchange:spectromicroscopy'
        ds.version = '1.0'
        
        
        ds.information.comment = 'Converted from .txrm (Xradia file format)',
        

        ds.information.experimenter.name = analyst
        
        ds.information.sample.name = sample
        
        ds.exchange.data = self.absdata
        ds.exchange.data_signal = 1
        ds.exchange.data_axes='x:y'
        
        ds.exchange.energy=self.ev
        ds.exchange.energy_units = 'ev'
        
        
        #Since we do not have a scanning microscope we fill the x_dist and y_dist from pixel_size
        self.x_dist = np.arange(np.float(self.n_cols))*pixelsize
        self.y_dist = np.arange(np.float(self.n_rows))*pixelsize
    
        ds.exchange.x = self.x_dist
        ds.exchange.x_units = 'um'
        ds.exchange.y = self.y_dist
        ds.exchange.y_units = 'um'     
    
        
        ds.spectromicroscopy.data_dwell = exptimes
        
        self.data_dwell = np.ones((self.n_ev))*exptimes[0]
          
          
        return
        
#----------------------------------------------------------------------
    def read_txrm(self, filename, ds):
            
        if not olef.isOleFile(filename):
            print "File not valid OLE type."
            return
        # Open OLE file:
        ole = olef.OleFileIO(filename)
        # Get list of streams:
        #list = ole.listdir()
        #print list
        
        verbose = False

        # Test if known streams/storages exist:
        if ole.exists('Version'):
            stream = ole.openstream('Version')
            data = stream.read()
            version = struct.unpack('<f', data)
            if verbose: print "version = ", version[0]  
                           
        analyst = ''
        if ole.exists('SampleInfo/Analyst'):
            stream = ole.openstream('SampleInfo/Analyst')
            data = stream.read()
            analyst = struct.unpack('<50s', data)
            analyst = analyst[0]
            if verbose: print "SampleInfo/Analyst = %s" % analyst
                
        facility = ''
        if ole.exists('SampleInfo/Facility'):
            stream = ole.openstream('SampleInfo/Facility')
            data = stream.read()
            facility = struct.unpack('<50s', data)
            facility = facility[0]
            if verbose: print "SampleInfo/Facility = %s" % facility
                
        sample = ''
        if ole.exists('SampleInfo/SampleID'):
            stream = ole.openstream('SampleInfo/SampleID')
            data = stream.read()
            sample = struct.unpack('<50s', data)
            sample = sample[0]
            if verbose: print "SampleInfo/SampleID = %s" % sample
                
                
        datasize = np.empty((3), dtype=np.int)
        if ole.exists('ImageInfo/NoOfImages'):                  
            stream = ole.openstream('ImageInfo/NoOfImages')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/NoOfImages = %i" % nev[0]  
            nimgs = nev[0]
            datasize[2] = np.int(nimgs)
            self.n_ev = datasize[2]
            
        date = ''
        try:
            #This is an array of date+time stamps....
            if ole.exists('ImageInfo/Date'):   
                stream = ole.openstream('ImageInfo/Date')       
                data = stream.read()
                dates = struct.unpack('<'+'17s23x'*nimgs, data)
                date = dates[0]
                if verbose: print "ImageInfo/Date = %s" % date    
        except:
            pass
                
        if ole.exists('Alignment/StageShiftsApplied'):
            stream = ole.openstream('Alignment/StageShiftsApplied')
            data = stream.read()
            shift = struct.unpack('<I', data)
            if verbose: print "shift = ", shift[0]  

        if ole.exists('Alignment/X-Shifts'):                  
            stream = ole.openstream('Alignment/X-Shifts')
            data = stream.read()
            size = ole.get_size('Alignment/X-Shifts')
            struct_fmt = "<{}f".format(size/4)
            XShift = struct.unpack(struct_fmt, data)
            if verbose: print "Alignment/X-Shifts: \n ",  XShift  

        if ole.exists('Alignment/Y-Shifts'):                  
            stream = ole.openstream('Alignment/Y-Shifts')
            data = stream.read()
            size = ole.get_size('Alignment/Y-Shifts')
            struct_fmt = "<{}f".format(size/4)
            YShift = struct.unpack(struct_fmt, data)
            if verbose: print "Alignment/Y-Shifts: \n ",  YShift  

        if ole.exists('ImageInfo/XPosition'):                  
            stream = ole.openstream('ImageInfo/XPosition')
            data = stream.read()
            size = ole.get_size('ImageInfo/XPosition')
            struct_fmt = "<{}f".format(size/4)
            XPosition = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/XPosition: \n ",  XPosition  

        if ole.exists('ImageInfo/YPosition'):                  
            stream = ole.openstream('ImageInfo/YPosition')
            data = stream.read()
            size = ole.get_size('ImageInfo/YPosition')
            struct_fmt = "<{}f".format(size/4)
            YPosition = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/YPosition: \n ",  YPosition  

        if ole.exists('ImageInfo/ZPosition'):                  
            stream = ole.openstream('ImageInfo/ZPosition')
            data = stream.read()
            size = ole.get_size('ImageInfo/ZPosition')
            struct_fmt = "<{}f".format(size/4)
            ZPosition = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/ZPosition: \n ",  ZPosition  

        if ole.exists('ImageInfo/ImageWidth'):                 
            stream = ole.openstream('ImageInfo/ImageWidth')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageWidth = %i" % nev[0]  
            datasize[0] = np.int(nev[0])
            self.n_cols = datasize[0]
                
        if ole.exists('ImageInfo/ImageHeight'):                  
            stream = ole.openstream('ImageInfo/ImageHeight')
            data = stream.read()
            nev = struct.unpack('<I', data)
            if verbose: print "ImageInfo/ImageHeight = %i" % nev[0]  
            datasize[1] = np.int(nev[0])
            self.n_rows = datasize[1]
                
        if ole.exists('ImageInfo/Angles'):                  
            stream = ole.openstream('ImageInfo/Angles')
            data = stream.read()
            struct_fmt = "<{}f".format(nimgs)
            angles = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Angles: \n ",  angles  
        
        if ole.exists('ImageInfo/Energy'):                  
            stream = ole.openstream('ImageInfo/Energy')
            data = stream.read()
            size = ole.get_size('ImageInfo/Energy')
            struct_fmt = "<{}f".format(size/4)
            eng = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Energy: \n ",  eng  
            self.ev = np.array(eng)                           
                
        if ole.exists('ImageInfo/PixelSize'):                  
            stream = ole.openstream('ImageInfo/PixelSize')
            data = stream.read()
            struct_fmt = '<1f'
            pixelsize = struct.unpack(struct_fmt, data)
            pixelsize = pixelsize[0]
            if verbose: print "ImageInfo/PixelSize: %f " %  pixelsize  
                
        if ole.exists('ImageInfo/ExpTimes'):                  
            stream = ole.openstream('ImageInfo/ExpTimes')
            data = stream.read()
            struct_fmt = "<{}f".format(nimgs)
            exptimes = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/ExpTimes: \n ",  exptimes
            
                
        # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
        if ole.exists('ImageInfo/DataType'):                  
            stream = ole.openstream('ImageInfo/DataType')
            data = stream.read()
            struct_fmt = '<1I'
            datatype = struct.unpack(struct_fmt, data)
            datatype = int(datatype[0])
            if verbose: print "ImageInfo/DataType: %f " %  datatype  
         
            
        self.absdata = np.empty((self.n_cols, self.n_rows, self.n_ev), dtype=np.float32)
        #Read the images - They are stored in ImageData1, ImageData2... Each
        #folder contains 100 images 1-100, 101-200...           
        for i in range(1, nimgs+1):
            img_string = "ImageData%i/Image%i" % (np.ceil(i/100.0), i)
            stream = ole.openstream(img_string)
            data = stream.read()
            # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
            if datatype == 10:
                struct_fmt = "<{}f".format(self.n_cols*self.n_rows)
                imgdata = struct.unpack(struct_fmt, data)
            elif datatype == 5:                   
                struct_fmt = "<{}h".format(self.n_cols*self.n_rows)
                imgdata = struct.unpack(struct_fmt, data)
            else:                            
                print "Wrong data type"
                return
                    
            self.absdata[:,:,i-1] = np.reshape(imgdata, (self.n_cols, self.n_rows), order='F')
                
        ole.close()
                
        #Fill the data structure with data: 
        ds.implements = 'information:exchange:spectromicroscopy'
        ds.version = '1.0'
        
        
        ds.information.file_creation_datetime = date
        ds.information.comment = 'Converted from .txrm (Xradia file format)',
        

        ds.information.experimenter.name = analyst
        
        ds.information.sample.name = sample
        
        ds.exchange.data = self.absdata
        ds.exchange.data_signal = 1
        ds.exchange.data_axes='x:y'
        
        ds.exchange.energy=self.ev
        ds.exchange.energy_units = 'keV'
        
        
        #Since we do not have a scanning microscope we fill the x_dist and y_dist from pixel_size
        self.x_dist = np.arange(np.float(self.n_cols))*pixelsize
        self.y_dist = np.arange(np.float(self.n_rows))*pixelsize
    
        ds.exchange.x = self.x_dist
        ds.exchange.x_units = 'um'
        ds.exchange.y = self.y_dist
        ds.exchange.y_units = 'um'    
        
        ds.exchange.angles = angles

        ds.spectromicroscopy.data_dwell = exptimes 
        
        
        self.data_dwell = np.ones((self.n_ev))*exptimes[0]
          
        ds.exchange.sample_position_x = XPosition
        ds.exchange.sample_position_y = YPosition
        ds.exchange.sample_position_z = ZPosition

        ds.exchange.sample_image_shift_x = XShift
        ds.exchange.sample_image_shift_y = YShift

        ds.exchange.actual_pixel_size =  pixelsize 
        return
    

