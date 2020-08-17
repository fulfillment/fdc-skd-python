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

class OrderResponseV2(object):
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
        'id': 'int',
        'tracking_numbers': 'list[TrackingNumberV2]',
        'validated_consignee': 'Paths1orderspostresponses201contentapplication1jsonschemapropertiesoriginalConsignee',
        'original_consignee': 'ConsigneeV21',
        'current_status': 'StatusEventV2',
        'warehouse': 'UserV2',
        'merchant': 'MerchantV2',
        'depart_date': 'datetime',
        'dispatch_date': 'datetime',
        'recorded_on': 'datetime',
        'merchant_shipping_method': 'str',
        'purchase_order_num': 'str',
        'merchant_order_id': 'str',
        'parent_order': 'OrderResponseV2ParentOrder'
    }

    attribute_map = {
        'id': 'id',
        'tracking_numbers': 'trackingNumbers',
        'validated_consignee': 'validatedConsignee',
        'original_consignee': 'originalConsignee',
        'current_status': 'currentStatus',
        'warehouse': 'warehouse',
        'merchant': 'merchant',
        'depart_date': 'departDate',
        'dispatch_date': 'dispatchDate',
        'recorded_on': 'recordedOn',
        'merchant_shipping_method': 'merchantShippingMethod',
        'purchase_order_num': 'purchaseOrderNum',
        'merchant_order_id': 'merchantOrderId',
        'parent_order': 'parentOrder'
    }

    def __init__(self, id=None, tracking_numbers=None, validated_consignee=None, original_consignee=None, current_status=None, warehouse=None, merchant=None, depart_date=None, dispatch_date=None, recorded_on=None, merchant_shipping_method=None, purchase_order_num=None, merchant_order_id=None, parent_order=None):  # noqa: E501
        """OrderResponseV2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._tracking_numbers = None
        self._validated_consignee = None
        self._original_consignee = None
        self._current_status = None
        self._warehouse = None
        self._merchant = None
        self._depart_date = None
        self._dispatch_date = None
        self._recorded_on = None
        self._merchant_shipping_method = None
        self._purchase_order_num = None
        self._merchant_order_id = None
        self._parent_order = None
        self.discriminator = None
        self.id = id
        if tracking_numbers is not None:
            self.tracking_numbers = tracking_numbers
        self.validated_consignee = validated_consignee
        self.original_consignee = original_consignee
        self.current_status = current_status
        if warehouse is not None:
            self.warehouse = warehouse
        self.merchant = merchant
        if depart_date is not None:
            self.depart_date = depart_date
        if dispatch_date is not None:
            self.dispatch_date = dispatch_date
        self.recorded_on = recorded_on
        self.merchant_shipping_method = merchant_shipping_method
        if purchase_order_num is not None:
            self.purchase_order_num = purchase_order_num
        self.merchant_order_id = merchant_order_id
        if parent_order is not None:
            self.parent_order = parent_order

    @property
    def id(self):
        """Gets the id of this OrderResponseV2.  # noqa: E501

        FDC ID for this order  # noqa: E501

        :return: The id of this OrderResponseV2.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrderResponseV2.

        FDC ID for this order  # noqa: E501

        :param id: The id of this OrderResponseV2.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def tracking_numbers(self):
        """Gets the tracking_numbers of this OrderResponseV2.  # noqa: E501


        :return: The tracking_numbers of this OrderResponseV2.  # noqa: E501
        :rtype: list[TrackingNumberV2]
        """
        return self._tracking_numbers

    @tracking_numbers.setter
    def tracking_numbers(self, tracking_numbers):
        """Sets the tracking_numbers of this OrderResponseV2.


        :param tracking_numbers: The tracking_numbers of this OrderResponseV2.  # noqa: E501
        :type: list[TrackingNumberV2]
        """

        self._tracking_numbers = tracking_numbers

    @property
    def validated_consignee(self):
        """Gets the validated_consignee of this OrderResponseV2.  # noqa: E501


        :return: The validated_consignee of this OrderResponseV2.  # noqa: E501
        :rtype: Paths1orderspostresponses201contentapplication1jsonschemapropertiesoriginalConsignee
        """
        return self._validated_consignee

    @validated_consignee.setter
    def validated_consignee(self, validated_consignee):
        """Sets the validated_consignee of this OrderResponseV2.


        :param validated_consignee: The validated_consignee of this OrderResponseV2.  # noqa: E501
        :type: Paths1orderspostresponses201contentapplication1jsonschemapropertiesoriginalConsignee
        """
        if validated_consignee is None:
            raise ValueError("Invalid value for `validated_consignee`, must not be `None`")  # noqa: E501

        self._validated_consignee = validated_consignee

    @property
    def original_consignee(self):
        """Gets the original_consignee of this OrderResponseV2.  # noqa: E501


        :return: The original_consignee of this OrderResponseV2.  # noqa: E501
        :rtype: ConsigneeV21
        """
        return self._original_consignee

    @original_consignee.setter
    def original_consignee(self, original_consignee):
        """Sets the original_consignee of this OrderResponseV2.


        :param original_consignee: The original_consignee of this OrderResponseV2.  # noqa: E501
        :type: ConsigneeV21
        """
        if original_consignee is None:
            raise ValueError("Invalid value for `original_consignee`, must not be `None`")  # noqa: E501

        self._original_consignee = original_consignee

    @property
    def current_status(self):
        """Gets the current_status of this OrderResponseV2.  # noqa: E501


        :return: The current_status of this OrderResponseV2.  # noqa: E501
        :rtype: StatusEventV2
        """
        return self._current_status

    @current_status.setter
    def current_status(self, current_status):
        """Sets the current_status of this OrderResponseV2.


        :param current_status: The current_status of this OrderResponseV2.  # noqa: E501
        :type: StatusEventV2
        """
        if current_status is None:
            raise ValueError("Invalid value for `current_status`, must not be `None`")  # noqa: E501

        self._current_status = current_status

    @property
    def warehouse(self):
        """Gets the warehouse of this OrderResponseV2.  # noqa: E501


        :return: The warehouse of this OrderResponseV2.  # noqa: E501
        :rtype: UserV2
        """
        return self._warehouse

    @warehouse.setter
    def warehouse(self, warehouse):
        """Sets the warehouse of this OrderResponseV2.


        :param warehouse: The warehouse of this OrderResponseV2.  # noqa: E501
        :type: UserV2
        """

        self._warehouse = warehouse

    @property
    def merchant(self):
        """Gets the merchant of this OrderResponseV2.  # noqa: E501


        :return: The merchant of this OrderResponseV2.  # noqa: E501
        :rtype: MerchantV2
        """
        return self._merchant

    @merchant.setter
    def merchant(self, merchant):
        """Sets the merchant of this OrderResponseV2.


        :param merchant: The merchant of this OrderResponseV2.  # noqa: E501
        :type: MerchantV2
        """
        if merchant is None:
            raise ValueError("Invalid value for `merchant`, must not be `None`")  # noqa: E501

        self._merchant = merchant

    @property
    def depart_date(self):
        """Gets the depart_date of this OrderResponseV2.  # noqa: E501

        DateTime order departed an FDC warehouse  # noqa: E501

        :return: The depart_date of this OrderResponseV2.  # noqa: E501
        :rtype: datetime
        """
        return self._depart_date

    @depart_date.setter
    def depart_date(self, depart_date):
        """Sets the depart_date of this OrderResponseV2.

        DateTime order departed an FDC warehouse  # noqa: E501

        :param depart_date: The depart_date of this OrderResponseV2.  # noqa: E501
        :type: datetime
        """

        self._depart_date = depart_date

    @property
    def dispatch_date(self):
        """Gets the dispatch_date of this OrderResponseV2.  # noqa: E501

        DateTime order was dispatched for fulfillment by FDC  # noqa: E501

        :return: The dispatch_date of this OrderResponseV2.  # noqa: E501
        :rtype: datetime
        """
        return self._dispatch_date

    @dispatch_date.setter
    def dispatch_date(self, dispatch_date):
        """Sets the dispatch_date of this OrderResponseV2.

        DateTime order was dispatched for fulfillment by FDC  # noqa: E501

        :param dispatch_date: The dispatch_date of this OrderResponseV2.  # noqa: E501
        :type: datetime
        """

        self._dispatch_date = dispatch_date

    @property
    def recorded_on(self):
        """Gets the recorded_on of this OrderResponseV2.  # noqa: E501

        DateTime order was recorded by FDC  # noqa: E501

        :return: The recorded_on of this OrderResponseV2.  # noqa: E501
        :rtype: datetime
        """
        return self._recorded_on

    @recorded_on.setter
    def recorded_on(self, recorded_on):
        """Sets the recorded_on of this OrderResponseV2.

        DateTime order was recorded by FDC  # noqa: E501

        :param recorded_on: The recorded_on of this OrderResponseV2.  # noqa: E501
        :type: datetime
        """
        if recorded_on is None:
            raise ValueError("Invalid value for `recorded_on`, must not be `None`")  # noqa: E501

        self._recorded_on = recorded_on

    @property
    def merchant_shipping_method(self):
        """Gets the merchant_shipping_method of this OrderResponseV2.  # noqa: E501

        Requested ship method  # noqa: E501

        :return: The merchant_shipping_method of this OrderResponseV2.  # noqa: E501
        :rtype: str
        """
        return self._merchant_shipping_method

    @merchant_shipping_method.setter
    def merchant_shipping_method(self, merchant_shipping_method):
        """Sets the merchant_shipping_method of this OrderResponseV2.

        Requested ship method  # noqa: E501

        :param merchant_shipping_method: The merchant_shipping_method of this OrderResponseV2.  # noqa: E501
        :type: str
        """
        if merchant_shipping_method is None:
            raise ValueError("Invalid value for `merchant_shipping_method`, must not be `None`")  # noqa: E501

        self._merchant_shipping_method = merchant_shipping_method

    @property
    def purchase_order_num(self):
        """Gets the purchase_order_num of this OrderResponseV2.  # noqa: E501

        Merchant provided PO#  # noqa: E501

        :return: The purchase_order_num of this OrderResponseV2.  # noqa: E501
        :rtype: str
        """
        return self._purchase_order_num

    @purchase_order_num.setter
    def purchase_order_num(self, purchase_order_num):
        """Sets the purchase_order_num of this OrderResponseV2.

        Merchant provided PO#  # noqa: E501

        :param purchase_order_num: The purchase_order_num of this OrderResponseV2.  # noqa: E501
        :type: str
        """

        self._purchase_order_num = purchase_order_num

    @property
    def merchant_order_id(self):
        """Gets the merchant_order_id of this OrderResponseV2.  # noqa: E501

        Merchant provided ID  # noqa: E501

        :return: The merchant_order_id of this OrderResponseV2.  # noqa: E501
        :rtype: str
        """
        return self._merchant_order_id

    @merchant_order_id.setter
    def merchant_order_id(self, merchant_order_id):
        """Sets the merchant_order_id of this OrderResponseV2.

        Merchant provided ID  # noqa: E501

        :param merchant_order_id: The merchant_order_id of this OrderResponseV2.  # noqa: E501
        :type: str
        """
        if merchant_order_id is None:
            raise ValueError("Invalid value for `merchant_order_id`, must not be `None`")  # noqa: E501

        self._merchant_order_id = merchant_order_id

    @property
    def parent_order(self):
        """Gets the parent_order of this OrderResponseV2.  # noqa: E501


        :return: The parent_order of this OrderResponseV2.  # noqa: E501
        :rtype: OrderResponseV2ParentOrder
        """
        return self._parent_order

    @parent_order.setter
    def parent_order(self, parent_order):
        """Sets the parent_order of this OrderResponseV2.


        :param parent_order: The parent_order of this OrderResponseV2.  # noqa: E501
        :type: OrderResponseV2ParentOrder
        """

        self._parent_order = parent_order

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
        if issubclass(OrderResponseV2, dict):
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
        if not isinstance(other, OrderResponseV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
