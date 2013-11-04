"""
.. module:: dataExchange.py
   :platform: Unix
   :synopsis: Implements classes for interacting with Data Exchange files.

.. moduleauthor:: David Vine <djvine@gmail.com>


""" 

import h5py
from h5py import create_group, create_dataset
import os
import sys

class DataExchangeFile(object):
	"""
	.. class:: DataExchangeFile(object)
        Create/Open/Append to Data Exchange files.


        :attr f: handle to the hdf5 file.


    """
	def __init__(self, filename):
		"""
		.. method:: __init__(filename)
			If filename exists, open in 'rw' mode.
			If filename doesn't exist, create new file.
		"""
		if os.path.isfile(filename): # File exists
			self.open_file(filename, mode='rw')
			if 'implements' not in self.f.listnames():
				raise Exception('{:s} has no root level "implements" group')
				sys.exit(1)

		else: # Create new file
			self.open_file(filename, mode='w')
			self.f.create_dataset('implements',data='')
			self.create_top_level_group('exchange')

	def __getitem__(self, item):
		return self.f[item]

	def __setitem__(self, item, value)
		self.f[item] = value

	def open_file(self, filename, mode='rw'):
		self.filename = filename
		self.filemode = mode
		self.f = h5py.File(filename, mode=mode)

	def close(self):
		self.f.close()

	def create_file(self, filename):
		self.open(filename, mode='w')

	def create_top_level_group(self, group_name):
		self.f.create_group(group_name)
		implements = self.f['/implements'].value
		del self.f['implements']
		if implements is '':
			self.create_group('implements', data=group_name)
		else:
			self.create_group('implements', data=':'.join([implements, group_name]))

	def create_measurement(self, **kwargs):
		self.f.create_top_level_group('measurement')

		# kwargs are measurement subgroups


class DataExchangeEntry(object):

	def __init__(self, **kwargs):
		pass

	def _archetype_definitions(self):
		"""
		SYNTAX:
		'root': '/',
		'name': 'NAME',
		'docstring': 'Class for describing X.'
			'': {
				'value': None,
				'units': 'm',
				'docstring': ''
			}
		"""


		self.attenuator = {
			'root': '/measurement',
			'name': 'attenuator',
			'docstring': 'Class for describing beam attenuators.'
			'distance': {
				'value': None,
				'units': 'm',
				'docstring': 'Distance from the sample'
			},
			'thickness': {
				'value': None,
				'units': 'm',
				'docstring': 'Thickness of attenuator along beam direction'
			},
			'attenuator_transmission': {
				'value': None,
				'units': 'None',
				'docstring': 'The nominal amount of the beam that gets through (transmitted intensity)/(incident intensity)'
			},
			'type': {
				'value': None,
				'units': 'text',
				'docstring': 'Type or composition of attenuator'
			}
		}





