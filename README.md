## About Data Exchange

Data Exchange is a Python toolbox for reading and writing  [Data Exchange](http://www.aps.anl.gov/DataExchange/) files. It provides an interface between tomographic raw datasets collected at different synchrotron facilities and [tomoPy](https://github.com/tomopy/tomopy/ "tomoPy"), a Python toolbox to perform tomographic data processing and image reconstruction tasks developed at the [Advanced Photon Source](http://www.aps.anl.gov/ "APS").

## External Dependencies:
- [tifffile.c](http://www.lfd.uci.edu/~gohlke/code/tifffile.c.html), a Python C extension module used by [tifffile.py](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html) for decoding PackBits and LZW encoded TIFF data

 

## Python Dependencies:

- [NumPy 1.8.0](http://www.numpy.org "numpy")
- [H5Py 2.2.1](http://www.h5py.org "h5py")
- [ez_setup 0.9](https://pypi.python.org/pypi/ez_setup "ez_setup")
- [tifffile.py](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html), a Python module to read and write image data from and to TIFF files.

## Installing Data Exchange:

Make sure you have [Python 2.6](http://www.python.org/download/releases/2.6/ "tsss...") or [2.7](http://www.python.org/download/releases/2.7/ "tsss...") and the above dependencies installed in your system. 

- To install from an egg distribution download the [latest released egg](https://github.com/data-exchange/data-exchange/releases) for your system, open shell prompt and type `easy_install my-egg-name` in the directory where the egg resides. 
- To build and install from source, download the [latest source tarball](https://github.com/data-exchange/data-exchange/releases), open shell prompt and type `python setup.py install` or `python setup.py install --user` in the directory where `setup.py` resides.

To test if the installation was succesfull, open a new shell and try:

- ``python -c "import data_exchange"``

## Using Data Exchange:

- In [`data-exchange/src/python/examples`](https://github.com/data-exchange/data-exchange/tree/master/src/python/examples) there are readers to handle tomographic datasets collected at all major synchrotron facilities.




