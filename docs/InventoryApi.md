# swagger_client.InventoryApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_inventory**](InventoryApi.md#get_inventory) | **GET** /inventory | List of Item Inventories

# **get_inventory**
> ItemInventoryArrayV2 get_inventory(page=page, limit=limit, merchant_ids=merchant_ids, external_sku_names=external_sku_names)

List of Item Inventories

Retrieve inventory for one or more items. This API requires elevated permissions, please speak to your success manager.

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
api_instance = swagger_client.InventoryApi(swagger_client.ApiClient(configuration))
page = 1 # int | A multiplier of the number of items (limit paramater) to skip before returning results (optional) (default to 1)
limit = 80 # int | The numbers of items to return (optional) (default to 80)
merchant_ids = [56] # list[int] | A CSV of merchant id, '123' or '1,2,3' (optional)
external_sku_names = ['external_sku_names_example'] # list[str] | A CSV of sku reference names, 'skuName1' or 'skuName1,skuName2,skuName3' (optional)

try:
    # List of Item Inventories
    api_response = api_instance.get_inventory(page=page, limit=limit, merchant_ids=merchant_ids, external_sku_names=external_sku_names)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InventoryApi->get_inventory: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| A multiplier of the number of items (limit paramater) to skip before returning results | [optional] [default to 1]
 **limit** | **int**| The numbers of items to return | [optional] [default to 80]
 **merchant_ids** | [**list[int]**](int.md)| A CSV of merchant id, &#x27;123&#x27; or &#x27;1,2,3&#x27; | [optional] 
 **external_sku_names** | [**list[str]**](str.md)| A CSV of sku reference names, &#x27;skuName1&#x27; or &#x27;skuName1,skuName2,skuName3&#x27; | [optional] 

### Return type

[**ItemInventoryArrayV2**](ItemInventoryArrayV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

