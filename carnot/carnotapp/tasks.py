from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from datetime import datetime
from celery import shared_task


import pandas as pd
import pdb
import os
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@shared_task
def storeData(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    filepath= os.path.join(parent_dir,filename)
    df = pd.read_excel(filepath)
    df = df.sort_values(by = 'sts')
    
    for idx, row in df.iterrows():
        device_id = row['device_fk_id']
        
        if cache.get(device_id):
            device_details = cache.get(device_id)
            starttime,endtime = device_details['starttime'],device_details['endtime']
            current_time_converted= datetime.fromisoformat(starttime)
            endtime_converted = datetime.fromisoformat(endtime)
            new_time = datetime.fromisoformat(row['sts']) 
            
            if new_time > endtime_converted:
                # cache.set(device_id, new_time)
                # Store other fields of the data as well
                device_details['end']=(row['longitude'],row['latitude']) 
                device_details['endtime'] = row['sts']
                if device_details['location']:
                    location = device_details['location']
                    location.append((row['longitude'],row['latitude']) )
                    device_details['location'] = location
                else : 
                    device_details['location'] = [(row['longitude'],row['latitude']) ]
                    
                if device_details['time']:
                    time =  device_details['time']
                    time.append(new_time)
                    device_details['time'] = time
                else : 
                    device_details['time'] = [row['sts']]
                    
                cache.set(device_id, device_details)
            elif new_time<current_time_converted:
                device_details['start']=(row['longitude'],row['latitude']) 
                device_details['starttime'] = row['sts']
                device_details['location'] =[(row['longitude'],row['latitude']) ]+device_details['location']
                device_details['time']  = [new_time]+device_details['time']

                cache.set(device_id, device_details)

                # cache.hmset(device_id, { start  'latitude': row['latitude'], 'longitude': row['longitude']})
        else:
        # If there is no data for the device ID in the cache, store it
            # cache.set(device_id, row['sts'])
            cache.set(device_id, {'start': (row['longitude'],row['latitude']), 'end': (row['longitude'],row['latitude']),'starttime':row['sts'],'endtime':row['sts'],'location':[(row['longitude'],row['latitude'])],'time':[row['sts']]},CACHE_TTL)
            

            
        
    
    