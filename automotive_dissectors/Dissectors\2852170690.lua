local service_layer_header_size = 56


---
--- Brake2Status dissector
---
local p_brake2status_brake2status_payload = Proto (
    "2852170690_1426085711_payload",
    "Brake2Status Brake2Status Interface Payload")

p_brake2status_brake2status_payload.fields = {
    ProtoField.bool ("Brake2Status.Brake2Status.values.brakePressed", "Brake2Status.values.brakePressed", base.NONE),
    ProtoField.bytes ("Brake2Status.Brake2Status.faults.brakePressed", "Brake2Status.faults.brakePressed"),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment0", "Brake2Status.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment1", "Brake2Status.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment2", "Brake2Status.paddingToAlignment2", base.DEC),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment3", "Brake2Status.paddingToAlignment3", base.DEC),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment4", "Brake2Status.paddingToAlignment4", base.DEC),
    ProtoField.uint8 ("Brake2Status.Brake2Status.paddingToAlignment5", "Brake2Status.paddingToAlignment5", base.DEC)
}

function p_brake2status_brake2status_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_brake2status_brake2status_payload, buf ())
    subtree:add (p_brake2status_brake2status_payload.fields [1], buf (0 + 0, 1)) -- brakePressed
    subtree:add (p_brake2status_brake2status_payload.fields [2], buf (0 + 1, 1)) -- brakePressed
    subtree:add (p_brake2status_brake2status_payload.fields [3], buf (0 + 2, 1)) -- paddingToAlignment0
    subtree:add (p_brake2status_brake2status_payload.fields [4], buf (0 + 3, 1)) -- paddingToAlignment1
    subtree:add (p_brake2status_brake2status_payload.fields [5], buf (0 + 4, 1)) -- paddingToAlignment2
    subtree:add (p_brake2status_brake2status_payload.fields [6], buf (0 + 5, 1)) -- paddingToAlignment3
    subtree:add (p_brake2status_brake2status_payload.fields [7], buf (0 + 6, 1)) -- paddingToAlignment4
    subtree:add (p_brake2status_brake2status_payload.fields [8], buf (0 + 7, 1)) -- paddingToAlignment5
    return message_size
end

local p_brake2status_brake2status = Proto (
    "2852170690_1426085711",
    "Brake2Status Brake2Status Protocol")

function p_brake2status_brake2status.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170690_1426085711_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_brake2status_brake2status)

---
--- Brake2Status dissector
---
local p_brake2status_service = Proto (
  "2852170690_service",
  "Brake2Status Service Message")

function p_brake2status_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170690_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_brake2status_service = Proto (
  "network_2852170690_service",
  "Brake2Status Service Network Protocol")
function p_network_brake2status_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170690_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_brake2status_service)