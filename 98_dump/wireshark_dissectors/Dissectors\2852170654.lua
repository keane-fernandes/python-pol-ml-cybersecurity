local service_layer_header_size = 56


---
--- BrakeStatus dissector
---
local p_brakestatus_brakestatus_payload = Proto (
    "2852170654_1426085675_payload",
    "BrakeStatus BrakeStatus Interface Payload")

p_brakestatus_brakestatus_payload.fields = {
    ProtoField.bool ("BrakeStatus.BrakeStatus.values.brakePressed", "BrakeStatus.values.brakePressed", base.NONE),
    ProtoField.bytes ("BrakeStatus.BrakeStatus.faults.brakePressed", "BrakeStatus.faults.brakePressed"),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment0", "BrakeStatus.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment1", "BrakeStatus.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment2", "BrakeStatus.paddingToAlignment2", base.DEC),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment3", "BrakeStatus.paddingToAlignment3", base.DEC),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment4", "BrakeStatus.paddingToAlignment4", base.DEC),
    ProtoField.uint8 ("BrakeStatus.BrakeStatus.paddingToAlignment5", "BrakeStatus.paddingToAlignment5", base.DEC)
}

function p_brakestatus_brakestatus_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_brakestatus_brakestatus_payload, buf ())
    subtree:add (p_brakestatus_brakestatus_payload.fields [1], buf (0 + 0, 1)) -- brakePressed
    subtree:add (p_brakestatus_brakestatus_payload.fields [2], buf (0 + 1, 1)) -- brakePressed
    subtree:add (p_brakestatus_brakestatus_payload.fields [3], buf (0 + 2, 1)) -- paddingToAlignment0
    subtree:add (p_brakestatus_brakestatus_payload.fields [4], buf (0 + 3, 1)) -- paddingToAlignment1
    subtree:add (p_brakestatus_brakestatus_payload.fields [5], buf (0 + 4, 1)) -- paddingToAlignment2
    subtree:add (p_brakestatus_brakestatus_payload.fields [6], buf (0 + 5, 1)) -- paddingToAlignment3
    subtree:add (p_brakestatus_brakestatus_payload.fields [7], buf (0 + 6, 1)) -- paddingToAlignment4
    subtree:add (p_brakestatus_brakestatus_payload.fields [8], buf (0 + 7, 1)) -- paddingToAlignment5
    return message_size
end

local p_brakestatus_brakestatus = Proto (
    "2852170654_1426085675",
    "BrakeStatus BrakeStatus Protocol")

function p_brakestatus_brakestatus.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170654_1426085675_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_brakestatus_brakestatus)

---
--- BrakeStatus dissector
---
local p_brakestatus_service = Proto (
  "2852170654_service",
  "BrakeStatus Service Message")

function p_brakestatus_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170654_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_brakestatus_service = Proto (
  "network_2852170654_service",
  "BrakeStatus Service Network Protocol")
function p_network_brakestatus_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170654_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_brakestatus_service)