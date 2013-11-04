from nose.tools import *
import data_exchange as dex
import os
import shutil

new_filename = 'new_file.h5'
existing_filename = 'existing_file.h5'

def test_create_new_file():
	f = dex.DataExchangeFile(new_file)

	assert(os.path.isfile(new_file))

	assert('implements' in f.f.keys())

	assert('exchange' in f.f.keys())

	assert(str(f.f['/implements'].value).find('exchange')>-1)

