local service_layer_header_size = 56


---
--- ThrottlePedal2Demand dissector
---
local p_thottlepedal2status_throttlepedal2demand_payload = Proto (
    "2852170696_1426085717_payload",
    "ThottlePedal2Status ThrottlePedal2Demand Interface Payload")

p_thottlepedal2status_throttlepedal2demand_payload.fields = {
    ProtoField.uint32 ("ThottlePedal2Status.ThrottlePedal2Demand.values.throttleDemand", "ThrottlePedal2Demand.values.throttleDemand", base.DEC),
    ProtoField.bytes ("ThottlePedal2Status.ThrottlePedal2Demand.faults.throttleDemand", "ThrottlePedal2Demand.faults.throttleDemand"),
    ProtoField.uint8 ("ThottlePedal2Status.ThrottlePedal2Demand.paddingToAlignment0", "ThrottlePedal2Demand.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("ThottlePedal2Status.ThrottlePedal2Demand.paddingToAlignment1", "ThrottlePedal2Demand.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("ThottlePedal2Status.ThrottlePedal2Demand.paddingToAlignment2", "ThrottlePedal2Demand.paddingToAlignment2", base.DEC)
}

function p_thottlepedal2status_throttlepedal2demand_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_thottlepedal2status_throttlepedal2demand_payload, buf ())
    subtree:add (p_thottlepedal2status_throttlepedal2demand_payload.fields [1], buf (0 + 0, 4)) -- throttleDemand
    subtree:add (p_thottlepedal2status_throttlepedal2demand_payload.fields [2], buf (0 + 4, 1)) -- throttleDemand
    subtree:add (p_thottlepedal2status_throttlepedal2demand_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_thottlepedal2status_throttlepedal2demand_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_thottlepedal2status_throttlepedal2demand_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    return message_size
end

local p_thottlepedal2status_throttlepedal2demand = Proto (
    "2852170696_1426085717",
    "ThottlePedal2Status ThrottlePedal2Demand Protocol")

function p_thottlepedal2status_throttlepedal2demand.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170696_1426085717_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_thottlepedal2status_throttlepedal2demand)

---
--- ThottlePedal2Status dissector
---
local p_thottlepedal2status_service = Proto (
  "2852170696_service",
  "ThottlePedal2Status Service Message")

function p_thottlepedal2status_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170696_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_thottlepedal2status_service = Proto (
  "network_2852170696_service",
  "ThottlePedal2Status Service Network Protocol")
function p_network_thottlepedal2status_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170696_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_thottlepedal2status_service)