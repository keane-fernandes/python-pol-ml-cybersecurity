local service_layer_header_size = 56


---
--- CalData dissector
---
local p_cruisecontrolvehiclefunctioncalibration_caldata_payload = Proto (
    "2852170666_1426085687_payload",
    "CruiseControlVehicleFunctionCalibration CalData Interface Payload")

p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields = {
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.values.empty-struct-implicit-field", "CalData.values.empty-struct-implicit-field", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.faults.empty-struct-implicit-field", "CalData.faults.empty-struct-implicit-field", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment0", "CalData.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment1", "CalData.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment2", "CalData.paddingToAlignment2", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment3", "CalData.paddingToAlignment3", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment4", "CalData.paddingToAlignment4", base.DEC),
    ProtoField.uint8 ("CruiseControlVehicleFunctionCalibration.CalData.paddingToAlignment5", "CalData.paddingToAlignment5", base.DEC)
}

function p_cruisecontrolvehiclefunctioncalibration_caldata_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload, buf ())
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [1], buf (0 + 0, 1)) -- empty-struct-implicit-field
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [2], buf (0 + 1, 1)) -- empty-struct-implicit-field
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [3], buf (0 + 2, 1)) -- paddingToAlignment0
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [4], buf (0 + 3, 1)) -- paddingToAlignment1
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [5], buf (0 + 4, 1)) -- paddingToAlignment2
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [6], buf (0 + 5, 1)) -- paddingToAlignment3
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [7], buf (0 + 6, 1)) -- paddingToAlignment4
    subtree:add (p_cruisecontrolvehiclefunctioncalibration_caldata_payload.fields [8], buf (0 + 7, 1)) -- paddingToAlignment5
    return message_size
end

local p_cruisecontrolvehiclefunctioncalibration_caldata = Proto (
    "2852170666_1426085687",
    "CruiseControlVehicleFunctionCalibration CalData Protocol")

function p_cruisecontrolvehiclefunctioncalibration_caldata.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170666_1426085687_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_cruisecontrolvehiclefunctioncalibration_caldata)

---
--- CruiseControlVehicleFunctionCalibration dissector
---
local p_cruisecontrolvehiclefunctioncalibration_service = Proto (
  "2852170666_service",
  "CruiseControlVehicleFunctionCalibration Service Message")

function p_cruisecontrolvehiclefunctioncalibration_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170666_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_cruisecontrolvehiclefunctioncalibration_service = Proto (
  "network_2852170666_service",
  "CruiseControlVehicleFunctionCalibration Service Network Protocol")
function p_network_cruisecontrolvehiclefunctioncalibration_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170666_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_cruisecontrolvehiclefunctioncalibration_service)