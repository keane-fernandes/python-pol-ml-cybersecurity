local service_layer_header_size = 56


---
--- MotorDemand dissector
---
local p_motorcontrolcommand_motordemand_payload = Proto (
    "2852170648_1426085669_payload",
    "MotorControlCommand MotorDemand Interface Payload")

p_motorcontrolcommand_motordemand_payload.fields = {
    ProtoField.uint32 ("MotorControlCommand.MotorDemand.values.demand", "MotorDemand.values.demand", base.DEC),
    ProtoField.bytes ("MotorControlCommand.MotorDemand.faults.demand", "MotorDemand.faults.demand"),
    ProtoField.uint8 ("MotorControlCommand.MotorDemand.paddingToAlignment0", "MotorDemand.paddingToAlignment0", base.DEC),
    ProtoField.uint8 ("MotorControlCommand.MotorDemand.paddingToAlignment1", "MotorDemand.paddingToAlignment1", base.DEC),
    ProtoField.uint8 ("MotorControlCommand.MotorDemand.paddingToAlignment2", "MotorDemand.paddingToAlignment2", base.DEC)
}

function p_motorcontrolcommand_motordemand_payload.dissector (buf, pkt, tree)
    local message_size = 8
    local subtree = tree:add (p_motorcontrolcommand_motordemand_payload, buf ())
    subtree:add (p_motorcontrolcommand_motordemand_payload.fields [1], buf (0 + 0, 4)) -- demand
    subtree:add (p_motorcontrolcommand_motordemand_payload.fields [2], buf (0 + 4, 1)) -- demand
    subtree:add (p_motorcontrolcommand_motordemand_payload.fields [3], buf (0 + 5, 1)) -- paddingToAlignment0
    subtree:add (p_motorcontrolcommand_motordemand_payload.fields [4], buf (0 + 6, 1)) -- paddingToAlignment1
    subtree:add (p_motorcontrolcommand_motordemand_payload.fields [5], buf (0 + 7, 1)) -- paddingToAlignment2
    return message_size
end

local p_motorcontrolcommand_motordemand = Proto (
    "2852170648_1426085669",
    "MotorControlCommand MotorDemand Protocol")

function p_motorcontrolcommand_motordemand.dissector (buf, pkt, tree)
    local payload_offset = service_layer_header_size
    local payload_size = 8

    local offset = Dissector.get ("service_layer_header"):call (buf (0, service_layer_header_size):tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170648_1426085669_payload"):call (buf (payload_offset, payload_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_motorcontrolcommand_motordemand)

---
--- MotorControlCommand dissector
---
local p_motorcontrolcommand_service = Proto (
  "2852170648_service",
  "MotorControlCommand Service Message")

function p_motorcontrolcommand_service.dissector (buf, pkt, tree)
    local iid = buf (16+8+4+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python
    return Dissector.get ("2852170648_" .. iid):call (buf ():tvb (), pkt, tree)
end

local p_network_motorcontrolcommand_service = Proto (
  "network_2852170648_service",
  "MotorControlCommand Service Network Protocol")
function p_network_motorcontrolcommand_service.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local offset = Dissector.get ("transport_layer_header"):call (buf ():tvb (), pkt, tree)
    offset = offset + Dissector.get ("2852170648_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
    return offset
end

-- DissectorTable.get ("udp.port"):add_for_decode_as (p_network_motorcontrolcommand_service)