# OrderResponseV2

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | FDC ID for this order | 
**tracking_numbers** | [**list[TrackingNumberV2]**](TrackingNumberV2.md) |  | [optional] 
**validated_consignee** | [**Paths1orderspostresponses201contentapplication1jsonschemapropertiesoriginalConsignee**](Paths1orderspostresponses201contentapplication1jsonschemapropertiesoriginalConsignee.md) |  | 
**original_consignee** | [**ConsigneeV21**](ConsigneeV21.md) |  | 
**current_status** | [**StatusEventV2**](StatusEventV2.md) |  | 
**warehouse** | [**UserV2**](UserV2.md) |  | [optional] 
**merchant** | [**MerchantV2**](MerchantV2.md) |  | 
**depart_date** | **datetime** | DateTime order departed an FDC warehouse | [optional] 
**dispatch_date** | **datetime** | DateTime order was dispatched for fulfillment by FDC | [optional] 
**recorded_on** | **datetime** | DateTime order was recorded by FDC | 
**merchant_shipping_method** | **str** | Requested ship method | 
**purchase_order_num** | **str** | Merchant provided PO# | [optional] 
**merchant_order_id** | **str** | Merchant provided ID | 
**parent_order** | [**OrderResponseV2ParentOrder**](OrderResponseV2ParentOrder.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

