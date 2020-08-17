# coding: utf-8

"""
    Fulfillment.com APIv2

    Welcome to our current iteration of our REST API. While we encourage you to upgrade to v2.0 we will continue support for our [SOAP API](https://github.com/fulfillment/soap-integration).  # Versioning  The Fulfillment.com (FDC) REST API is version controlled and backwards compatible. We have many future APIs scheduled for publication within our v2.0 spec so please be prepared for us to add data nodes in our responses, however, we will not remove knowledge from previously published APIs.  #### A Current Response  ```javascript {   id: 123 } ```  #### A Potential Future Response  ```javascript {   id: 123,   reason: \"More Knowledge\" } ```  # Getting Started  We use OAuth v2.0 to authenticate clients, you can choose [implicit](https://oauth.net/2/grant-types/implicit/) or [password](https://oauth.net/2/grant-types/password/) grant type. To obtain an OAuth `client_id` and `client_secret` contact your account executive.  **Tip**: Generate an additional login and use those credentials for your integration so that changes are accredited to that \"user\".  You are now ready to make requests to our other APIs by filling your `Authorization` header with `Bearer {access_token}`.  ## Perpetuating Access  Perpetuating access to FDC without storing your password locally can be achieved using the `refresh_token` returned by [POST /oauth/access_token](#operation/generateToken).  A simple concept to achieve this is outlined below.  1. Your application/script will ask you for your `username` and `password`, your `client_id` and `client_secret` will be accessible via a DB or ENV. 2. [Request an access_token](#operation/generateToken)   + Your function should be capable of formatting your request for both a `grant_type` of \\\"password\\\" (step 1) and \\\"refresh_token\\\" (step 4). 3. Store the `access_token` and `refresh_token` so future requests can skip step 1 4. When the `access_token` expires request anew using your `refresh_token`, replace both tokens in local storage.  + If this fails you will have to revert to step 1.  Alternatively if you choose for your application/script to have access to your `username` and `password` you can skip step 4.  In all scenarios we recommend storing all credentials outside your codebase.  ## Date Time Definitions  We will report all date-time stamps using the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard. When using listing API's where fromDate and toDate are available note that both dates are inclusive while requiring the fromDate to be before or at the toDate.  ### The Fulfillment Process  Many steps are required to fulfill your order we report back to you three fundamental milestones inside the orders model.  * `recordedOn` When we received your order. This will never change.  * `dispatchDate` When the current iteration of your order was scheduled for fulfillment. This may change however it is an indicator that the physical process of fulfillment has begun and a tracking number has been **assigned** to your order. The tracking number **MAY CHANGE**. You will not be able to cancel an order once it has been dispatched. If you need to recall an order that has been dispatched please contact your account executive.  * `departDate` When we recorded your order passing our final inspection and placed with the carrier. At this point it is **safe to inform the consignee** of the tracking number as it will not change.  ## Evaluating Error Responses  We currently return two different error models, with and without context. All errors will include a `message` node while errors with `context` will include additional information designed to save you time when encountering highly probable errors. For example, when you send us a request to create a duplicate order, we will reject your request and the context will include the FDC order `id` so that you may record it for your records.  ### Without Context  New order with missing required fields.  | Header | Response | | ------ | -------- | | Status | `400 Bad Request` |  ```javascript {       \"message\": \"Invalid request body\" } ```  ### With Context  New order with duplicate `merchantOrderId`.  | Header | Response | | ------ | -------- | | Status | `409 Conflict` |  ```javascript {   \"message\": \"Duplicate Order\",   \"context\": {     \"id\": 123   } } ```  ## Status Codes  Codes are a concatenation of State, Stage, and Detail.  `^([0-9]{2})([0-9]{2})([0-9]{2})$`  | Code | State              | Stage    | Detail         | | ---- | ------------------ | -------- | -------------- | | 010101 | Processing Order | Recieved | Customer Order | | 010102 | Processing Order | Recieved | Recieved | | 010201 | Processing Order | Approved | | | 010301 | Processing Order | Hold | Merchant Stock | | 010302 | Processing Order | Hold | Merchant Funds | | 010303 | Processing Order | Hold | For Merchant | | 010304 | Processing Order | Hold | Oversized Shipment | | 010305 | Processing Order | Hold | Invalid Parent Order | | 010306 | Processing Order | Hold | Invalid Address | | 010307 | Processing Order | Hold | By Admin | | 010401 | Processing Order | Address Problem | Incomplete Address | | 010402 | Processing Order | Address Problem | Invalid Locality | | 010403 | Processing Order | Address Problem | Invalid Region | | 010404 | Processing Order | Address Problem | Address Not Found | | 010405 | Processing Order | Address Problem | Many Addresses Found | | 010406 | Processing Order | Address Problem | Invalid Postal Code | | 010407 | Processing Order | Address Problem | Country Not Mapped | | 010408 | Processing Order | Address Problem | Invalid Recipient Name | | 010409 | Processing Order | Address Problem | Bad UK Address | | 010410 | Processing Order | Address Problem | Invalid Address Line 1 or 2 | | 010501 | Processing Order | Sku Problem | Invalid SKU | | 010501 | Processing Order | Sku Problem | Child Order has Invalid SKUs | | 010601 | Processing Order | Facility Problem | Facility Not Mapped | | 010701 | Processing Order | Ship Method Problem | Unmapped Ship Method | | 010702 | Processing Order | Ship Method Problem | Unmapped Ship Cost | | 010703 | Processing Order | Ship Method Problem | Missing Ship Method | | 010704 | Processing Order | Ship Method Problem | Invalid Ship Method | | 010705 | Processing Order | Ship Method Problem | Order Weight Outside of Ship Method Weight | | 010801 | Processing Order | Inventory Problem | Insufficient Inventory In Facility | | 010802 | Processing Order | Inventory Problem | Issue Encountered During Inventory Adjustment | | 010901 | Processing Order | Released To WMS | Released | | 020101 | Fulfillment In Progress | Postage Problem | Address Issue | | 020102 | Fulfillment In Progress | Postage Problem | Postage OK, OMS Issue Occurred | | 020103 | Fulfillment In Progress | Postage Problem | Postage Void Failed | | 020201 | Fulfillment In Progress | Postage Acquired | | | 020301 | Fulfillment In Progress | Postage Voided | Postage Void Failed Gracefully | | 020301 | Fulfillment In Progress | Hold | Departure Hold Requested | | 020401 | Fulfillment In Progress | 4PL Processing | | | 020501 | Fulfillment In Progress | 4PL Problem | Order is Proccessable, Postage Issue Occurred | | 020601 | Fulfillment In Progress | Label Printed | | | 020701 | Fulfillment In Progress | Shipment Cubed | | | 020801 | Fulfillment In Progress | Picking Inventory | | | 020901 | Fulfillment In Progress | Label Print Verified | | | 021001 | Fulfillment In Progress | Passed Final Inspection | | | 030101 | Shipped | Fulfilled By 4PL | | | 030102 | Shipped | Fulfilled By 4PL | Successfully Fulfilled, OMS Encountered Issue During Processing | | 030201 | Shipped | Fulfilled By FDC | | | 040101 | Returned | Returned | | | 050101 | Cancelled | Cancelled | | | 060101 | Test | Test | Test |   # noqa: E501

    OpenAPI spec version: 2.0
    Contact: dev@fulfillment.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import io
import json
import logging
import re
import ssl

import certifi
# python 2 and python 3 compatibility library
import six
from six.moves.urllib.parse import urlencode

try:
    import urllib3
except ImportError:
    raise ImportError('Swagger python client requires urllib3.')


logger = logging.getLogger(__name__)


class RESTResponse(io.IOBase):

    def __init__(self, resp):
        self.urllib3_response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = resp.data

    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.urllib3_response.getheaders()

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.urllib3_response.getheader(name, default)


class RESTClientObject(object):

    def __init__(self, configuration, pools_size=4, maxsize=None):
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75  # noqa: E501
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680  # noqa: E501
        # maxsize is the number of requests to host that are allowed in parallel  # noqa: E501
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html  # noqa: E501

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        # ca_certs
        if configuration.ssl_ca_cert:
            ca_certs = configuration.ssl_ca_cert
        else:
            # if not set certificate file, use Mozilla's root certificates.
            ca_certs = certifi.where()

        addition_pool_args = {}
        if configuration.assert_hostname is not None:
            addition_pool_args['assert_hostname'] = configuration.assert_hostname  # noqa: E501

        if maxsize is None:
            if configuration.connection_pool_maxsize is not None:
                maxsize = configuration.connection_pool_maxsize
            else:
                maxsize = 4

        # https pool manager
        if configuration.proxy:
            self.pool_manager = urllib3.ProxyManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                proxy_url=configuration.proxy,
                **addition_pool_args
            )
        else:
            self.pool_manager = urllib3.PoolManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                **addition_pool_args
            )

    def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None, _preload_content=True,
                _request_timeout=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT',
                          'PATCH', 'OPTIONS']

        if post_params and body:
            raise ValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, ) if six.PY3 else (int, long)):  # noqa: E501,F821
                timeout = urllib3.Timeout(total=_request_timeout)
            elif (isinstance(_request_timeout, tuple) and
                  len(_request_timeout) == 2):
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0], read=_request_timeout[1])

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if query_params:
                    url += '?' + urlencode(query_params)
                if re.search('json', headers['Content-Type'], re.IGNORECASE):
                    request_body = '{}'
                    if body is not None:
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'application/x-www-form-urlencoded':  # noqa: E501
                    r = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=False,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'multipart/form-data':
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers['Content-Type']
                    r = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=True,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                # Pass a `string` parameter directly in the body to support
                # other content types than Json when `body` argument is
                # provided in serialized form
                elif isinstance(body, str):
                    request_body = body
                    r = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                r = self.pool_manager.request(method, url,
                                              fields=query_params,
                                              preload_content=_preload_content,
                                              timeout=timeout,
                                              headers=headers)
        except urllib3.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        if _preload_content:
            r = RESTResponse(r)

            # In the python 3, the response.data is bytes.
            # we need to decode it to string.
            if six.PY3:
                r.data = r.data.decode('utf8')

            # log response body
            logger.debug("response body: %s", r.data)

        if not 200 <= r.status <= 299:
            raise ApiException(http_resp=r)

        return r

    def GET(self, url, headers=None, query_params=None, _preload_content=True,
            _request_timeout=None):
        return self.request("GET", url,
                            headers=headers,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            query_params=query_params)

    def HEAD(self, url, headers=None, query_params=None, _preload_content=True,
             _request_timeout=None):
        return self.request("HEAD", url,
                            headers=headers,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            query_params=query_params)

    def OPTIONS(self, url, headers=None, query_params=None, post_params=None,
                body=None, _preload_content=True, _request_timeout=None):
        return self.request("OPTIONS", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def DELETE(self, url, headers=None, query_params=None, body=None,
               _preload_content=True, _request_timeout=None):
        return self.request("DELETE", url,
                            headers=headers,
                            query_params=query_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def POST(self, url, headers=None, query_params=None, post_params=None,
             body=None, _preload_content=True, _request_timeout=None):
        return self.request("POST", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def PUT(self, url, headers=None, query_params=None, post_params=None,
            body=None, _preload_content=True, _request_timeout=None):
        return self.request("PUT", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def PATCH(self, url, headers=None, query_params=None, post_params=None,
              body=None, _preload_content=True, _request_timeout=None):
        return self.request("PATCH", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
