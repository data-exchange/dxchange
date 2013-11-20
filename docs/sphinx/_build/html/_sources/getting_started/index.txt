***************
Getting Started
***************

Data Exchange Reference
-----------------------
For more details on the Data Exchange standard see: `link <http://www.aps.anl.gov/DataExchange/>`_.

Dependencies
------------
To use data_exchange you will need to have `h5py <https://github.com/h5py/h5py>`_ installed. ``h5py`` comes pre-installed in the Enthought Python Distribution. 

Creating Data Exchange Files
----------------------------
A data_exchange file can be created::

	import data_exchange as dex

	f = dex.DataExchangeFile('DataExchange_test.h5', mode='w')

The file 'DataExchange_test.h5' will be created and it will have two groups already defined (as per the Data Exchange reference):
	* implements,
	* exchange.

The 'implements' dataset is kept up to date by calling the ``create_top_level_group`` method when creating groups in file root.

Adding Data To Data Exchange Files
----------------------------------

Data is added to the data exchange file using DataExchangeEntry instances. There are predefined entries for:
	* data
	* sample
	* geometry
	* experiment
	* experimenter
	* exchange
	* instrument
	* source
	* shutter
	* attenuator
	* monochromator
	* detector
	* roi
	* objective
	* scintillator
	* translation
	* orientation

These classes have a specific structure which allows them to be parsed and added to the Data Exchange file. The structure is flexible enough to allow arbitrary datasets and attributes. Groups cannot be defined arbitrarily and this is by design because the group should be an agreed upon part of the Data Exchange definition.

Each entry type has a default location in the hdf5 path wher it will be placed. So for sample::

	sample = dex.DataExchangeEntry.sample()

You can change the default location::

	sample = dex.DataExchangeEntry.sample(root='/measurement_4/')
	sample.root = '/measurement_4'

When sample is added to the Data Exchange file it will create a group ``/measurement/sample``. The deault name ``sample`` can also be modified::

	sample.entry_name = 'sample_7'

which will cause the group ``/measurement/sample_7`` to be created.

Each entry has a number of predefined datasets and attributes but these are arbitrary. Datasets are defined as the keyword to the entry definition and the data is specified in a dictionary entry called ``value``.
The follwing will create a dataset called name whose data is 'sample'::

	sample = dex.DataExchangeEntry.sample(name={'value':'sample'})

Any other values in the dictionary will be treated as attributues for the ``name`` dataset::

	sample = dex.DataExchangeEntry.sample(temperature={'value':120.0, 'units':'celsius'})

You can specify options to the underlying ``h5py.create_dataset`` function like this::

	import numpy as np
	d = dex.DataExchangeEntry.data(data={'value': np.zeros((10,10)), 
	                                     'units':'m', 
	                                     'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4}}
	                                     )

Add a timestamp in ``iso8601`` format like this::
	
	from datetime import datetime
	d = dex.DataExchangeEntry.data(data={'value': np.zeros((10,10)), 
	                                     'units':'m', 
	                                     'datetime': datetime.now().isoformat()
	                                     })
