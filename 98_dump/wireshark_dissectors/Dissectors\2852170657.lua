local service_layer_header_size = 56


---
--- ThrottlePedalDemand dissector
---
local p_thottlepedalstatus_throttlepedaldemand_payload = Proto (
    "2852170657_1426085678_payload",
    "ThottlePedalStatus ThrottlePedalDemand Interface Payload")

p_thottlepedalstatus_throttlepedaldemand_payload.fields = {
    ProtoField.uint32 ("ThottlePedalStatus.ThrottlePedalDemand.values.throttleDemand", "ThrottlePedalDemand.values.throttleDemand", base.DEC),
    ProtoField.bytes ("ThottlePedalStatus.ThrottlePedalDemand.faults.throttleDemand", "ThrottlePedalDemand.faults.throttleDemand"),
    ProtoField.uint8 ("ThottlePedalStatus.ThrottlePedalDemand.paddingToAlignment0", "ThrottlePedalDemand.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("ThottlePedalStatus.ThrottlePedalDemand.paddingToAlignment1", "ThrottlePedalDemand.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("ThottlePedalStatus.ThrottlePedalDemand.paddingToAlignment2", "ThrottlePedalDemand.paddingToAlignment2", base.DEC)
}

function p_thottlepedalstatus_throttlepedaldemand_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_thottlepedalstatus_throttlepedaldemand_payload, buf ())
    subtree:add (p_thottlepedalstatus_throttlepedaldemand_payload.fields [1], buf (0 + 0, 4)) -- throttleDemand
    subtree:add (p_thottlepedalstatus_throttlepedaldemand_payload.fields [2], buf (0 + 4, 1)) -- throttleDemand
    subtree:add (p_thottlepedalstatus_throttlepedaldemand_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_thottlepedalstatus_throttlepedaldemand_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_thottlepedalstatus_throttlepedaldemand_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    return message_size
end

local p_thottlepedalstatus_throttlepedaldemand = Proto (
    "2852170657_1426085678",
    "ThottlePedalStatus ThrottlePedalDemand Protocol")

function p_thottlepedalstatus_throttlepedaldemand.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170657_1426085678_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_thottlepedalstatus_throttlepedaldemand)

---
--- ThottlePedalStatus dissector
---
local p_thottlepedalstatus_service = Proto (
  "2852170657_service",
  "ThottlePedalStatus Service Message")

function p_thottlepedalstatus_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170657_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_thottlepedalstatus_service = Proto (
  "network_2852170657_service",
  "ThottlePedalStatus Service Network Protocol")
function p_network_thottlepedalstatus_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170657_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_thottlepedalstatus_service)