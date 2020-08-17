# swagger_client.TrackingApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_track**](TrackingApi.md#get_track) | **GET** /track | Tracking

# **get_track**
> TrackingResponse get_track(tracking_number=tracking_number)

Tracking

Get uniformed tracking events for any package, this response is carrier independent. Please note, an API Key is required for throttling purposes, please contact your success manager for details.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TrackingApi()
tracking_number = 'tracking_number_example' # str |  (optional)

try:
    # Tracking
    api_response = api_instance.get_track(tracking_number=tracking_number)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrackingApi->get_track: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tracking_number** | **str**|  | [optional] 

### Return type

[**TrackingResponse**](TrackingResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

