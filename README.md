# swagger-client
Welcome to our current iteration of our REST API. While we encourage you to upgrade to v2.0 we will continue support for our [SOAP API](https://github.com/fulfillment/soap-integration).  # Versioning  The Fulfillment.com (FDC) REST API is version controlled and backwards compatible. We have many future APIs scheduled for publication within our v2.0 spec so please be prepared for us to add data nodes in our responses, however, we will not remove knowledge from previously published APIs.  #### A Current Response  ```javascript {   id: 123 } ```  #### A Potential Future Response  ```javascript {   id: 123,   reason: \"More Knowledge\" } ```  # Getting Started  We use OAuth v2.0 to authenticate clients, you can choose [implicit](https://oauth.net/2/grant-types/implicit/) or [password](https://oauth.net/2/grant-types/password/) grant type. To obtain an OAuth `client_id` and `client_secret` contact your account executive.  **Tip**: Generate an additional login and use those credentials for your integration so that changes are accredited to that \"user\".  You are now ready to make requests to our other APIs by filling your `Authorization` header with `Bearer {access_token}`.  ## Perpetuating Access  Perpetuating access to FDC without storing your password locally can be achieved using the `refresh_token` returned by [POST /oauth/access_token](#operation/generateToken).  A simple concept to achieve this is outlined below.  1. Your application/script will ask you for your `username` and `password`, your `client_id` and `client_secret` will be accessible via a DB or ENV. 2. [Request an access_token](#operation/generateToken)   + Your function should be capable of formatting your request for both a `grant_type` of \\\"password\\\" (step 1) and \\\"refresh_token\\\" (step 4). 3. Store the `access_token` and `refresh_token` so future requests can skip step 1 4. When the `access_token` expires request anew using your `refresh_token`, replace both tokens in local storage.  + If this fails you will have to revert to step 1.  Alternatively if you choose for your application/script to have access to your `username` and `password` you can skip step 4.  In all scenarios we recommend storing all credentials outside your codebase.  ## Date Time Definitions  We will report all date-time stamps using the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard. When using listing API's where fromDate and toDate are available note that both dates are inclusive while requiring the fromDate to be before or at the toDate.  ### The Fulfillment Process  Many steps are required to fulfill your order we report back to you three fundamental milestones inside the orders model.  * `recordedOn` When we received your order. This will never change.  * `dispatchDate` When the current iteration of your order was scheduled for fulfillment. This may change however it is an indicator that the physical process of fulfillment has begun and a tracking number has been **assigned** to your order. The tracking number **MAY CHANGE**. You will not be able to cancel an order once it has been dispatched. If you need to recall an order that has been dispatched please contact your account executive.  * `departDate` When we recorded your order passing our final inspection and placed with the carrier. At this point it is **safe to inform the consignee** of the tracking number as it will not change.  ## Evaluating Error Responses  We currently return two different error models, with and without context. All errors will include a `message` node while errors with `context` will include additional information designed to save you time when encountering highly probable errors. For example, when you send us a request to create a duplicate order, we will reject your request and the context will include the FDC order `id` so that you may record it for your records.  ### Without Context  New order with missing required fields.  | Header | Response | | ------ | -------- | | Status | `400 Bad Request` |  ```javascript {       \"message\": \"Invalid request body\" } ```  ### With Context  New order with duplicate `merchantOrderId`.  | Header | Response | | ------ | -------- | | Status | `409 Conflict` |  ```javascript {   \"message\": \"Duplicate Order\",   \"context\": {     \"id\": 123   } } ```  ## Status Codes  Codes are a concatenation of State, Stage, and Detail.  `^([0-9]{2})([0-9]{2})([0-9]{2})$`  | Code | State              | Stage    | Detail         | | ---- | ------------------ | -------- | -------------- | | 010101 | Processing Order | Recieved | Customer Order | | 010102 | Processing Order | Recieved | Recieved | | 010201 | Processing Order | Approved | | | 010301 | Processing Order | Hold | Merchant Stock | | 010302 | Processing Order | Hold | Merchant Funds | | 010303 | Processing Order | Hold | For Merchant | | 010304 | Processing Order | Hold | Oversized Shipment | | 010305 | Processing Order | Hold | Invalid Parent Order | | 010306 | Processing Order | Hold | Invalid Address | | 010307 | Processing Order | Hold | By Admin | | 010401 | Processing Order | Address Problem | Incomplete Address | | 010402 | Processing Order | Address Problem | Invalid Locality | | 010403 | Processing Order | Address Problem | Invalid Region | | 010404 | Processing Order | Address Problem | Address Not Found | | 010405 | Processing Order | Address Problem | Many Addresses Found | | 010406 | Processing Order | Address Problem | Invalid Postal Code | | 010407 | Processing Order | Address Problem | Country Not Mapped | | 010408 | Processing Order | Address Problem | Invalid Recipient Name | | 010409 | Processing Order | Address Problem | Bad UK Address | | 010410 | Processing Order | Address Problem | Invalid Address Line 1 or 2 | | 010501 | Processing Order | Sku Problem | Invalid SKU | | 010501 | Processing Order | Sku Problem | Child Order has Invalid SKUs | | 010601 | Processing Order | Facility Problem | Facility Not Mapped | | 010701 | Processing Order | Ship Method Problem | Unmapped Ship Method | | 010702 | Processing Order | Ship Method Problem | Unmapped Ship Cost | | 010703 | Processing Order | Ship Method Problem | Missing Ship Method | | 010704 | Processing Order | Ship Method Problem | Invalid Ship Method | | 010705 | Processing Order | Ship Method Problem | Order Weight Outside of Ship Method Weight | | 010801 | Processing Order | Inventory Problem | Insufficient Inventory In Facility | | 010802 | Processing Order | Inventory Problem | Issue Encountered During Inventory Adjustment | | 010901 | Processing Order | Released To WMS | Released | | 020101 | Fulfillment In Progress | Postage Problem | Address Issue | | 020102 | Fulfillment In Progress | Postage Problem | Postage OK, OMS Issue Occurred | | 020103 | Fulfillment In Progress | Postage Problem | Postage Void Failed | | 020201 | Fulfillment In Progress | Postage Acquired | | | 020301 | Fulfillment In Progress | Postage Voided | Postage Void Failed Gracefully | | 020301 | Fulfillment In Progress | Hold | Departure Hold Requested | | 020401 | Fulfillment In Progress | 4PL Processing | | | 020501 | Fulfillment In Progress | 4PL Problem | Order is Proccessable, Postage Issue Occurred | | 020601 | Fulfillment In Progress | Label Printed | | | 020701 | Fulfillment In Progress | Shipment Cubed | | | 020801 | Fulfillment In Progress | Picking Inventory | | | 020901 | Fulfillment In Progress | Label Print Verified | | | 021001 | Fulfillment In Progress | Passed Final Inspection | | | 030101 | Shipped | Fulfilled By 4PL | | | 030102 | Shipped | Fulfilled By 4PL | Successfully Fulfilled, OMS Encountered Issue During Processing | | 030201 | Shipped | Fulfilled By FDC | | | 040101 | Returned | Returned | | | 050101 | Cancelled | Cancelled | | | 060101 | Test | Test | Test | 

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 2.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen
For more information, please visit [https://fulfillment.com](https://fulfillment.com)

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AuthApi(swagger_client.ApiClient(configuration))
body = swagger_client.AccessTokenRequestV2() # AccessTokenRequestV2 | Get an access token

try:
    # Generate an Access Token
    api_response = api_instance.post_oauth_access_token(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthApi->post_oauth_access_token: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.fulfillment.com/v2*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthApi* | [**post_oauth_access_token**](docs/AuthApi.md#post_oauth_access_token) | **POST** /oauth/access_token | Generate an Access Token
*InventoryApi* | [**get_inventory**](docs/InventoryApi.md#get_inventory) | **GET** /inventory | List of Item Inventories
*OrdersApi* | [**delete_orders_id**](docs/OrdersApi.md#delete_orders_id) | **DELETE** /orders/{id} | Cancel an Order
*OrdersApi* | [**get_order**](docs/OrdersApi.md#get_order) | **GET** /orders/{id} | Order Details
*OrdersApi* | [**get_orders**](docs/OrdersApi.md#get_orders) | **GET** /orders | List of Orders
*OrdersApi* | [**post_orders**](docs/OrdersApi.md#post_orders) | **POST** /orders | New Order
*PartnersApi* | [**put_orders_id_ship**](docs/PartnersApi.md#put_orders_id_ship) | **PUT** /orders/{id}/ship | Ship an Order
*PartnersApi* | [**put_orders_id_status**](docs/PartnersApi.md#put_orders_id_status) | **PUT** /orders/{id}/status | Update Order Status
*ReturnsApi* | [**get_returns**](docs/ReturnsApi.md#get_returns) | **GET** /returns | List Returns
*ReturnsApi* | [**put_returns**](docs/ReturnsApi.md#put_returns) | **PUT** /returns | Inform us of an RMA
*TrackingApi* | [**get_track**](docs/TrackingApi.md#get_track) | **GET** /track | Tracking
*UsersApi* | [**get_users_me**](docs/UsersApi.md#get_users_me) | **GET** /users/me | About Me

## Documentation For Models

 - [AccessTokenRequestV2](docs/AccessTokenRequestV2.md)
 - [AccessTokenResponseV2](docs/AccessTokenResponseV2.md)
 - [ConsigneeNewV2](docs/ConsigneeNewV2.md)
 - [ConsigneeV2](docs/ConsigneeV2.md)
 - [ConsigneeV21](docs/ConsigneeV21.md)
 - [ErrorStandardV2](docs/ErrorStandardV2.md)
 - [ErrorStandardWithContextV2](docs/ErrorStandardWithContextV2.md)
 - [Feature](docs/Feature.md)
 - [FeatureProperties](docs/FeatureProperties.md)
 - [Geometry](docs/Geometry.md)
 - [IsoCountryV2](docs/IsoCountryV2.md)
 - [ItemInventoryArrayV2](docs/ItemInventoryArrayV2.md)
 - [ItemInventoryArrayV2Item](docs/ItemInventoryArrayV2Item.md)
 - [ItemInventoryArrayV2Merchant](docs/ItemInventoryArrayV2Merchant.md)
 - [ItemInventoryArrayV2Meta](docs/ItemInventoryArrayV2Meta.md)
 - [ItemInventoryArrayV2Quantity](docs/ItemInventoryArrayV2Quantity.md)
 - [ItemInventoryArrayV2QuantityTotal](docs/ItemInventoryArrayV2QuantityTotal.md)
 - [ItemInventoryV2](docs/ItemInventoryV2.md)
 - [MerchantV2](docs/MerchantV2.md)
 - [OneOfAccessTokenRequestV2](docs/OneOfAccessTokenRequestV2.md)
 - [OneOfGeometryCoordinates](docs/OneOfGeometryCoordinates.md)
 - [OneOfOrderResponseOneOfV2](docs/OneOfOrderResponseOneOfV2.md)
 - [OrderRequestV2](docs/OrderRequestV2.md)
 - [OrderResponseOneOfV2](docs/OrderResponseOneOfV2.md)
 - [OrderResponseV2](docs/OrderResponseV2.md)
 - [OrderResponseV2ParentOrder](docs/OrderResponseV2ParentOrder.md)
 - [OrderShipV2](docs/OrderShipV2.md)
 - [OrdersItems](docs/OrdersItems.md)
 - [OrdersWarehouse](docs/OrdersWarehouse.md)
 - [OrdersidstatusStatus](docs/OrdersidstatusStatus.md)
 - [PaginationV2](docs/PaginationV2.md)
 - [ReturnV2](docs/ReturnV2.md)
 - [ReturnsArrayV2](docs/ReturnsArrayV2.md)
 - [ReturnsArrayV2Item](docs/ReturnsArrayV2Item.md)
 - [ReturnsArrayV2Meta](docs/ReturnsArrayV2Meta.md)
 - [ReturnsArrayV2NonRestockedReason](docs/ReturnsArrayV2NonRestockedReason.md)
 - [ReturnsArrayV2Order](docs/ReturnsArrayV2Order.md)
 - [ReturnsArrayV2Status](docs/ReturnsArrayV2Status.md)
 - [ReturnsItems](docs/ReturnsItems.md)
 - [RmaItemV2](docs/RmaItemV2.md)
 - [RmaRequestV2](docs/RmaRequestV2.md)
 - [RmaResponseV2](docs/RmaResponseV2.md)
 - [StatusEventV2](docs/StatusEventV2.md)
 - [StatusTypeSimpleV2](docs/StatusTypeSimpleV2.md)
 - [StatusTypeV2](docs/StatusTypeV2.md)
 - [StatusTypeV2ActionRequiredBy](docs/StatusTypeV2ActionRequiredBy.md)
 - [StatusTypeV2Stage](docs/StatusTypeV2Stage.md)
 - [TrackingEventV2](docs/TrackingEventV2.md)
 - [TrackingNumberV2](docs/TrackingNumberV2.md)
 - [TrackingResponse](docs/TrackingResponse.md)
 - [UserContactV2](docs/UserContactV2.md)
 - [UserContactV21](docs/UserContactV21.md)
 - [UserContactV21Merchant](docs/UserContactV21Merchant.md)
 - [UserV2](docs/UserV2.md)

## Documentation For Authorization


## apiKey

- **Type**: API key
- **API key parameter name**: x-api-key
- **Location**: HTTP header

## fdcAuth

- **Type**: OAuth
- **Flow**: password
- **Authorization URL**: 
- **Scopes**: 
 - ****: 


## Author

dev@fulfillment.com
