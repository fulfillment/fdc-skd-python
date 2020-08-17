# coding: utf-8

"""
    Fulfillment.com APIv2

    Welcome to our current iteration of our REST API. While we encourage you to upgrade to v2.0 we will continue support for our [SOAP API](https://github.com/fulfillment/soap-integration).  # Versioning  The Fulfillment.com (FDC) REST API is version controlled and backwards compatible. We have many future APIs scheduled for publication within our v2.0 spec so please be prepared for us to add data nodes in our responses, however, we will not remove knowledge from previously published APIs.  #### A Current Response  ```javascript {   id: 123 } ```  #### A Potential Future Response  ```javascript {   id: 123,   reason: \"More Knowledge\" } ```  # Getting Started  We use OAuth v2.0 to authenticate clients, you can choose [implicit](https://oauth.net/2/grant-types/implicit/) or [password](https://oauth.net/2/grant-types/password/) grant type. To obtain an OAuth `client_id` and `client_secret` contact your account executive.  **Tip**: Generate an additional login and use those credentials for your integration so that changes are accredited to that \"user\".  You are now ready to make requests to our other APIs by filling your `Authorization` header with `Bearer {access_token}`.  ## Perpetuating Access  Perpetuating access to FDC without storing your password locally can be achieved using the `refresh_token` returned by [POST /oauth/access_token](#operation/generateToken).  A simple concept to achieve this is outlined below.  1. Your application/script will ask you for your `username` and `password`, your `client_id` and `client_secret` will be accessible via a DB or ENV. 2. [Request an access_token](#operation/generateToken)   + Your function should be capable of formatting your request for both a `grant_type` of \\\"password\\\" (step 1) and \\\"refresh_token\\\" (step 4). 3. Store the `access_token` and `refresh_token` so future requests can skip step 1 4. When the `access_token` expires request anew using your `refresh_token`, replace both tokens in local storage.  + If this fails you will have to revert to step 1.  Alternatively if you choose for your application/script to have access to your `username` and `password` you can skip step 4.  In all scenarios we recommend storing all credentials outside your codebase.  ## Date Time Definitions  We will report all date-time stamps using the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard. When using listing API's where fromDate and toDate are available note that both dates are inclusive while requiring the fromDate to be before or at the toDate.  ### The Fulfillment Process  Many steps are required to fulfill your order we report back to you three fundamental milestones inside the orders model.  * `recordedOn` When we received your order. This will never change.  * `dispatchDate` When the current iteration of your order was scheduled for fulfillment. This may change however it is an indicator that the physical process of fulfillment has begun and a tracking number has been **assigned** to your order. The tracking number **MAY CHANGE**. You will not be able to cancel an order once it has been dispatched. If you need to recall an order that has been dispatched please contact your account executive.  * `departDate` When we recorded your order passing our final inspection and placed with the carrier. At this point it is **safe to inform the consignee** of the tracking number as it will not change.  ## Evaluating Error Responses  We currently return two different error models, with and without context. All errors will include a `message` node while errors with `context` will include additional information designed to save you time when encountering highly probable errors. For example, when you send us a request to create a duplicate order, we will reject your request and the context will include the FDC order `id` so that you may record it for your records.  ### Without Context  New order with missing required fields.  | Header | Response | | ------ | -------- | | Status | `400 Bad Request` |  ```javascript {       \"message\": \"Invalid request body\" } ```  ### With Context  New order with duplicate `merchantOrderId`.  | Header | Response | | ------ | -------- | | Status | `409 Conflict` |  ```javascript {   \"message\": \"Duplicate Order\",   \"context\": {     \"id\": 123   } } ```  ## Status Codes  Codes are a concatenation of State, Stage, and Detail.  `^([0-9]{2})([0-9]{2})([0-9]{2})$`  | Code | State              | Stage    | Detail         | | ---- | ------------------ | -------- | -------------- | | 010101 | Processing Order | Recieved | Customer Order | | 010102 | Processing Order | Recieved | Recieved | | 010201 | Processing Order | Approved | | | 010301 | Processing Order | Hold | Merchant Stock | | 010302 | Processing Order | Hold | Merchant Funds | | 010303 | Processing Order | Hold | For Merchant | | 010304 | Processing Order | Hold | Oversized Shipment | | 010305 | Processing Order | Hold | Invalid Parent Order | | 010306 | Processing Order | Hold | Invalid Address | | 010307 | Processing Order | Hold | By Admin | | 010401 | Processing Order | Address Problem | Incomplete Address | | 010402 | Processing Order | Address Problem | Invalid Locality | | 010403 | Processing Order | Address Problem | Invalid Region | | 010404 | Processing Order | Address Problem | Address Not Found | | 010405 | Processing Order | Address Problem | Many Addresses Found | | 010406 | Processing Order | Address Problem | Invalid Postal Code | | 010407 | Processing Order | Address Problem | Country Not Mapped | | 010408 | Processing Order | Address Problem | Invalid Recipient Name | | 010409 | Processing Order | Address Problem | Bad UK Address | | 010410 | Processing Order | Address Problem | Invalid Address Line 1 or 2 | | 010501 | Processing Order | Sku Problem | Invalid SKU | | 010501 | Processing Order | Sku Problem | Child Order has Invalid SKUs | | 010601 | Processing Order | Facility Problem | Facility Not Mapped | | 010701 | Processing Order | Ship Method Problem | Unmapped Ship Method | | 010702 | Processing Order | Ship Method Problem | Unmapped Ship Cost | | 010703 | Processing Order | Ship Method Problem | Missing Ship Method | | 010704 | Processing Order | Ship Method Problem | Invalid Ship Method | | 010705 | Processing Order | Ship Method Problem | Order Weight Outside of Ship Method Weight | | 010801 | Processing Order | Inventory Problem | Insufficient Inventory In Facility | | 010802 | Processing Order | Inventory Problem | Issue Encountered During Inventory Adjustment | | 010901 | Processing Order | Released To WMS | Released | | 020101 | Fulfillment In Progress | Postage Problem | Address Issue | | 020102 | Fulfillment In Progress | Postage Problem | Postage OK, OMS Issue Occurred | | 020103 | Fulfillment In Progress | Postage Problem | Postage Void Failed | | 020201 | Fulfillment In Progress | Postage Acquired | | | 020301 | Fulfillment In Progress | Postage Voided | Postage Void Failed Gracefully | | 020301 | Fulfillment In Progress | Hold | Departure Hold Requested | | 020401 | Fulfillment In Progress | 4PL Processing | | | 020501 | Fulfillment In Progress | 4PL Problem | Order is Proccessable, Postage Issue Occurred | | 020601 | Fulfillment In Progress | Label Printed | | | 020701 | Fulfillment In Progress | Shipment Cubed | | | 020801 | Fulfillment In Progress | Picking Inventory | | | 020901 | Fulfillment In Progress | Label Print Verified | | | 021001 | Fulfillment In Progress | Passed Final Inspection | | | 030101 | Shipped | Fulfilled By 4PL | | | 030102 | Shipped | Fulfilled By 4PL | Successfully Fulfilled, OMS Encountered Issue During Processing | | 030201 | Shipped | Fulfilled By FDC | | | 040101 | Returned | Returned | | | 050101 | Cancelled | Cancelled | | | 060101 | Test | Test | Test |   # noqa: E501

    OpenAPI spec version: 2.0
    Contact: dev@fulfillment.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TrackingEventV2(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'event_source': 'str',
        'event_location': 'Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin',
        'event_date_time': 'datetime',
        'event_category_code': 'int',
        'event_category': 'str',
        'event_status': 'str'
    }

    attribute_map = {
        'event_source': 'eventSource',
        'event_location': 'eventLocation',
        'event_date_time': 'eventDateTime',
        'event_category_code': 'eventCategoryCode',
        'event_category': 'eventCategory',
        'event_status': 'eventStatus'
    }

    def __init__(self, event_source=None, event_location=None, event_date_time=None, event_category_code=None, event_category=None, event_status=None):  # noqa: E501
        """TrackingEventV2 - a model defined in Swagger"""  # noqa: E501
        self._event_source = None
        self._event_location = None
        self._event_date_time = None
        self._event_category_code = None
        self._event_category = None
        self._event_status = None
        self.discriminator = None
        if event_source is not None:
            self.event_source = event_source
        if event_location is not None:
            self.event_location = event_location
        if event_date_time is not None:
            self.event_date_time = event_date_time
        if event_category_code is not None:
            self.event_category_code = event_category_code
        if event_category is not None:
            self.event_category = event_category
        if event_status is not None:
            self.event_status = event_status

    @property
    def event_source(self):
        """Gets the event_source of this TrackingEventV2.  # noqa: E501


        :return: The event_source of this TrackingEventV2.  # noqa: E501
        :rtype: str
        """
        return self._event_source

    @event_source.setter
    def event_source(self, event_source):
        """Sets the event_source of this TrackingEventV2.


        :param event_source: The event_source of this TrackingEventV2.  # noqa: E501
        :type: str
        """
        allowed_values = ["carrier", "internal"]  # noqa: E501
        if event_source not in allowed_values:
            raise ValueError(
                "Invalid value for `event_source` ({0}), must be one of {1}"  # noqa: E501
                .format(event_source, allowed_values)
            )

        self._event_source = event_source

    @property
    def event_location(self):
        """Gets the event_location of this TrackingEventV2.  # noqa: E501


        :return: The event_location of this TrackingEventV2.  # noqa: E501
        :rtype: Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin
        """
        return self._event_location

    @event_location.setter
    def event_location(self, event_location):
        """Sets the event_location of this TrackingEventV2.


        :param event_location: The event_location of this TrackingEventV2.  # noqa: E501
        :type: Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin
        """

        self._event_location = event_location

    @property
    def event_date_time(self):
        """Gets the event_date_time of this TrackingEventV2.  # noqa: E501


        :return: The event_date_time of this TrackingEventV2.  # noqa: E501
        :rtype: datetime
        """
        return self._event_date_time

    @event_date_time.setter
    def event_date_time(self, event_date_time):
        """Sets the event_date_time of this TrackingEventV2.


        :param event_date_time: The event_date_time of this TrackingEventV2.  # noqa: E501
        :type: datetime
        """

        self._event_date_time = event_date_time

    @property
    def event_category_code(self):
        """Gets the event_category_code of this TrackingEventV2.  # noqa: E501


        :return: The event_category_code of this TrackingEventV2.  # noqa: E501
        :rtype: int
        """
        return self._event_category_code

    @event_category_code.setter
    def event_category_code(self, event_category_code):
        """Sets the event_category_code of this TrackingEventV2.


        :param event_category_code: The event_category_code of this TrackingEventV2.  # noqa: E501
        :type: int
        """

        self._event_category_code = event_category_code

    @property
    def event_category(self):
        """Gets the event_category of this TrackingEventV2.  # noqa: E501


        :return: The event_category of this TrackingEventV2.  # noqa: E501
        :rtype: str
        """
        return self._event_category

    @event_category.setter
    def event_category(self, event_category):
        """Sets the event_category of this TrackingEventV2.


        :param event_category: The event_category of this TrackingEventV2.  # noqa: E501
        :type: str
        """

        self._event_category = event_category

    @property
    def event_status(self):
        """Gets the event_status of this TrackingEventV2.  # noqa: E501


        :return: The event_status of this TrackingEventV2.  # noqa: E501
        :rtype: str
        """
        return self._event_status

    @event_status.setter
    def event_status(self, event_status):
        """Sets the event_status of this TrackingEventV2.


        :param event_status: The event_status of this TrackingEventV2.  # noqa: E501
        :type: str
        """

        self._event_status = event_status

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TrackingEventV2, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TrackingEventV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
