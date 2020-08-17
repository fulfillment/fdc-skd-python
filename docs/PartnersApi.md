# swagger_client.PartnersApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**put_orders_id_ship**](PartnersApi.md#put_orders_id_ship) | **PUT** /orders/{id}/ship | Ship an Order
[**put_orders_id_status**](PartnersApi.md#put_orders_id_status) | **PUT** /orders/{id}/status | Update Order Status

# **put_orders_id_ship**
> Paths1orderspostresponses201contentapplication1jsonschema put_orders_id_ship(body, id)

Ship an Order

Note, this API is used to update orders and is reserved for our shipping partners.

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
api_instance = swagger_client.PartnersApi(swagger_client.ApiClient(configuration))
body = swagger_client.OrderShipV2() # OrderShipV2 | Shipping Details
id = 56 # int | The FDC order Id

try:
    # Ship an Order
    api_response = api_instance.put_orders_id_ship(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PartnersApi->put_orders_id_ship: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrderShipV2**](OrderShipV2.md)| Shipping Details | 
 **id** | **int**| The FDC order Id | 

### Return type

[**Paths1orderspostresponses201contentapplication1jsonschema**](Paths1orderspostresponses201contentapplication1jsonschema.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_orders_id_status**
> Paths1orderspostresponses201contentapplication1jsonschema put_orders_id_status(body, id)

Update Order Status

Note, this API is used to update orders and is reserved for our shipping partners.

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
api_instance = swagger_client.PartnersApi(swagger_client.ApiClient(configuration))
body = swagger_client.StatusTypeSimpleV2() # StatusTypeSimpleV2 | New status event
id = 56 # int | The FDC order Id

try:
    # Update Order Status
    api_response = api_instance.put_orders_id_status(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PartnersApi->put_orders_id_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StatusTypeSimpleV2**](StatusTypeSimpleV2.md)| New status event | 
 **id** | **int**| The FDC order Id | 

### Return type

[**Paths1orderspostresponses201contentapplication1jsonschema**](Paths1orderspostresponses201contentapplication1jsonschema.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

