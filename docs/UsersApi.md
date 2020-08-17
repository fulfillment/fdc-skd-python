# swagger_client.UsersApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_users_me**](UsersApi.md#get_users_me) | **GET** /users/me | About Me

# **get_users_me**
> UserContactV2 get_users_me()

About Me

Returns the user profile of the access token's owner. This could be useful if managing multiple accounts or confirming validity of a token.

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
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))

try:
    # About Me
    api_response = api_instance.get_users_me()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_users_me: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserContactV2**](UserContactV2.md)

### Authorization

[fdcAuth](../README.md#fdcAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

