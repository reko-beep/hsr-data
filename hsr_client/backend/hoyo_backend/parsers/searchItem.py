

from ..constants import Types
from ..routes import ENTRY_URL_ROUTE

def make_model_compatible(raw_data : dict, type: Types):


    __compatibledict = {
       
    }
    __compatibledict['url'] = ENTRY_URL_ROUTE.format(entry_id = raw_data.get('entry_page_id', 0))
    __compatibledict['name'] = raw_data['name']
    __compatibledict['iconPath'] = raw_data['icon_url']
    __compatibledict['id'] = raw_data['entry_page_id']
    print(type, int(type))
    __compatibledict['type'] = int(type)

    exclude = {'name', 'icon_url', 'id'}

    ## add extra keys for filtering 
    extra_keys = list(set(raw_data['filter_values'].keys()) - exclude)
    for k in extra_keys:
        if 'values' in raw_data['filter_values'][k]:             
            if 'rarity' in k:
                __compatibledict['rarity'] = int(raw_data['filter_values'][k]['values'][0][0])
            else:                
                __compatibledict[k] = raw_data['filter_values'][k]['values'][0] 

   
           
   
    return __compatibledict

