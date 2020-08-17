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

class TrackingResponse(object):
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
        'tracked_events': 'list[TrackingEventV2]',
        'fdc_order_id': 'int',
        'first_transit_event': 'datetime',
        'last_updated_date_time': 'datetime',
        'last_checked_date_time': 'datetime',
        'first_checked_date_time': 'datetime',
        'status_message': 'str',
        'status_category_code': 'int',
        'status_date_time': 'datetime',
        'status': 'str',
        'destination': 'Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin',
        'origin': 'Feature',
        'tracking_number': 'TrackingNumberV2'
    }

    attribute_map = {
        'tracked_events': 'trackedEvents',
        'fdc_order_id': 'fdcOrderId',
        'first_transit_event': 'firstTransitEvent',
        'last_updated_date_time': 'lastUpdatedDateTime',
        'last_checked_date_time': 'lastCheckedDateTime',
        'first_checked_date_time': 'firstCheckedDateTime',
        'status_message': 'statusMessage',
        'status_category_code': 'statusCategoryCode',
        'status_date_time': 'statusDateTime',
        'status': 'status',
        'destination': 'destination',
        'origin': 'origin',
        'tracking_number': 'trackingNumber'
    }

    def __init__(self, tracked_events=None, fdc_order_id=None, first_transit_event=None, last_updated_date_time=None, last_checked_date_time=None, first_checked_date_time=None, status_message=None, status_category_code=None, status_date_time=None, status=None, destination=None, origin=None, tracking_number=None):  # noqa: E501
        """TrackingResponse - a model defined in Swagger"""  # noqa: E501
        self._tracked_events = None
        self._fdc_order_id = None
        self._first_transit_event = None
        self._last_updated_date_time = None
        self._last_checked_date_time = None
        self._first_checked_date_time = None
        self._status_message = None
        self._status_category_code = None
        self._status_date_time = None
        self._status = None
        self._destination = None
        self._origin = None
        self._tracking_number = None
        self.discriminator = None
        if tracked_events is not None:
            self.tracked_events = tracked_events
        if fdc_order_id is not None:
            self.fdc_order_id = fdc_order_id
        if first_transit_event is not None:
            self.first_transit_event = first_transit_event
        if last_updated_date_time is not None:
            self.last_updated_date_time = last_updated_date_time
        if last_checked_date_time is not None:
            self.last_checked_date_time = last_checked_date_time
        if first_checked_date_time is not None:
            self.first_checked_date_time = first_checked_date_time
        if status_message is not None:
            self.status_message = status_message
        if status_category_code is not None:
            self.status_category_code = status_category_code
        if status_date_time is not None:
            self.status_date_time = status_date_time
        if status is not None:
            self.status = status
        if destination is not None:
            self.destination = destination
        if origin is not None:
            self.origin = origin
        if tracking_number is not None:
            self.tracking_number = tracking_number

    @property
    def tracked_events(self):
        """Gets the tracked_events of this TrackingResponse.  # noqa: E501


        :return: The tracked_events of this TrackingResponse.  # noqa: E501
        :rtype: list[TrackingEventV2]
        """
        return self._tracked_events

    @tracked_events.setter
    def tracked_events(self, tracked_events):
        """Sets the tracked_events of this TrackingResponse.


        :param tracked_events: The tracked_events of this TrackingResponse.  # noqa: E501
        :type: list[TrackingEventV2]
        """

        self._tracked_events = tracked_events

    @property
    def fdc_order_id(self):
        """Gets the fdc_order_id of this TrackingResponse.  # noqa: E501


        :return: The fdc_order_id of this TrackingResponse.  # noqa: E501
        :rtype: int
        """
        return self._fdc_order_id

    @fdc_order_id.setter
    def fdc_order_id(self, fdc_order_id):
        """Sets the fdc_order_id of this TrackingResponse.


        :param fdc_order_id: The fdc_order_id of this TrackingResponse.  # noqa: E501
        :type: int
        """

        self._fdc_order_id = fdc_order_id

    @property
    def first_transit_event(self):
        """Gets the first_transit_event of this TrackingResponse.  # noqa: E501


        :return: The first_transit_event of this TrackingResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._first_transit_event

    @first_transit_event.setter
    def first_transit_event(self, first_transit_event):
        """Sets the first_transit_event of this TrackingResponse.


        :param first_transit_event: The first_transit_event of this TrackingResponse.  # noqa: E501
        :type: datetime
        """

        self._first_transit_event = first_transit_event

    @property
    def last_updated_date_time(self):
        """Gets the last_updated_date_time of this TrackingResponse.  # noqa: E501


        :return: The last_updated_date_time of this TrackingResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._last_updated_date_time

    @last_updated_date_time.setter
    def last_updated_date_time(self, last_updated_date_time):
        """Sets the last_updated_date_time of this TrackingResponse.


        :param last_updated_date_time: The last_updated_date_time of this TrackingResponse.  # noqa: E501
        :type: datetime
        """

        self._last_updated_date_time = last_updated_date_time

    @property
    def last_checked_date_time(self):
        """Gets the last_checked_date_time of this TrackingResponse.  # noqa: E501


        :return: The last_checked_date_time of this TrackingResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._last_checked_date_time

    @last_checked_date_time.setter
    def last_checked_date_time(self, last_checked_date_time):
        """Sets the last_checked_date_time of this TrackingResponse.


        :param last_checked_date_time: The last_checked_date_time of this TrackingResponse.  # noqa: E501
        :type: datetime
        """

        self._last_checked_date_time = last_checked_date_time

    @property
    def first_checked_date_time(self):
        """Gets the first_checked_date_time of this TrackingResponse.  # noqa: E501


        :return: The first_checked_date_time of this TrackingResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._first_checked_date_time

    @first_checked_date_time.setter
    def first_checked_date_time(self, first_checked_date_time):
        """Sets the first_checked_date_time of this TrackingResponse.


        :param first_checked_date_time: The first_checked_date_time of this TrackingResponse.  # noqa: E501
        :type: datetime
        """

        self._first_checked_date_time = first_checked_date_time

    @property
    def status_message(self):
        """Gets the status_message of this TrackingResponse.  # noqa: E501


        :return: The status_message of this TrackingResponse.  # noqa: E501
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """Sets the status_message of this TrackingResponse.


        :param status_message: The status_message of this TrackingResponse.  # noqa: E501
        :type: str
        """

        self._status_message = status_message

    @property
    def status_category_code(self):
        """Gets the status_category_code of this TrackingResponse.  # noqa: E501


        :return: The status_category_code of this TrackingResponse.  # noqa: E501
        :rtype: int
        """
        return self._status_category_code

    @status_category_code.setter
    def status_category_code(self, status_category_code):
        """Sets the status_category_code of this TrackingResponse.


        :param status_category_code: The status_category_code of this TrackingResponse.  # noqa: E501
        :type: int
        """

        self._status_category_code = status_category_code

    @property
    def status_date_time(self):
        """Gets the status_date_time of this TrackingResponse.  # noqa: E501


        :return: The status_date_time of this TrackingResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._status_date_time

    @status_date_time.setter
    def status_date_time(self, status_date_time):
        """Sets the status_date_time of this TrackingResponse.


        :param status_date_time: The status_date_time of this TrackingResponse.  # noqa: E501
        :type: datetime
        """

        self._status_date_time = status_date_time

    @property
    def status(self):
        """Gets the status of this TrackingResponse.  # noqa: E501


        :return: The status of this TrackingResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TrackingResponse.


        :param status: The status of this TrackingResponse.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def destination(self):
        """Gets the destination of this TrackingResponse.  # noqa: E501


        :return: The destination of this TrackingResponse.  # noqa: E501
        :rtype: Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this TrackingResponse.


        :param destination: The destination of this TrackingResponse.  # noqa: E501
        :type: Paths1trackgetresponses200contentapplication1jsonschemapropertiesorigin
        """

        self._destination = destination

    @property
    def origin(self):
        """Gets the origin of this TrackingResponse.  # noqa: E501


        :return: The origin of this TrackingResponse.  # noqa: E501
        :rtype: Feature
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this TrackingResponse.


        :param origin: The origin of this TrackingResponse.  # noqa: E501
        :type: Feature
        """

        self._origin = origin

    @property
    def tracking_number(self):
        """Gets the tracking_number of this TrackingResponse.  # noqa: E501


        :return: The tracking_number of this TrackingResponse.  # noqa: E501
        :rtype: TrackingNumberV2
        """
        return self._tracking_number

    @tracking_number.setter
    def tracking_number(self, tracking_number):
        """Sets the tracking_number of this TrackingResponse.


        :param tracking_number: The tracking_number of this TrackingResponse.  # noqa: E501
        :type: TrackingNumberV2
        """

        self._tracking_number = tracking_number

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
        if issubclass(TrackingResponse, dict):
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
        if not isinstance(other, TrackingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
