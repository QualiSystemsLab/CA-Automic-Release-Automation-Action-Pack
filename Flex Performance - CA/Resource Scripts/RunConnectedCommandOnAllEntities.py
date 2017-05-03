"""
Run Command on All Entities in the reservation
Version 1.1
Required variables: command_name, command_inputs (csv), print_output, use_exact_name, run_synchronusly
"""
from qualipy.api.cloudshell_api import CloudShellAPISession
from qualipy.api.cloudshell_api import InputNameValue
import json
from os import environ as parameter
import thread


# Get CloudShell information passed as env. variables
connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservationDetails = json.loads(parameter["RESERVATIONCONTEXT"])
resourceDetails = json.loads(parameter["RESOURCECONTEXT"])
command_name = parameter["command_name"]
command_inputs = parameter["command_inputs"].split(',')
processed_command_inputs = []
if command_inputs == ['']: command_inputs = []
for index in range(0,len(command_inputs),2):
    processed_command_inputs.append(InputNameValue(command_inputs[index],command_inputs[index+1]))
command_tag = parameter["command_tag"]
print_output = parameter["print_output"]=="True"
use_exact_name = parameter["use_exact_name"] == "True"
run_synchronously = parameter["run_synchronously"] == "True"

# Create an API Session on TestShell Python API
api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], reservationDetails["domain"])
reservation_details_from_api = api.GetReservationDetails(reservationDetails["id"])

for resource in reservation_details_from_api.ReservationDescription.Resources:
    try:
        if not use_exact_name:
            resource_commands = api.GetResourceConnectedCommands(resource.Name)
            for command in resource_commands.Commands:
                if command.Name.find(command_name) != -1 and len(command.Parameters) == len(processed_command_inputs):
                    if not run_synchronously:
                        thread.start_new_thread(api.ExecuteResourceConnectedCommand,(reservationDetails["id"], resource.Name, command.Name, command_tag, processed_command_inputs, [], print_output))
                        break
                    else:
                        api.ExecuteResourceConnectedCommand(reservationDetails["id"], resource.Name, command.Name, command_tag, processed_command_inputs, [], print_output)
        else:
            if not run_synchronously:
                thread.start_new_thread(api.ExecuteResourceConnectedCommand,(reservationDetails["id"], resource.Name, command_name, command_tag, processed_command_inputs, [], print_output))
                continue
            else:
                api.ExecuteResourceConnectedCommand(reservationDetails["id"], resource.Name, command_namee, command_tag, processed_command_inputs, [], print_output)
    except:
        continue