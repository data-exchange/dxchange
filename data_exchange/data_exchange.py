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
import pdb
py3 = sys.version_info[0] == 3


class DataExchangeFile(h5py.File):
    """
    .. class:: DataExchangeFile(object)
        Interact with Data Exchange files.


        :method create_top_level_group: Helper function for creating a top level group which will update the implements group automagically.


    """
    def __init__(self, *args, **kwargs):
        super(DataExchangeFile, self).__init__(*args, **kwargs)
        
        if kwargs['mode'] == 'w': #New File
            self.create_top_level_group('exchange')
        else:
            # Verify this file conforms to Data Exchange guidelines
            try:
                assert 'implements' in self.keys()
                assert 'exchange' in self.keys()
            except AssertionError:
                print('WARNING: File does not have either/both "implements" or "exchange" group')

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

    def add_entry(self, dexen_ob):

        if type(dexen_ob) != list:
            dexen_ob = [dexen_ob]

        for dexen in dexen_ob:

            # Does HDF5 path exist?
            path = dexen.root.split('/')
            try:
                path.remove('')
            except ValueError:
                pass
            if not path[0] in self.keys():
                self.create_top_level_group(path[0])

            root = dexen.root
            self.require_group(root)

            dsets = [ds for ds in dir(dexen) if not ds.startswith('__')]
            [dsets.remove(item) for item in ['entry_name', 'root', 'docstring']]

            for ds_name in dsets:
                if getattr(dexen, ds_name)['value'] is not None:
                    ds = self[getattr(dexen, 'root')].create_dataset(ds_name, data=getattr(dexen, ds_name)['value'])
                    for key in getattr(dexen, ds_name).keys():
                        if key in ['value', 'docstring']:
                            pass
                        else:
                            ds.attrs[key] = getattr(dexen, ds_name)[key]

        
            



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
                *'entry_name': The name of entry (e.g. 'monochromator' or 'sample_7'). It is a HDF5 Group.
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
        self._data = {
            'root': '/exchange',
            'entry_name': 'data',
            'docstring': 'The result of the measurement.',
            'data': {
                'value': None,
                'units': 'counts',
                'docstring': 'The result of the measurement.'
            },
        }

        self._sample = {
            'root': '/measurement',
            'entry_name': 'sample',
            'docstring': 'The sample measured.',
            'name': {
                'value': None,
                'units': 'text',
                'docstring': 'Descriptive name of the sample.'
            },
            'description': {
                'value': None,
                'units': 'text',
                'docstring': 'Description of the sample.'
            },
            'preparation date': {
                'value': None,
                'units': 'text',
                'docstring': 'Date and time the sample was prepared.'
            },
            'chemical formula': {
                'value': None,
                'units': 'text',
                'docstring': 'Sample chemical formula using the CIF format.'
            },
            'mass': {
                'value': None,
                'units': 'kg',
                'docstring': 'Mass of the sample.'
            },
            'concentration': {
                'value': None,
                'units': 'kgm^-3',
                'docstring': 'Mass/volume.'
            },
            'environment': {
                'value': None,
                'units': 'text',
                'docstring': 'Sample environment.'
            },
            'temperature': {
                'value': None,
                'units': 'kelvin',
                'docstring': 'Sample temperature.'
            },
            'temperature set': {
                'value': None,
                'units': 'kelvin',
                'docstring': 'Sample temperature set point.'
            },
            'pressure': {
                'value': None,
                'units': 'kPa',
                'docstring': 'Sample pressure.'
            },
            'thickness': {
                'value': None, 
                'units': 'm',
                'docstring': 'Sample thickness.'
            },
            'position': {
                'value': None,
                'units': 'text',
                'docstring': 'Sample position in the sample changer/robot.'
            }
        }

        self._geometry = {
            'root': '/measurement',
            'entry_name': 'geometry',
            'docstring': 'The general position and orientation of a component'
        }

        self._experiment = {
            'root': '/measurement',
            'entry_name': 'experiment',
            'docstring': 'This provides references to facility ids for the proposal, scheduled activity, and safety form.',
            'proposal': {
                'value': None,
                'units': 'text',
                'docstring': 'Proposal reference number. For the APS this is the General User Proposal number.'
            },
            'activity': {
                'value': None,
                'units': 'text',
                'docstring': 'Proposal scheduler id. For the APS this is the beamline scheduler activity id.'
            },
            'safety': {
                'value': None,
                'units': 'text',
                'docstring': 'Safety reference document. For the APS this is the Experiment Safety Approval Form number.'
            },
        }

        self._experimenter = {
            'root': '/measurement',
            'entry_name': 'experimenter',
            'docstring': 'Description of a single experimenter.',
            'name': {
                'value': None,
                'units': 'text',
                'docstring': 'User name.'
            },
            'role': {
                'value': None,
                'units': 'text',
                'docstring': 'User role.'
            },
            'affiliation': {
                'value': None,
                'units': 'text',
                'docstring': 'User affiliation.'
            },
            'address': {
                'value': None,
                'units': 'text',
                'docstring': 'User address.'
            },
            'phone': {
                'value': None,
                'units': 'text',
                'docstring': 'User phone number.'
            },
            'email': {
                'value': None,
                'units': 'text',
                'docstring': 'User email address.'
            },
            'facility_user_id': {
                'value': None,
                'units': 'text',
                'docstring': 'User badge number.'
            },
        }

        self._instrument = {
            'root': '/measurement',
            'entry_name': 'instrument',
            'docstring': 'All relevant beamline components status at the beginning of a measurement',
            'name': {
                'value': None,
                'units': 'text',
                'docstring': 'Name of the instrument.'
            },
        }

        self._source = {
            'root': '/measurement/instrument',
            'entry_name': 'source',
            'docstring': 'The light source being used',
            'name': {
                'value': None,
                'units': 'text',
                'docstring': 'Name of the facility.'
            },
            'datetime': {
                'value': None,
                'units': 'text',
                'docstring': 'Date and time source was measured.'
            },
            'beamline': {
                'value': None,
                'units': 'text',
                'docstring': 'Name of the beamline.'
            },
            'current': {
                'value': None,
                'units': 'A',
                'docstring': 'Electron beam current (A).'
            },
            'energy': {
                'value': None,
                'units': 'J',
                'docstring': 'Characteristic photon energy of the source (J). For an APS bending magnet this is 30 keV or 4.807e-15 J.'
            },
            'pulse_energy': {
                'value': None,
                'units': 'J',
                'docstring': 'Sum of the energy of all the photons in the pulse (J).'
            },
            'pulse_width': {
                'value': None,
                'units': 's',
                'docstring': 'Duration of the pulse (s).'
            },
            'source': {
                'value': None,
                'units': 'text',
                'docstring': 'Beam mode: TOPUP'
            },
            'beam intensity incident': {
                'value': None,
                'units': 'phs^-1',
                'docstring': 'Incident beam intensity in (photons per s).'
            },
            'beam intensity transmitted': {
                'value': None,
                'units': 'phs^-1',
                'docstring': 'Transmitted beam intensity (photons per s).'
            },
        }

        self._shutter = {
            'root': '/measurement/instrument',
            'entry_name': 'shutter',
            'docstring': 'The shutter being used',
            'name': {
                'value': None,
                'units': 'text',
                'docstring': 'Name of the shutter.'
            },
            'status': {
                'value': None,
                'units': 'text',
                'docstring': '"OPEN" or "CLOSED" or "NORMAL"'
            },
        }

        self._attenuator = {
            'root': '/measurement/instrument',
            'entry_name': 'attenuator',
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

        self._monochromator = {
            'root': '/measurement/instrument',
            'entry_name': 'monochromator',
            'docstring': 'X-ray beam monochromator.',
            'type': {
                'value': None,
                'units': 'text',
                'docstring': 'Multilayer type.'
            },
            'energy': {
                'value': None,
                'units': 'J',
                'docstring': 'Peak of the spectrum that the monochromator selects. Since units is not defined this field is in J and corresponds to 10 keV'
            },
            'energy_error': {
                'value': None,
                'units': 'J',
                'docstring': 'Standard deviation of the spectrum that the monochromator selects. Since units is not defined this field is in J.'
            },
            'mono_stripe': {
                'value': None,
                'units': 'text',
                'docstring': 'Type of multilayer coating or crystal.'
            }
        }

        self._detector = {
            'root': '/measurement/instrument',
            'entry_name': '_detector',
            'docstring': 'X-ray detector.',
            'manufacturer': {
                'value': None,
                'units': 'text',
                'docstring': 'The detector manufacturer.'
            },
            'model': {
                'value': None,
                'units': 'text',
                'docstring': 'The detector model'
            },
            'serial_number': {
                'value': None,
                'units': 'text',
                'docstring': 'The detector serial number.'
            },
            'output_data': {
                'value': None,
                'units': 'text',
                'docstring': 'String HDF5 path to the exchange group where the detector output data is located.'
            }
        }


    def _generate_classes(self):

        def __init__(self, **kwargs):
            for kw in kwargs:
                setattr(self, kw, kwargs[kw]) 

        # Generate a class for each entry definition
        for entry_name in self.__dict__:
            try:
                if entry_name.startswith('_'):
                    entry_type = getattr(self, entry_name)
                    entry_name = entry_name[1:]
                    if entry_name not in DataExchangeEntry.__dict__.keys():
                        entry_type['__base__'] = DataExchangeEntry
                        entry_type['__name__'] = entry_type['entry_name']
                        entry_type['__init__'] = __init__
                        setattr(DataExchangeEntry, entry_name, type(entry_type['entry_name'], (object,), entry_type))
            except:
                print("Unable to create DataExchangeEntry for {:s}".format(entry_name))
                raise



DataExchangeEntry()
        








