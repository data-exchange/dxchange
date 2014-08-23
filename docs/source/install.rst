.. APS Data Exchange toolbox

.. _installation:

========================
Installing Data Exchange
========================

Make sure you have Python 2.6 or 2.7
and these dependencies installed in your system. 

======  ==============================================
Python  URL
======  ==============================================
2.6     http://www.python.org/download/releases/2.6
2.7     http://www.python.org/download/releases/2.7
======  ==============================================

.. note:: This code was developed using the Enthought Python
   Distribution (www.enthought.com) which satisfies most of the
   above-stated Python Dependencies.

Python Dependencies
*******************

===========  =======  ====================================================
dependency   version  URL
===========  =======  ====================================================
NumPy        1.8.0    http://www.numpy.org 
H5Py         2.2.1    http://www.h5py.org
ez_setup     0.9      https://pypi.python.org/pypi/ez_setup
tifffile.py    -      http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html
===========  =======  ====================================================

.. note:: tifffile is a Python module to read and write image data from and to TIFF files


External Dependencies
*********************
==========  =======  ===================================================  
dependency  version  URL
==========  =======  ===================================================  
tifffile.c     -     http://www.lfd.uci.edu/~gohlke/code/tifffile.c.html
==========  =======  ===================================================  

.. note:: tiffile.c is a Python C extension module used by tifffile.py for decoding PackBits and LZW encoded TIFF data


Quick Install
-------------

==========  ==============================================================================================================
from        procedure
==========  ==============================================================================================================
source      #. download latest source tarball from https://github.com/data-exchange/data-exchange/releases then
            #. ``python setup.py install`` or ``python setup.py install --user`` in the directory where *setup.py* resides 
==========  ==============================================================================================================


To test if installation was succesfull:

#. open a new command shell
#. **change to a different directory than the tomopy source**
#. try::

    python -c "import dataexchange"

If it doesn't complain you are good to go!

Install Example
---------------

Here is a complete example of the installation:

#. download latest source .tar.gz from https://github.com/data-exchange/data-exchange/releases
#. expand the source .tar.gz into a new directory, build and install with these commands::

     /bin/tcsh
     setenv SANDBOX /tmp/sandbox
     mkdir -p $SANDBOX/lib/python2.7/site-packages/
     cd /tmp
     tar xzf ~/Downloads/data-exchange-0.0.2.tar.gz
     cd data_exchange-0.0.2/
     python install.py $SANDBOX 
     setenv LD_LIBRARY_PATH $SANDBOX/lib
     setenv C_INCLUDE_PATH $SANDBOX/include
     setenv PYTHONPATH $SANDBOX/lib/python2.7/site-packages/
     python setup.py install --prefix=$SANDBOX
     cd /tmp
 
     echo "SANDBOX = $SANDBOX"
     echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"
     echo "C_INCLUDE_PATH = $C_INCLUDE_PATH"
     echo "PYTHONPATH = $PYTHONPATH"
     python -c "import dataexchange"
