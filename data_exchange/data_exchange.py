"""
.. module:: data_exchange.py
   :platform: Unix
   :synopsis: Subclasses the h5py module for interacting with Data Exchange files.

.. moduleauthor:: David Vine <djvine@gmail.com>


""" 
from functools import wraps 
import h5py
import os
import sys
py3 = sys.version_info[0] == 3


class DataExchangeFile(h5py.File):
    """
    .. class:: DataExchangeFile(object)
        Interact with Data Exchange files.


        :method create_top_level_group: Helper function for creating a top level group which will update the implements group automagically.


    """
    def __init__(self, *args, **kwargs):
        super(DataExchangeFile, self).__init__(*args, **kwargs)

        if self.mode == 'w': #New File
            self.create_top_level_group('exchange')
        else:
            # Verify this file conforms to Data Exchange guidelines
            try:
                assert 'implements' in self.keys()
                assert 'exchange' in self.keys()
            except AssertionError:
                print('WARNING: {:s} does not have either/both "implements" or "exchange" group'.format(args[1]))

    def __repr__(self):
        if not self.id:
            r = u'<Closed DataExchange file>'
        else:
            # Filename has to be forced to Unicode if it comes back bytes
            # Mode is always a "native" string
            filename = self.filename
            if isinstance(filename, bytes):  # Can't decode fname
                filename = filename.decode('utf8', 'replace')
            r = u'<DataExchange file "%s" (mode %s)>' % (os.path.basename(filename),
                                                 self.mode)
        if py3:
            return r
        return r.encode('utf8')


    def create_top_level_group(self, group_name):
        self.create_group(group_name)
        try:
            implements = self['/implements'].value
            del self['implements']
            self.create_dataset('implements', data=':'.join([implements, group_name]))
        except KeyError:
            self.create_dataset('implements', data=group_name)

    def add_entry(self, dexen):

        assert isinstance(dexen.__base__, DataExchangeEntry)

        # Does HDF5 path exist?
        path = dexen.split('/')
        try:
            path.remove('')
        except ValueError:
            pass
        if not path[0] in self.keys():
            self.create_top_level_group(path[0])




        
            



class DataExchangeEntry(object):

    def __init__(self, **kwargs):
        self._entry_definitions()
        self._generate_classes()


    def _entry_definitions(self):
        """
        ..method:: _entry_definitions(self)

            This method contains the archetypes for Data Exchange file entries.

            The syntax for an entry is:
                *'root': The HDF5 path where this entry will be created (e.g. '/measurement_3/sample' or '/exchange/').
                *'name': The name of entry (e.g. 'monochromator' or 'sample_7'). It is a HDF5 Group.
                *'docstring': Describes this type of entry. E.g for sample: "The sample measured." 
                                    *This is used only for autogegnerating documentation for DataExchangeEntry.
                                    *It does not get written to the DataExchangeFile.
                *'ENTRY':   An entry is a dataset with attributes under the 'name' group.
                            Each 'ENTRY' should have:
                                * value: The dataset
                                * units: Units for value - an attribute of the dataset
                                * docstring: Used for autogenerating documentation 
                            Where a value is ``None`` this entry will not be added to the DataExchangeFile.
                            'ENTRY' can have any other parameter and these will be treated as HDF5 dataset attributes
        """


        self._attenuator = {
            'root': '/measurement',
            'name': 'attenuator',
            'docstring': 'X-ray beam attenuator.',
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


    def _generate_classes(self):

        # Generate a class for each entry definition
        for entry_name in self.__dict__:
            try:
                if entry_name.startswith('_'):
                    entry_type = getattr(self, entry_name)
                    entry_name = entry_name[1:]
                    if entry_name not in DataExchangeEntry.__dict__.keys():
                        entry_type['__base__'] = DataExchangeEntry
                        entry_type['__name__'] = entry_type['name']
                        setattr(DataExchangeEntry, entry_name, type(entry_type['name'], (object,), entry_type))
            except:
                print("Unable to create DataExchangeEntry for {:s}".format(entry_name))
                raise


DataExchangeEntry()
        








