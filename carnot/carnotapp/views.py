"""
Methods for device related details endpoints.
"""




from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.cache import cache
from rest_framework.response import Response
from carnotapp.utilities.utility import storeData
from datetime import datetime

# Create your views here.


@api_view(['GET'])
def device_latest_info(request,device_id):
    "Return device details"
    device_details = cache.get(device_id)
    if not device_details:
        return Response({"message":"Device not Found!"})
    return Response(device_details)


@api_view(['GET'])
def device_location(request,device_id):
    "Return device location detail"
    device_details = cache.get(device_id)
    if not device_details:
        return Response({"message":"Device not Found!"})
    start = device_details.get('start')
    end = device_details.get('end')
    return Response({'start':start,'end':end})
@api_view(['POST'])
def filtered_location(request):
    "Return device time range details"
    device_details = cache.get(request.data.get('device_id'))
    if not device_details:
        return Response({"message":"Device not Found!"})
    try : 
        
        start_idx = device_details['time'].index(datetime.fromisoformat(request.data.get('starttime')))
        end_idx = device_details['time'].index(datetime.fromisoformat(request.data.get('endtime')))
    except : 
        return Response({'message':"location does not exist for given time"})
    
    return Response({'data':device_details['location'][start_idx:end_idx]})

@api_view(['GET'])
def redisappendddd(request):
    "Stores Data into Redis"
    storeData('raw_data (4) (5).xlsx')
    return Response({'message':"Successfully"})

    




