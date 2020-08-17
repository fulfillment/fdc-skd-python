# swagger_client.AuthApi

All URIs are relative to *https://api.fulfillment.com/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_oauth_access_token**](AuthApi.md#post_oauth_access_token) | **POST** /oauth/access_token | Generate an Access Token

# **post_oauth_access_token**
> AccessTokenResponseV2 post_oauth_access_token(body)

Generate an Access Token

By default tokens are valid for 7 days while refresh tokens are valid for 30 days. If your `grant_type` is \"password\" include the `username` and `password`, if however your `grant_type` is \"refresh_token\" the username/password are not required, instead set the `refresh_token`

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AuthApi()
body = swagger_client.AccessTokenRequestV2() # AccessTokenRequestV2 | Get an access token

try:
    # Generate an Access Token
    api_response = api_instance.post_oauth_access_token(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthApi->post_oauth_access_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccessTokenRequestV2**](AccessTokenRequestV2.md)| Get an access token | 

### Return type

[**AccessTokenResponseV2**](AccessTokenResponseV2.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

