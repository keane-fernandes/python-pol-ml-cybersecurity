local p_servicelayer = Proto ("servicelayer_resilient_message", "Service Layer Resilient Network Protocol")

function p_servicelayer.dissector (buf, pkt, tree)
    local transport_layer_header_size = 16
    local sid = buf (transport_layer_header_size+16+8+4+4+4, 4):uint () -- FIXME obviously this field offset should be computed by python

    local offset = Dissector.get ("transport_layer_header"):call (buf (0, transport_layer_header_size):tvb (), pkt, tree)
    return offset + Dissector.get (sid .. "_service"):call (buf (transport_layer_header_size):tvb (), pkt, tree)
end

DissectorTable.get ("udp.port"):add_for_decode_as (p_servicelayer)