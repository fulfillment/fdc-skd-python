# OrderRequestV2

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_id** | **int** | Necessary if you have a multitenancy account, otherwise we will associate the order with your account | [optional] 
**merchant_order_id** | **str** | Unique ID provided by the merchant | 
**shipping_method** | **str** | Custom for you, it will be mapped to an actual method within the OMS UI | 
**recipient** | [**ConsigneeNewV2**](ConsigneeNewV2.md) |  | 
**items** | [**list[OrdersItems]**](OrdersItems.md) |  | 
**warehouse** | [**OrdersWarehouse**](OrdersWarehouse.md) |  | [optional] 
**integrator** | **str** | Use of this property requires special permission and must be discussed with your account executive; values are restricted while custom values need to be accepted by your AE. | [optional] 
**notes** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

