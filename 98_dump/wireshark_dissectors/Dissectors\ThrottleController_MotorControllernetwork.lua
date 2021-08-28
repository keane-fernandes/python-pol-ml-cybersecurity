-- FIXME probably need to come up with a more unique naming scheme.
p_servicelayer_ThrottleController_MotorController_network_message = Proto (
  "servicelayer_ThrottleController_MotorController_network_message",
  "ThrottleController_MotorController network Distributor Message Protocol")
function p_servicelayer_ThrottleController_MotorController_network_message.init ()
    DissectorTable.get ('udp.port'):add (28091, Dissector.get ('servicelayer_network_message'))
    DissectorTable.get ('udp.port'):add (28191, Dissector.get ('servicelayer_network_message'))
end