local service_layer_header_size = 56


---
--- Speed2Status dissector
---
local p_vehiclespeed2status_speed2status_payload = Proto (
    "2852170687_1426085708_payload",
    "VehicleSpeed2Status Speed2Status Interface Payload")

p_vehiclespeed2status_speed2status_payload.fields = {
    ProtoField.uint32 ("VehicleSpeed2Status.Speed2Status.values.speed", "Speed2Status.values.speed", base.DEC),
    ProtoField.bool ("VehicleSpeed2Status.Speed2Status.values.speedRangeFault", "Speed2Status.values.speedRangeFault", base.NONE),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.values.paddingToAlignment0", "Speed2Status.values.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.values.paddingToAlignment1", "Speed2Status.values.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.values.paddingToAlignment2", "Speed2Status.values.paddingToAlignment2", base.DEC),
    ProtoField.bytes ("VehicleSpeed2Status.Speed2Status.faults.speed", "Speed2Status.faults.speed"),
    ProtoField.bytes ("VehicleSpeed2Status.Speed2Status.faults.speedRangeFault", "Speed2Status.faults.speedRangeFault"),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment0", "Speed2Status.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment1", "Speed2Status.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment2", "Speed2Status.paddingToAlignment2", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment3", "Speed2Status.paddingToAlignment3", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment4", "Speed2Status.paddingToAlignment4", base.DEC),
    ProtoField.uint8 ("VehicleSpeed2Status.Speed2Status.paddingToAlignment5", "Speed2Status.paddingToAlignment5", base.DEC)
}

function p_vehiclespeed2status_speed2status_payload.dissector (buf, pkt, tree)
    local message_size = 16
    local subtree = tree:add (p_vehiclespeed2status_speed2status_payload, buf ())
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [1], buf (0 + 0, 4)) -- speed
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [2], buf (0 + 4, 1)) -- speedRangeFault
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [6], buf (0 + 8, 1)) -- speed
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [7], buf (0 + 9, 1)) -- speedRangeFault
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [8], buf (0 + 10, 1)) -- paddingToAlignment0
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [9], buf (0 + 11, 1)) -- paddingToAlignment1
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [10], buf (0 + 12, 1)) -- paddingToAlignment2
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [11], buf (0 + 13, 1)) -- paddingToAlignment3
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [12], buf (0 + 14, 1)) -- paddingToAlignment4
    subtree:add (p_vehiclespeed2status_speed2status_payload.fields [13], buf (0 + 15, 1)) -- paddingToAlignment5
    return message_size
end

local p_vehiclespeed2status_speed2status = Proto (
    "2852170687_1426085708",
    "VehicleSpeed2Status Speed2Status Protocol")

function p_vehiclespeed2status_speed2status.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 16

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170687_1426085708_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_vehiclespeed2status_speed2status)

---
--- VehicleSpeed2Status dissector
---
local p_vehiclespeed2status_service = Proto (
  "2852170687_service",
  "VehicleSpeed2Status Service Message")

function p_vehiclespeed2status_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170687_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_vehiclespeed2status_service = Proto (
  "network_2852170687_service",
  "VehicleSpeed2Status Service Network Protocol")
function p_network_vehiclespeed2status_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170687_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_vehiclespeed2status_service)