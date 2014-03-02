## About Data Exchange

Data Exchange is a Python toolbox for reading and writing Data Exchange files.
Data Exchange interfaces with [tomoPy](https://github.com/tomopy/tomopy/ "tomoPy"), a Python toolbox to perform tomographic data processing and image reconstruction tasks at the [Advanced Photon Source](http://www.aps.anl.gov/ "APS").
Data Exchange readers handles tomographic datasets collected at all major synchron facilities and pipelines them into tomoPy.

## External Dependencies:
- [tifffile.c](http://www.lfd.uci.edu/~gohlke/code/tifffile.c.html), a Python C extension module used by [tifffile.py](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html) for decoding PackBits and LZW encoded TIFF data

 

## Python Dependencies:

- [tifffile.py](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html), a Python module to read and write image data from and to TIFF files.

## Installing Data Exchange:

Make sure you have [Python 2.6](http://www.python.org/download/releases/2.6/ "tsss...") or [2.7](http://www.python.org/download/releases/2.7/ "tsss...") and the above dependencies installed in your system. 

- To build and install from source, download the [latest source tarball](https://github.com/data-exchange/data-exchange/archive/master.zip), open shell prompt and change directory where the `setup.py` resides (../data-exchange/src/python/) then type `python setup.py install` or as user typy `python setup.py install --user`.

To test if installation was succesfull, open a new shell and try:

- ``python -c "import data_exchange"``

If it doesn't complain you are good to go!






