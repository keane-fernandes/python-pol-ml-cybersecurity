local service_layer_header_size = 56


---
--- SpeedStatus dissector
---
local p_vehiclespeedstatus_speedstatus_payload = Proto (
    "2852170660_1426085681_payload",
    "VehicleSpeedStatus SpeedStatus Interface Payload")

p_vehiclespeedstatus_speedstatus_payload.fields = {
    ProtoField.uint32 ("VehicleSpeedStatus.SpeedStatus.values.speed", "SpeedStatus.values.speed", base.DEC),
    ProtoField.bool ("VehicleSpeedStatus.SpeedStatus.values.speedRangeFault", "SpeedStatus.values.speedRangeFault", base.NONE),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.values.paddingToAlignment0", "SpeedStatus.values.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.values.paddingToAlignment1", "SpeedStatus.values.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.values.paddingToAlignment2", "SpeedStatus.values.paddingToAlignment2", base.DEC),
    ProtoField.bytes ("VehicleSpeedStatus.SpeedStatus.faults.speed", "SpeedStatus.faults.speed"),
    ProtoField.bytes ("VehicleSpeedStatus.SpeedStatus.faults.speedRangeFault", "SpeedStatus.faults.speedRangeFault"),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment0", "SpeedStatus.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment1", "SpeedStatus.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment2", "SpeedStatus.paddingToAlignment2", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment3", "SpeedStatus.paddingToAlignment3", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment4", "SpeedStatus.paddingToAlignment4", base.DEC),
    ProtoField.uint8 ("VehicleSpeedStatus.SpeedStatus.paddingToAlignment5", "SpeedStatus.paddingToAlignment5", base.DEC)
}

function p_vehiclespeedstatus_speedstatus_payload.dissector (buf, pkt, tree)
    local message_size = 16
    local subtree = tree:add (p_vehiclespeedstatus_speedstatus_payload, buf ())
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [1], buf (0 + 0, 4)) -- speed
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [2], buf (0 + 4, 1)) -- speedRangeFault
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [6], buf (0 + 8, 1)) -- speed
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [7], buf (0 + 9, 1)) -- speedRangeFault
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [8], buf (0 + 10, 1)) -- paddingToAlignment0
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [9], buf (0 + 11, 1)) -- paddingToAlignment1
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [10], buf (0 + 12, 1)) -- paddingToAlignment2
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [11], buf (0 + 13, 1)) -- paddingToAlignment3
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [12], buf (0 + 14, 1)) -- paddingToAlignment4
    subtree:add (p_vehiclespeedstatus_speedstatus_payload.fields [13], buf (0 + 15, 1)) -- paddingToAlignment5
    return message_size
end

local p_vehiclespeedstatus_speedstatus = Proto (
    "2852170660_1426085681",
    "VehicleSpeedStatus SpeedStatus Protocol")

function p_vehiclespeedstatus_speedstatus.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 16

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170660_1426085681_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_vehiclespeedstatus_speedstatus)

---
--- VehicleSpeedStatus dissector
---
local p_vehiclespeedstatus_service = Proto (
  "2852170660_service",
  "VehicleSpeedStatus Service Message")

function p_vehiclespeedstatus_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170660_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_vehiclespeedstatus_service = Proto (
  "network_2852170660_service",
  "VehicleSpeedStatus Service Network Protocol")
function p_network_vehiclespeedstatus_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170660_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_vehiclespeedstatus_service)