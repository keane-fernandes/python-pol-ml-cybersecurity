local service_layer_header_size = 56


---
--- CruiseControlDemand dissector
---
local p_cruisecontrolstatus_cruisecontroldemand_payload = Proto (
    "2852170651_1426085672_payload",
    "CruiseControlStatus CruiseControlDemand Interface Payload")

p_cruisecontrolstatus_cruisecontroldemand_payload.fields = {
    ProtoField.uint32 ("CruiseControlStatus.CruiseControlDemand.values.throttleDemand", "CruiseControlDemand.values.throttleDemand", base.DEC),
    ProtoField.bytes ("CruiseControlStatus.CruiseControlDemand.faults.throttleDemand", "CruiseControlDemand.faults.throttleDemand"),
    ProtoField.uint8 ("CruiseControlStatus.CruiseControlDemand.paddingToAlignment0", "CruiseControlDemand.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("CruiseControlStatus.CruiseControlDemand.paddingToAlignment1", "CruiseControlDemand.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("CruiseControlStatus.CruiseControlDemand.paddingToAlignment2", "CruiseControlDemand.paddingToAlignment2", base.DEC)
}

function p_cruisecontrolstatus_cruisecontroldemand_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_cruisecontrolstatus_cruisecontroldemand_payload, buf ())
    subtree:add (p_cruisecontrolstatus_cruisecontroldemand_payload.fields [1], buf (0 + 0, 4)) -- throttleDemand
    subtree:add (p_cruisecontrolstatus_cruisecontroldemand_payload.fields [2], buf (0 + 4, 1)) -- throttleDemand
    subtree:add (p_cruisecontrolstatus_cruisecontroldemand_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_cruisecontrolstatus_cruisecontroldemand_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_cruisecontrolstatus_cruisecontroldemand_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    return message_size
end

local p_cruisecontrolstatus_cruisecontroldemand = Proto (
    "2852170651_1426085672",
    "CruiseControlStatus CruiseControlDemand Protocol")

function p_cruisecontrolstatus_cruisecontroldemand.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170651_1426085672_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_cruisecontrolstatus_cruisecontroldemand)

---
--- CruiseControlStatus dissector
---
local p_cruisecontrolstatus_service = Proto (
  "2852170651_service",
  "CruiseControlStatus Service Message")

function p_cruisecontrolstatus_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170651_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_cruisecontrolstatus_service = Proto (
  "network_2852170651_service",
  "CruiseControlStatus Service Network Protocol")
function p_network_cruisecontrolstatus_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170651_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_cruisecontrolstatus_service)