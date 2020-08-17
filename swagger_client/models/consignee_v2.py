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

class ConsigneeV2(object):
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
        'updated_by': 'Paths1returnsgetresponses200contentapplication1jsonschemapropertiesdataitemspropertiesupdatedBy',
        'updated_at': 'datetime',
        'iso': 'IsoCountryV2',
        'company_name': 'str',
        'country': 'str',
        'postal_code': 'str',
        'address_region': 'str',
        'address_locality': 'str',
        'address2': 'str',
        'address1': 'str',
        'phone': 'str',
        'last_name': 'str',
        'first_name': 'str',
        'email': 'str'
    }

    attribute_map = {
        'id': 'id',
        'updated_by': 'updatedBy',
        'updated_at': 'updatedAt',
        'iso': 'iso',
        'company_name': 'companyName',
        'country': 'country',
        'postal_code': 'postalCode',
        'address_region': 'addressRegion',
        'address_locality': 'addressLocality',
        'address2': 'address2',
        'address1': 'address1',
        'phone': 'phone',
        'last_name': 'lastName',
        'first_name': 'firstName',
        'email': 'email'
    }

    def __init__(self, id=None, updated_by=None, updated_at=None, iso=None, company_name=None, country=None, postal_code=None, address_region=None, address_locality=None, address2=None, address1=None, phone=None, last_name=None, first_name=None, email=None):  # noqa: E501
        """ConsigneeV2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._updated_by = None
        self._updated_at = None
        self._iso = None
        self._company_name = None
        self._country = None
        self._postal_code = None
        self._address_region = None
        self._address_locality = None
        self._address2 = None
        self._address1 = None
        self._phone = None
        self._last_name = None
        self._first_name = None
        self._email = None
        self.discriminator = None
        self.id = id
        if updated_by is not None:
            self.updated_by = updated_by
        if updated_at is not None:
            self.updated_at = updated_at
        if iso is not None:
            self.iso = iso
        if company_name is not None:
            self.company_name = company_name
        self.country = country
        self.postal_code = postal_code
        self.address_region = address_region
        self.address_locality = address_locality
        if address2 is not None:
            self.address2 = address2
        self.address1 = address1
        if phone is not None:
            self.phone = phone
        self.last_name = last_name
        self.first_name = first_name
        if email is not None:
            self.email = email

    @property
    def id(self):
        """Gets the id of this ConsigneeV2.  # noqa: E501


        :return: The id of this ConsigneeV2.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConsigneeV2.


        :param id: The id of this ConsigneeV2.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def updated_by(self):
        """Gets the updated_by of this ConsigneeV2.  # noqa: E501


        :return: The updated_by of this ConsigneeV2.  # noqa: E501
        :rtype: Paths1returnsgetresponses200contentapplication1jsonschemapropertiesdataitemspropertiesupdatedBy
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this ConsigneeV2.


        :param updated_by: The updated_by of this ConsigneeV2.  # noqa: E501
        :type: Paths1returnsgetresponses200contentapplication1jsonschemapropertiesdataitemspropertiesupdatedBy
        """

        self._updated_by = updated_by

    @property
    def updated_at(self):
        """Gets the updated_at of this ConsigneeV2.  # noqa: E501


        :return: The updated_at of this ConsigneeV2.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ConsigneeV2.


        :param updated_at: The updated_at of this ConsigneeV2.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def iso(self):
        """Gets the iso of this ConsigneeV2.  # noqa: E501


        :return: The iso of this ConsigneeV2.  # noqa: E501
        :rtype: IsoCountryV2
        """
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the iso of this ConsigneeV2.


        :param iso: The iso of this ConsigneeV2.  # noqa: E501
        :type: IsoCountryV2
        """

        self._iso = iso

    @property
    def company_name(self):
        """Gets the company_name of this ConsigneeV2.  # noqa: E501


        :return: The company_name of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this ConsigneeV2.


        :param company_name: The company_name of this ConsigneeV2.  # noqa: E501
        :type: str
        """

        self._company_name = company_name

    @property
    def country(self):
        """Gets the country of this ConsigneeV2.  # noqa: E501

        Ideally provide the two character ISO code  # noqa: E501

        :return: The country of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this ConsigneeV2.

        Ideally provide the two character ISO code  # noqa: E501

        :param country: The country of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if country is None:
            raise ValueError("Invalid value for `country`, must not be `None`")  # noqa: E501

        self._country = country

    @property
    def postal_code(self):
        """Gets the postal_code of this ConsigneeV2.  # noqa: E501

        Postal Code / Zip  # noqa: E501

        :return: The postal_code of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """Sets the postal_code of this ConsigneeV2.

        Postal Code / Zip  # noqa: E501

        :param postal_code: The postal_code of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if postal_code is None:
            raise ValueError("Invalid value for `postal_code`, must not be `None`")  # noqa: E501

        self._postal_code = postal_code

    @property
    def address_region(self):
        """Gets the address_region of this ConsigneeV2.  # noqa: E501

        Province / State  # noqa: E501

        :return: The address_region of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._address_region

    @address_region.setter
    def address_region(self, address_region):
        """Sets the address_region of this ConsigneeV2.

        Province / State  # noqa: E501

        :param address_region: The address_region of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if address_region is None:
            raise ValueError("Invalid value for `address_region`, must not be `None`")  # noqa: E501

        self._address_region = address_region

    @property
    def address_locality(self):
        """Gets the address_locality of this ConsigneeV2.  # noqa: E501

        City  # noqa: E501

        :return: The address_locality of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._address_locality

    @address_locality.setter
    def address_locality(self, address_locality):
        """Sets the address_locality of this ConsigneeV2.

        City  # noqa: E501

        :param address_locality: The address_locality of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if address_locality is None:
            raise ValueError("Invalid value for `address_locality`, must not be `None`")  # noqa: E501

        self._address_locality = address_locality

    @property
    def address2(self):
        """Gets the address2 of this ConsigneeV2.  # noqa: E501


        :return: The address2 of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._address2

    @address2.setter
    def address2(self, address2):
        """Sets the address2 of this ConsigneeV2.


        :param address2: The address2 of this ConsigneeV2.  # noqa: E501
        :type: str
        """

        self._address2 = address2

    @property
    def address1(self):
        """Gets the address1 of this ConsigneeV2.  # noqa: E501


        :return: The address1 of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._address1

    @address1.setter
    def address1(self, address1):
        """Sets the address1 of this ConsigneeV2.


        :param address1: The address1 of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if address1 is None:
            raise ValueError("Invalid value for `address1`, must not be `None`")  # noqa: E501

        self._address1 = address1

    @property
    def phone(self):
        """Gets the phone of this ConsigneeV2.  # noqa: E501


        :return: The phone of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this ConsigneeV2.


        :param phone: The phone of this ConsigneeV2.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def last_name(self):
        """Gets the last_name of this ConsigneeV2.  # noqa: E501


        :return: The last_name of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this ConsigneeV2.


        :param last_name: The last_name of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if last_name is None:
            raise ValueError("Invalid value for `last_name`, must not be `None`")  # noqa: E501

        self._last_name = last_name

    @property
    def first_name(self):
        """Gets the first_name of this ConsigneeV2.  # noqa: E501


        :return: The first_name of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this ConsigneeV2.


        :param first_name: The first_name of this ConsigneeV2.  # noqa: E501
        :type: str
        """
        if first_name is None:
            raise ValueError("Invalid value for `first_name`, must not be `None`")  # noqa: E501

        self._first_name = first_name

    @property
    def email(self):
        """Gets the email of this ConsigneeV2.  # noqa: E501


        :return: The email of this ConsigneeV2.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ConsigneeV2.


        :param email: The email of this ConsigneeV2.  # noqa: E501
        :type: str
        """

        self._email = email

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
        if issubclass(ConsigneeV2, dict):
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
        if not isinstance(other, ConsigneeV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
