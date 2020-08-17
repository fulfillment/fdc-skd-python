# StatusTypeV2

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Depricated, use code instead | [optional] 
**is_closed** | **bool** | Depricated, does this status event close the order | [optional] 
**action_required_by** | [**StatusTypeV2ActionRequiredBy**](StatusTypeV2ActionRequiredBy.md) |  | [optional] 
**stage** | [**StatusTypeV2Stage**](StatusTypeV2Stage.md) |  | 
**state** | [**StatusTypeV2Stage**](StatusTypeV2Stage.md) |  | 
**detail** | **str** |  | [optional] 
**reason** | **str** | Depricated | [optional] 
**name** | **str** | Depricated, use stage/state instead | [optional] 
**detail_code** | **str** |  | 
**code** | **str** | Code, see [status codes](#section/Getting-Started/Status-Codes) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

