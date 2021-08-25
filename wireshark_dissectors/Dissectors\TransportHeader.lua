local p_transport_header = Proto ("transport_layer_header", "Transport Layer Header")
p_transport_header.fields = {}
p_transport_header.fields.header = ProtoField.bytes ("header", "header")

function p_transport_header.dissector (buf, pinfo, tree)
    local header_size = 16
    local subtree = tree:add (p_transport_header, buf (0, header_size))
    subtree:add (p_transport_header.fields.header, buf (0, header_size))
end
