# swagger_client.ReturnsApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_returns**](ReturnsApi.md#get_returns) | **GET** /returns | List Returns
[**put_returns**](ReturnsApi.md#put_returns) | **PUT** /returns | Inform us of an RMA

# **get_returns**
> ReturnsArrayV2 get_returns(from_date, to_date, page=page, limit=limit)

List Returns

Retrieves summary return activity during the queried timespan. Although return knowledge can be learned from `GET /orders/{id}` it can take an unknown amount of time for an order that is refused or undeliverable to return to an FDC facility. Instead we recommend regularly querying this API.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: fdcAuth
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.ReturnsApi(swagger_client.ApiClient(configuration))
from_date = 'from_date_example' # str | Date-time in ISO 8601 format for selecting orders after, or at, the specified time
to_date = 'to_date_example' # str | Date-time in ISO 8601 format for selecting orders before, or at, the specified time
page = 1 # int | A multiplier of the number of items (limit paramater) to skip before returning results (optional) (default to 1)
limit = 80 # int | The numbers of items to return (optional) (default to 80)

try:
    # List Returns
    api_response = api_instance.get_returns(from_date, to_date, page=page, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReturnsApi->get_returns: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_date** | **str**| Date-time in ISO 8601 format for selecting orders after, or at, the specified time | 
 **to_date** | **str**| Date-time in ISO 8601 format for selecting orders before, or at, the specified time | 
 **page** | **int**| A multiplier of the number of items (limit paramater) to skip before returning results | [optional] [default to 1]
 **limit** | **int**| The numbers of items to return | [optional] [default to 80]

### Return type

[**ReturnsArrayV2**](ReturnsArrayV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_returns**
> RmaResponseV2 put_returns(body)

Inform us of an RMA

Inform FDC of an expected return.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: fdcAuth
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.ReturnsApi(swagger_client.ApiClient(configuration))
body = swagger_client.RmaRequestV2() # RmaRequestV2 | RMA

try:
    # Inform us of an RMA
    api_response = api_instance.put_returns(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReturnsApi->put_returns: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RmaRequestV2**](RmaRequestV2.md)| RMA | 

### Return type

[**RmaResponseV2**](RmaResponseV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

