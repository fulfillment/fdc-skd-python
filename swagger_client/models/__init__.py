# coding: utf-8

# flake8: noqa
"""
    Fulfillment.com APIv2

    Welcome to our current iteration of our REST API. While we encourage you to upgrade to v2.0 we will continue support for our [SOAP API](https://github.com/fulfillment/soap-integration).  # Versioning  The Fulfillment.com (FDC) REST API is version controlled and backwards compatible. We have many future APIs scheduled for publication within our v2.0 spec so please be prepared for us to add data nodes in our responses, however, we will not remove knowledge from previously published APIs.  #### A Current Response  ```javascript {   id: 123 } ```  #### A Potential Future Response  ```javascript {   id: 123,   reason: \"More Knowledge\" } ```  # Getting Started  We use OAuth v2.0 to authenticate clients, you can choose [implicit](https://oauth.net/2/grant-types/implicit/) or [password](https://oauth.net/2/grant-types/password/) grant type. To obtain an OAuth `client_id` and `client_secret` contact your account executive.  **Tip**: Generate an additional login and use those credentials for your integration so that changes are accredited to that \"user\".  You are now ready to make requests to our other APIs by filling your `Authorization` header with `Bearer {access_token}`.  ## Perpetuating Access  Perpetuating access to FDC without storing your password locally can be achieved using the `refresh_token` returned by [POST /oauth/access_token](#operation/generateToken).  A simple concept to achieve this is outlined below.  1. Your application/script will ask you for your `username` and `password`, your `client_id` and `client_secret` will be accessible via a DB or ENV. 2. [Request an access_token](#operation/generateToken)   + Your function should be capable of formatting your request for both a `grant_type` of \\\"password\\\" (step 1) and \\\"refresh_token\\\" (step 4). 3. Store the `access_token` and `refresh_token` so future requests can skip step 1 4. When the `access_token` expires request anew using your `refresh_token`, replace both tokens in local storage.  + If this fails you will have to revert to step 1.  Alternatively if you choose for your application/script to have access to your `username` and `password` you can skip step 4.  In all scenarios we recommend storing all credentials outside your codebase.  ## Date Time Definitions  We will report all date-time stamps using the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard. When using listing API's where fromDate and toDate are available note that both dates are inclusive while requiring the fromDate to be before or at the toDate.  ### The Fulfillment Process  Many steps are required to fulfill your order we report back to you three fundamental milestones inside the orders model.  * `recordedOn` When we received your order. This will never change.  * `dispatchDate` When the current iteration of your order was scheduled for fulfillment. This may change however it is an indicator that the physical process of fulfillment has begun and a tracking number has been **assigned** to your order. The tracking number **MAY CHANGE**. You will not be able to cancel an order once it has been dispatched. If you need to recall an order that has been dispatched please contact your account executive.  * `departDate` When we recorded your order passing our final inspection and placed with the carrier. At this point it is **safe to inform the consignee** of the tracking number as it will not change.  ## Evaluating Error Responses  We currently return two different error models, with and without context. All errors will include a `message` node while errors with `context` will include additional information designed to save you time when encountering highly probable errors. For example, when you send us a request to create a duplicate order, we will reject your request and the context will include the FDC order `id` so that you may record it for your records.  ### Without Context  New order with missing required fields.  | Header | Response | | ------ | -------- | | Status | `400 Bad Request` |  ```javascript {       \"message\": \"Invalid request body\" } ```  ### With Context  New order with duplicate `merchantOrderId`.  | Header | Response | | ------ | -------- | | Status | `409 Conflict` |  ```javascript {   \"message\": \"Duplicate Order\",   \"context\": {     \"id\": 123   } } ```  ## Status Codes  Codes are a concatenation of State, Stage, and Detail.  `^([0-9]{2})([0-9]{2})([0-9]{2})$`  | Code | State              | Stage    | Detail         | | ---- | ------------------ | -------- | -------------- | | 010101 | Processing Order | Recieved | Customer Order | | 010102 | Processing Order | Recieved | Recieved | | 010201 | Processing Order | Approved | | | 010301 | Processing Order | Hold | Merchant Stock | | 010302 | Processing Order | Hold | Merchant Funds | | 010303 | Processing Order | Hold | For Merchant | | 010304 | Processing Order | Hold | Oversized Shipment | | 010305 | Processing Order | Hold | Invalid Parent Order | | 010306 | Processing Order | Hold | Invalid Address | | 010307 | Processing Order | Hold | By Admin | | 010401 | Processing Order | Address Problem | Incomplete Address | | 010402 | Processing Order | Address Problem | Invalid Locality | | 010403 | Processing Order | Address Problem | Invalid Region | | 010404 | Processing Order | Address Problem | Address Not Found | | 010405 | Processing Order | Address Problem | Many Addresses Found | | 010406 | Processing Order | Address Problem | Invalid Postal Code | | 010407 | Processing Order | Address Problem | Country Not Mapped | | 010408 | Processing Order | Address Problem | Invalid Recipient Name | | 010409 | Processing Order | Address Problem | Bad UK Address | | 010410 | Processing Order | Address Problem | Invalid Address Line 1 or 2 | | 010501 | Processing Order | Sku Problem | Invalid SKU | | 010501 | Processing Order | Sku Problem | Child Order has Invalid SKUs | | 010601 | Processing Order | Facility Problem | Facility Not Mapped | | 010701 | Processing Order | Ship Method Problem | Unmapped Ship Method | | 010702 | Processing Order | Ship Method Problem | Unmapped Ship Cost | | 010703 | Processing Order | Ship Method Problem | Missing Ship Method | | 010704 | Processing Order | Ship Method Problem | Invalid Ship Method | | 010705 | Processing Order | Ship Method Problem | Order Weight Outside of Ship Method Weight | | 010801 | Processing Order | Inventory Problem | Insufficient Inventory In Facility | | 010802 | Processing Order | Inventory Problem | Issue Encountered During Inventory Adjustment | | 010901 | Processing Order | Released To WMS | Released | | 020101 | Fulfillment In Progress | Postage Problem | Address Issue | | 020102 | Fulfillment In Progress | Postage Problem | Postage OK, OMS Issue Occurred | | 020103 | Fulfillment In Progress | Postage Problem | Postage Void Failed | | 020201 | Fulfillment In Progress | Postage Acquired | | | 020301 | Fulfillment In Progress | Postage Voided | Postage Void Failed Gracefully | | 020301 | Fulfillment In Progress | Hold | Departure Hold Requested | | 020401 | Fulfillment In Progress | 4PL Processing | | | 020501 | Fulfillment In Progress | 4PL Problem | Order is Proccessable, Postage Issue Occurred | | 020601 | Fulfillment In Progress | Label Printed | | | 020701 | Fulfillment In Progress | Shipment Cubed | | | 020801 | Fulfillment In Progress | Picking Inventory | | | 020901 | Fulfillment In Progress | Label Print Verified | | | 021001 | Fulfillment In Progress | Passed Final Inspection | | | 030101 | Shipped | Fulfilled By 4PL | | | 030102 | Shipped | Fulfilled By 4PL | Successfully Fulfilled, OMS Encountered Issue During Processing | | 030201 | Shipped | Fulfilled By FDC | | | 040101 | Returned | Returned | | | 050101 | Cancelled | Cancelled | | | 060101 | Test | Test | Test |   # noqa: E501

    OpenAPI spec version: 2.0
    Contact: dev@fulfillment.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from swagger_client.models.access_token_request_v2 import AccessTokenRequestV2
from swagger_client.models.access_token_response_v2 import AccessTokenResponseV2
from swagger_client.models.consignee_new_v2 import ConsigneeNewV2
from swagger_client.models.consignee_v2 import ConsigneeV2
from swagger_client.models.consignee_v21 import ConsigneeV21
from swagger_client.models.error_standard_v2 import ErrorStandardV2
from swagger_client.models.error_standard_with_context_v2 import ErrorStandardWithContextV2
from swagger_client.models.feature import Feature
from swagger_client.models.feature_properties import FeatureProperties
from swagger_client.models.geometry import Geometry
from swagger_client.models.iso_country_v2 import IsoCountryV2
from swagger_client.models.item_inventory_array_v2 import ItemInventoryArrayV2
from swagger_client.models.item_inventory_array_v2_item import ItemInventoryArrayV2Item
from swagger_client.models.item_inventory_array_v2_merchant import ItemInventoryArrayV2Merchant
from swagger_client.models.item_inventory_array_v2_meta import ItemInventoryArrayV2Meta
from swagger_client.models.item_inventory_array_v2_quantity import ItemInventoryArrayV2Quantity
from swagger_client.models.item_inventory_array_v2_quantity_total import ItemInventoryArrayV2QuantityTotal
from swagger_client.models.item_inventory_v2 import ItemInventoryV2
from swagger_client.models.merchant_v2 import MerchantV2
from swagger_client.models.one_of_access_token_request_v2 import OneOfAccessTokenRequestV2
from swagger_client.models.one_of_geometry_coordinates import OneOfGeometryCoordinates
from swagger_client.models.one_of_order_response_one_of_v2 import OneOfOrderResponseOneOfV2
from swagger_client.models.order_request_v2 import OrderRequestV2
from swagger_client.models.order_response_one_of_v2 import OrderResponseOneOfV2
from swagger_client.models.order_response_v2 import OrderResponseV2
from swagger_client.models.order_response_v2_parent_order import OrderResponseV2ParentOrder
from swagger_client.models.order_ship_v2 import OrderShipV2
from swagger_client.models.orders_items import OrdersItems
from swagger_client.models.orders_warehouse import OrdersWarehouse
from swagger_client.models.ordersidstatus_status import OrdersidstatusStatus
from swagger_client.models.pagination_v2 import PaginationV2
from swagger_client.models.return_v2 import ReturnV2
from swagger_client.models.returns_array_v2 import ReturnsArrayV2
from swagger_client.models.returns_array_v2_item import ReturnsArrayV2Item
from swagger_client.models.returns_array_v2_meta import ReturnsArrayV2Meta
from swagger_client.models.returns_array_v2_non_restocked_reason import ReturnsArrayV2NonRestockedReason
from swagger_client.models.returns_array_v2_order import ReturnsArrayV2Order
from swagger_client.models.returns_array_v2_status import ReturnsArrayV2Status
from swagger_client.models.returns_items import ReturnsItems
from swagger_client.models.rma_item_v2 import RmaItemV2
from swagger_client.models.rma_request_v2 import RmaRequestV2
from swagger_client.models.rma_response_v2 import RmaResponseV2
from swagger_client.models.status_event_v2 import StatusEventV2
from swagger_client.models.status_type_simple_v2 import StatusTypeSimpleV2
from swagger_client.models.status_type_v2 import StatusTypeV2
from swagger_client.models.status_type_v2_action_required_by import StatusTypeV2ActionRequiredBy
from swagger_client.models.status_type_v2_stage import StatusTypeV2Stage
from swagger_client.models.tracking_event_v2 import TrackingEventV2
from swagger_client.models.tracking_number_v2 import TrackingNumberV2
from swagger_client.models.tracking_response import TrackingResponse
from swagger_client.models.user_contact_v2 import UserContactV2
from swagger_client.models.user_contact_v21 import UserContactV21
from swagger_client.models.user_contact_v21_merchant import UserContactV21Merchant
from swagger_client.models.user_v2 import UserV2
