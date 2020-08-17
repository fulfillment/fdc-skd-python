# coding: utf-8

"""
    Fulfillment.com APIv2

    Welcome to our current iteration of our REST API. While we encourage you to upgrade to v2.0 we will continue support for our [SOAP API](https://github.com/fulfillment/soap-integration).  # Versioning  The Fulfillment.com (FDC) REST API is version controlled and backwards compatible. We have many future APIs scheduled for publication within our v2.0 spec so please be prepared for us to add data nodes in our responses, however, we will not remove knowledge from previously published APIs.  #### A Current Response  ```javascript {   id: 123 } ```  #### A Potential Future Response  ```javascript {   id: 123,   reason: \"More Knowledge\" } ```  # Getting Started  We use OAuth v2.0 to authenticate clients, you can choose [implicit](https://oauth.net/2/grant-types/implicit/) or [password](https://oauth.net/2/grant-types/password/) grant type. To obtain an OAuth `client_id` and `client_secret` contact your account executive.  **Tip**: Generate an additional login and use those credentials for your integration so that changes are accredited to that \"user\".  You are now ready to make requests to our other APIs by filling your `Authorization` header with `Bearer {access_token}`.  ## Perpetuating Access  Perpetuating access to FDC without storing your password locally can be achieved using the `refresh_token` returned by [POST /oauth/access_token](#operation/generateToken).  A simple concept to achieve this is outlined below.  1. Your application/script will ask you for your `username` and `password`, your `client_id` and `client_secret` will be accessible via a DB or ENV. 2. [Request an access_token](#operation/generateToken)   + Your function should be capable of formatting your request for both a `grant_type` of \\\"password\\\" (step 1) and \\\"refresh_token\\\" (step 4). 3. Store the `access_token` and `refresh_token` so future requests can skip step 1 4. When the `access_token` expires request anew using your `refresh_token`, replace both tokens in local storage.  + If this fails you will have to revert to step 1.  Alternatively if you choose for your application/script to have access to your `username` and `password` you can skip step 4.  In all scenarios we recommend storing all credentials outside your codebase.  ## Date Time Definitions  We will report all date-time stamps using the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard. When using listing API's where fromDate and toDate are available note that both dates are inclusive while requiring the fromDate to be before or at the toDate.  ### The Fulfillment Process  Many steps are required to fulfill your order we report back to you three fundamental milestones inside the orders model.  * `recordedOn` When we received your order. This will never change.  * `dispatchDate` When the current iteration of your order was scheduled for fulfillment. This may change however it is an indicator that the physical process of fulfillment has begun and a tracking number has been **assigned** to your order. The tracking number **MAY CHANGE**. You will not be able to cancel an order once it has been dispatched. If you need to recall an order that has been dispatched please contact your account executive.  * `departDate` When we recorded your order passing our final inspection and placed with the carrier. At this point it is **safe to inform the consignee** of the tracking number as it will not change.  ## Evaluating Error Responses  We currently return two different error models, with and without context. All errors will include a `message` node while errors with `context` will include additional information designed to save you time when encountering highly probable errors. For example, when you send us a request to create a duplicate order, we will reject your request and the context will include the FDC order `id` so that you may record it for your records.  ### Without Context  New order with missing required fields.  | Header | Response | | ------ | -------- | | Status | `400 Bad Request` |  ```javascript {       \"message\": \"Invalid request body\" } ```  ### With Context  New order with duplicate `merchantOrderId`.  | Header | Response | | ------ | -------- | | Status | `409 Conflict` |  ```javascript {   \"message\": \"Duplicate Order\",   \"context\": {     \"id\": 123   } } ```  ## Status Codes  Codes are a concatenation of State, Stage, and Detail.  `^([0-9]{2})([0-9]{2})([0-9]{2})$`  | Code | State              | Stage    | Detail         | | ---- | ------------------ | -------- | -------------- | | 010101 | Processing Order | Recieved | Customer Order | | 010102 | Processing Order | Recieved | Recieved | | 010201 | Processing Order | Approved | | | 010301 | Processing Order | Hold | Merchant Stock | | 010302 | Processing Order | Hold | Merchant Funds | | 010303 | Processing Order | Hold | For Merchant | | 010304 | Processing Order | Hold | Oversized Shipment | | 010305 | Processing Order | Hold | Invalid Parent Order | | 010306 | Processing Order | Hold | Invalid Address | | 010307 | Processing Order | Hold | By Admin | | 010401 | Processing Order | Address Problem | Incomplete Address | | 010402 | Processing Order | Address Problem | Invalid Locality | | 010403 | Processing Order | Address Problem | Invalid Region | | 010404 | Processing Order | Address Problem | Address Not Found | | 010405 | Processing Order | Address Problem | Many Addresses Found | | 010406 | Processing Order | Address Problem | Invalid Postal Code | | 010407 | Processing Order | Address Problem | Country Not Mapped | | 010408 | Processing Order | Address Problem | Invalid Recipient Name | | 010409 | Processing Order | Address Problem | Bad UK Address | | 010410 | Processing Order | Address Problem | Invalid Address Line 1 or 2 | | 010501 | Processing Order | Sku Problem | Invalid SKU | | 010501 | Processing Order | Sku Problem | Child Order has Invalid SKUs | | 010601 | Processing Order | Facility Problem | Facility Not Mapped | | 010701 | Processing Order | Ship Method Problem | Unmapped Ship Method | | 010702 | Processing Order | Ship Method Problem | Unmapped Ship Cost | | 010703 | Processing Order | Ship Method Problem | Missing Ship Method | | 010704 | Processing Order | Ship Method Problem | Invalid Ship Method | | 010705 | Processing Order | Ship Method Problem | Order Weight Outside of Ship Method Weight | | 010801 | Processing Order | Inventory Problem | Insufficient Inventory In Facility | | 010802 | Processing Order | Inventory Problem | Issue Encountered During Inventory Adjustment | | 010901 | Processing Order | Released To WMS | Released | | 020101 | Fulfillment In Progress | Postage Problem | Address Issue | | 020102 | Fulfillment In Progress | Postage Problem | Postage OK, OMS Issue Occurred | | 020103 | Fulfillment In Progress | Postage Problem | Postage Void Failed | | 020201 | Fulfillment In Progress | Postage Acquired | | | 020301 | Fulfillment In Progress | Postage Voided | Postage Void Failed Gracefully | | 020301 | Fulfillment In Progress | Hold | Departure Hold Requested | | 020401 | Fulfillment In Progress | 4PL Processing | | | 020501 | Fulfillment In Progress | 4PL Problem | Order is Proccessable, Postage Issue Occurred | | 020601 | Fulfillment In Progress | Label Printed | | | 020701 | Fulfillment In Progress | Shipment Cubed | | | 020801 | Fulfillment In Progress | Picking Inventory | | | 020901 | Fulfillment In Progress | Label Print Verified | | | 021001 | Fulfillment In Progress | Passed Final Inspection | | | 030101 | Shipped | Fulfilled By 4PL | | | 030102 | Shipped | Fulfilled By 4PL | Successfully Fulfilled, OMS Encountered Issue During Processing | | 030201 | Shipped | Fulfilled By FDC | | | 040101 | Returned | Returned | | | 050101 | Cancelled | Cancelled | | | 060101 | Test | Test | Test |   # noqa: E501

    OpenAPI spec version: 2.0
    Contact: dev@fulfillment.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class OrdersApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_orders_id(self, id, **kwargs):  # noqa: E501
        """Cancel an Order  # noqa: E501

        Request an order is canceled to prevent shipment.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_orders_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: ID of order that needs to be canceled (required)
        :return: Paths1orderspostresponses201contentapplication1jsonschema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_orders_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_orders_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_orders_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """Cancel an Order  # noqa: E501

        Request an order is canceled to prevent shipment.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_orders_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: ID of order that needs to be canceled (required)
        :return: Paths1orderspostresponses201contentapplication1jsonschema
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_orders_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_orders_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['fdcAuth']  # noqa: E501

        return self.api_client.call_api(
            '/orders/{id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Paths1orderspostresponses201contentapplication1jsonschema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_order(self, id, **kwargs):  # noqa: E501
        """Order Details  # noqa: E501

        For the fastest results use the FDC provided `id` however you can use your `merchantOrderId` as the `id`.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_order(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The FDC order Id (required)
        :param int merchant_id: Providing your `merchantId` indicates the `id` is your `merchantOrderId`. Although it is not necessary to provide this it will speed up your results when using your `merchantOrderId` however it will slow your results when using the FDC provided `id`
        :param list[str] hydrate: Adds additional information to the response, uses a CSV format for multiple values.'
        :return: Paths1ordersgetresponses200contentapplication1jsonschema
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_order_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_order_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_order_with_http_info(self, id, **kwargs):  # noqa: E501
        """Order Details  # noqa: E501

        For the fastest results use the FDC provided `id` however you can use your `merchantOrderId` as the `id`.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_order_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: The FDC order Id (required)
        :param int merchant_id: Providing your `merchantId` indicates the `id` is your `merchantOrderId`. Although it is not necessary to provide this it will speed up your results when using your `merchantOrderId` however it will slow your results when using the FDC provided `id`
        :param list[str] hydrate: Adds additional information to the response, uses a CSV format for multiple values.'
        :return: Paths1ordersgetresponses200contentapplication1jsonschema
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'merchant_id', 'hydrate']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_order" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_order`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'merchant_id' in params:
            query_params.append(('merchantId', params['merchant_id']))  # noqa: E501
        if 'hydrate' in params:
            query_params.append(('hydrate', params['hydrate']))  # noqa: E501
            collection_formats['hydrate'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['fdcAuth']  # noqa: E501

        return self.api_client.call_api(
            '/orders/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Paths1ordersgetresponses200contentapplication1jsonschema',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_orders(self, from_date, to_date, **kwargs):  # noqa: E501
        """List of Orders  # noqa: E501

        Retrieve many orders at once  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_orders(from_date, to_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str from_date: Date-time in ISO 8601 format for selecting orders after, or at, the specified time (required)
        :param str to_date: Date-time in ISO 8601 format for selecting orders before, or at, the specified time (required)
        :param list[int] merchant_ids: A CSV of merchant id, '123' or '1,2,3'
        :param list[int] warehouse_ids: A CSV of warehouse id, '123' or '1,2,3'
        :param int page: A multiplier of the number of items (limit paramater) to skip before returning results
        :param int limit: The numbers of items to return
        :param list[str] hydrate: Adds additional information to the response, uses a CSV format for multiple values.'
        :return: OrderResponseOneOfV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_orders_with_http_info(from_date, to_date, **kwargs)  # noqa: E501
        else:
            (data) = self.get_orders_with_http_info(from_date, to_date, **kwargs)  # noqa: E501
            return data

    def get_orders_with_http_info(self, from_date, to_date, **kwargs):  # noqa: E501
        """List of Orders  # noqa: E501

        Retrieve many orders at once  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_orders_with_http_info(from_date, to_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str from_date: Date-time in ISO 8601 format for selecting orders after, or at, the specified time (required)
        :param str to_date: Date-time in ISO 8601 format for selecting orders before, or at, the specified time (required)
        :param list[int] merchant_ids: A CSV of merchant id, '123' or '1,2,3'
        :param list[int] warehouse_ids: A CSV of warehouse id, '123' or '1,2,3'
        :param int page: A multiplier of the number of items (limit paramater) to skip before returning results
        :param int limit: The numbers of items to return
        :param list[str] hydrate: Adds additional information to the response, uses a CSV format for multiple values.'
        :return: OrderResponseOneOfV2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['from_date', 'to_date', 'merchant_ids', 'warehouse_ids', 'page', 'limit', 'hydrate']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_orders" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'from_date' is set
        if ('from_date' not in params or
                params['from_date'] is None):
            raise ValueError("Missing the required parameter `from_date` when calling `get_orders`")  # noqa: E501
        # verify the required parameter 'to_date' is set
        if ('to_date' not in params or
                params['to_date'] is None):
            raise ValueError("Missing the required parameter `to_date` when calling `get_orders`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'from_date' in params:
            query_params.append(('fromDate', params['from_date']))  # noqa: E501
        if 'to_date' in params:
            query_params.append(('toDate', params['to_date']))  # noqa: E501
        if 'merchant_ids' in params:
            query_params.append(('merchantIds', params['merchant_ids']))  # noqa: E501
            collection_formats['merchantIds'] = 'csv'  # noqa: E501
        if 'warehouse_ids' in params:
            query_params.append(('warehouseIds', params['warehouse_ids']))  # noqa: E501
            collection_formats['warehouseIds'] = 'csv'  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'hydrate' in params:
            query_params.append(('hydrate', params['hydrate']))  # noqa: E501
            collection_formats['hydrate'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['fdcAuth']  # noqa: E501

        return self.api_client.call_api(
            '/orders', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OrderResponseOneOfV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_orders(self, body, **kwargs):  # noqa: E501
        """New Order  # noqa: E501

        Error Notes&#58; * When `409 Conflict` is a 'Duplicate Order' the `context` will include the FDC `id`, see samples.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_orders(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param OrderRequestV2 body: The order to create (required)
        :return: OrderResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_orders_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.post_orders_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def post_orders_with_http_info(self, body, **kwargs):  # noqa: E501
        """New Order  # noqa: E501

        Error Notes&#58; * When `409 Conflict` is a 'Duplicate Order' the `context` will include the FDC `id`, see samples.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_orders_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param OrderRequestV2 body: The order to create (required)
        :return: OrderResponseV2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_orders" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_orders`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['fdcAuth']  # noqa: E501

        return self.api_client.call_api(
            '/orders', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OrderResponseV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
