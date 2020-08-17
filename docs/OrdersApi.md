# swagger_client.OrdersApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_orders_id**](OrdersApi.md#delete_orders_id) | **DELETE** /orders/{id} | Cancel an Order
[**get_order**](OrdersApi.md#get_order) | **GET** /orders/{id} | Order Details
[**get_orders**](OrdersApi.md#get_orders) | **GET** /orders | List of Orders
[**post_orders**](OrdersApi.md#post_orders) | **POST** /orders | New Order

# **delete_orders_id**
> Paths1orderspostresponses201contentapplication1jsonschema delete_orders_id(id)

Cancel an Order

Request an order is canceled to prevent shipment.

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
api_instance = swagger_client.OrdersApi(swagger_client.ApiClient(configuration))
id = 56 # int | ID of order that needs to be canceled

try:
    # Cancel an Order
    api_response = api_instance.delete_orders_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrdersApi->delete_orders_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| ID of order that needs to be canceled | 

### Return type

[**Paths1orderspostresponses201contentapplication1jsonschema**](Paths1orderspostresponses201contentapplication1jsonschema.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order**
> Paths1ordersgetresponses200contentapplication1jsonschema get_order(id, merchant_id=merchant_id, hydrate=hydrate)

Order Details

For the fastest results use the FDC provided `id` however you can use your `merchantOrderId` as the `id`.

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
api_instance = swagger_client.OrdersApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | The FDC order Id
merchant_id = 56 # int | Providing your `merchantId` indicates the `id` is your `merchantOrderId`. Although it is not necessary to provide this it will speed up your results when using your `merchantOrderId` however it will slow your results when using the FDC provided `id` (optional)
hydrate = ['hydrate_example'] # list[str] | Adds additional information to the response, uses a CSV format for multiple values.' (optional)

try:
    # Order Details
    api_response = api_instance.get_order(id, merchant_id=merchant_id, hydrate=hydrate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrdersApi->get_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The FDC order Id | 
 **merchant_id** | **int**| Providing your &#x60;merchantId&#x60; indicates the &#x60;id&#x60; is your &#x60;merchantOrderId&#x60;. Although it is not necessary to provide this it will speed up your results when using your &#x60;merchantOrderId&#x60; however it will slow your results when using the FDC provided &#x60;id&#x60; | [optional] 
 **hydrate** | [**list[str]**](str.md)| Adds additional information to the response, uses a CSV format for multiple values.&#x27; | [optional] 

### Return type

[**Paths1ordersgetresponses200contentapplication1jsonschema**](Paths1ordersgetresponses200contentapplication1jsonschema.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orders**
> OrderResponseOneOfV2 get_orders(from_date, to_date, merchant_ids=merchant_ids, warehouse_ids=warehouse_ids, page=page, limit=limit, hydrate=hydrate)

List of Orders

Retrieve many orders at once

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
api_instance = swagger_client.OrdersApi(swagger_client.ApiClient(configuration))
from_date = 'from_date_example' # str | Date-time in ISO 8601 format for selecting orders after, or at, the specified time
to_date = 'to_date_example' # str | Date-time in ISO 8601 format for selecting orders before, or at, the specified time
merchant_ids = [56] # list[int] | A CSV of merchant id, '123' or '1,2,3' (optional)
warehouse_ids = [56] # list[int] | A CSV of warehouse id, '123' or '1,2,3' (optional)
page = 1 # int | A multiplier of the number of items (limit paramater) to skip before returning results (optional) (default to 1)
limit = 80 # int | The numbers of items to return (optional) (default to 80)
hydrate = ['hydrate_example'] # list[str] | Adds additional information to the response, uses a CSV format for multiple values.' (optional)

try:
    # List of Orders
    api_response = api_instance.get_orders(from_date, to_date, merchant_ids=merchant_ids, warehouse_ids=warehouse_ids, page=page, limit=limit, hydrate=hydrate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrdersApi->get_orders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_date** | **str**| Date-time in ISO 8601 format for selecting orders after, or at, the specified time | 
 **to_date** | **str**| Date-time in ISO 8601 format for selecting orders before, or at, the specified time | 
 **merchant_ids** | [**list[int]**](int.md)| A CSV of merchant id, &#x27;123&#x27; or &#x27;1,2,3&#x27; | [optional] 
 **warehouse_ids** | [**list[int]**](int.md)| A CSV of warehouse id, &#x27;123&#x27; or &#x27;1,2,3&#x27; | [optional] 
 **page** | **int**| A multiplier of the number of items (limit paramater) to skip before returning results | [optional] [default to 1]
 **limit** | **int**| The numbers of items to return | [optional] [default to 80]
 **hydrate** | [**list[str]**](str.md)| Adds additional information to the response, uses a CSV format for multiple values.&#x27; | [optional] 

### Return type

[**OrderResponseOneOfV2**](OrderResponseOneOfV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_orders**
> OrderResponseV2 post_orders(body)

New Order

Error Notes&#58; * When `409 Conflict` is a 'Duplicate Order' the `context` will include the FDC `id`, see samples. 

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
api_instance = swagger_client.OrdersApi(swagger_client.ApiClient(configuration))
body = swagger_client.OrderRequestV2() # OrderRequestV2 | The order to create

try:
    # New Order
    api_response = api_instance.post_orders(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrdersApi->post_orders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrderRequestV2**](OrderRequestV2.md)| The order to create | 

### Return type

[**OrderResponseV2**](OrderResponseV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

