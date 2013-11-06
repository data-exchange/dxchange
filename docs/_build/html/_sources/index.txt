.. data_exchange documentation master file, created by
   sphinx-quickstart on Tue Nov  5 22:08:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

data_exchange documentation
===========================

This is the documentation for data_exchange (updated: |today|)

data_exchange is a wrapper for h5py that takes the hassle out of making hdf5 files compatible with the `Data Exchange <http://www.aps.anl.gov/DataExchange/>`_ format.

What Is Data Exchange?
----------------------
The Scientific Data Exchange (or Data Exchange for short) is a set of guidelines for writing scientific data and meta-data in Hierarchical Data Format 5 (HDF5) files. The core principle of Data Exchange is that the guidelines must be simple and flexible enough that it is not necessary to use a support library beyond that supplied by the HDF Group. Since there is no library enforcing the file organization (beyond HDF5), the scientist is free to make their own choices as necessary, although the hope is that the guidelines are simple enough to follow that the end result will be more readily shared and understood data sets .

.. toctree::
   :maxdepth: 2

   getting_started/index
   data_exchange_api/index
   data_exchange_api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

