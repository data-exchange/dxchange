from nose.tools import *
import data_exchange as dex
import os
import shutil
import numpy as np
import ipdb

new_filename = 'new_file.h5'

def test_create_new_file():
	f = dex.DataExchangeFile(new_filename, mode='a')

	assert(os.path.isfile(new_filename))

	assert('implements' in f.keys())

	assert('exchange' in f.keys())

	assert(str(f['/implements'].value).find('exchange')>-1)

	f.close()

	os.remove(new_filename)

def test_create_dex_entry():
	# Create a file
	f = dex.DataExchangeFile(new_filename, mode='a')

	# Add some data
	rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
	f.add_entry(dex.DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}))

	# Close file
	f.close()

	os.remove(new_filename)

def test_open_existing_file():
	# Create a file
	f = dex.DataExchangeFile(new_filename, mode='a')

	# Add some data
	rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
	f.add_entry(dex.DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}))

	# Close file
	f.close()

	# Open file for readinf
	f = dex.DataExchangeFile(new_filename, mode='r')

	# Check that data is still there and was not deleted when the file was opened
	assert np.array_equal(f['/exchange/data'].value, rawdata)

	f.close()

	os.remove(new_filename)

def test_duplicate_data_exchange_entries():
	# Create a file
	f = dex.DataExchangeFile(new_filename, mode='a')

	# Add some data
	rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
	f.add_entry(dex.DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}))
	f.add_entry(dex.DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}))
	# Close file
	f.close()

	os.remove(new_filename)



