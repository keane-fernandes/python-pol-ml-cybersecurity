---
--- BulkNetwork dissector
---
local header_size = 12
local payloads_header_size = 2
local p_bulknetwork_servicelayer = Proto ("servicelayer_bulknetwork_message",
                                          "Service Layer Bulk Network Message Protocol")

function is_heartbeat_message (size)
    return size == header_size
end

function is_data_message (size)
    return size > header_size
end

function next_8byte_boundary (offset)
    return math.ceil (offset / 8) * 8;
end

function next_aligned_offset (offset)
    return next_8byte_boundary (offset+payloads_header_size) - payloads_header_size
end

function get_sid (buf, offset)
    -- FIXME obviously this field offset should be computed by python
    return buf (offset+16+8+4+4+4, 4):uint ()
end

p_bulknetwork_servicelayer.fields.payload_header = ProtoField.uint16 ("message_size", "Message Size", base.DEC)
function p_bulknetwork_servicelayer.dissector (buf, pkt, tree)
    local message_size = buf:len ()
    if is_data_message (message_size) then
        Dissector.get ("transport_layer_header"):call (buf (0, 16):tvb (), pkt, tree)
        local offset = next_aligned_offset (header_size)
        local subtree = tree:add (p_bulknetwork_servicelayer, buf ())
        local sid = get_sid (buf, offset+2)

        while offset < message_size do
            subtree:add (p_bulknetwork_servicelayer.fields.payload_header, buf (offset, 2))
            offset = offset + 2

            sid = get_sid (buf, offset)
            local service_dissector = Dissector.get (sid .. "_service")
            offset = offset + service_dissector:call (buf (offset):tvb (), pkt, subtree)

            offset = next_aligned_offset (offset)
        end
    elseif is_heartbeat_message (message_size) then
        tree:add (p_bulknetwork_servicelayer, buf ()):add_expert_info (PI_DEBUG, PI_CHAT, "Heartbeat message")
    end
    return offset
end

DissectorTable.get ("udp.port"):add_for_decode_as (p_bulknetwork_servicelayer)