import data_exchange as dex
from datetime import datetime

# DataExchangeEntry has a predefined class for each entry in the reference manual
att = dex.DataExchangeEntry.attenuator()

# All attenuator elements are predefined so tab-completion will work in ipython
att.distance['value'] = 5.0
att.distance['units'] =  'm'
att.thickness['value'] = 1.0
att.thickness['units'] = 'mm'
# Value MUST be defined. All other attributes are optional. Any attribute can be added
att.type['value'] = 'silicon'
att.type['units'] = 'text'
att.type['puchased'] = datetime.now().isoformat()




f = dex.DataExchangeFile('test_Data_Exchange.h5', mode='w')
f.add_entry(att)


