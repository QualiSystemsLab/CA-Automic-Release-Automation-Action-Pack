"""
Run Command on All Entities in the reservation
Version 1.1.1
Required variables: command_name, command_inputs (csv), print_output, use_exact_name, run_synchronusly
"""
from qualipy.api.cloudshell_api import CloudShellAPISession
from qualipy.api.cloudshell_api import InputNameValue
import json
from os import environ as parameter
import sys

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
print_output = parameter["print_output"]=="True"
use_exact_name = parameter["use_exact_name"] == "True"
run_synchronously = parameter["run_synchronously"] == "True"

# Create an API Session on TestShell Python API
api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], reservationDetails["domain"])
reservation_details_from_api = api.GetReservationDetails(reservationDetails["id"])
entities_run = []

if run_synchronously:
    MethodToRun = api.ExecuteCommand
else:
    MethodToRun = api.EnqueueCommand

for resource in reservation_details_from_api.ReservationDescription.Resources:
    try:
        if not use_exact_name:
            resource_commands = api.GetResourceCommands(resource.Name)
            for command in resource_commands.Commands:
                if command.Name.find(command_name) != -1 and len(command.Parameters) == len(processed_command_inputs):
                    MethodToRun(reservationDetails["id"], resource.Name, 'Resource', command.Name, processed_command_inputs, print_output)
                    entities_run.append(resource.Name)
                    break
        else:
            MethodToRun(reservationDetails["id"], resource.Name, 'Resource', command_name, processed_command_inputs, print_output)
            entities_run.append(resource.Name)
    except:
        continue

for service in reservation_details_from_api.ReservationDescription.Services:
    try:
        if not use_exact_name:
            service_commands = api.GetServiceCommands(service.ServiceName)
            for command in service_commands.Commands:
                if command.Name.find(command_name) != -1 and len(command.Parameters) == len(processed_command_inputs):
                    MethodToRun(reservationDetails["id"], service.Alias, 'Service', command.Name, processed_command_inputs, print_output)
                    entities_run.append(service.Alias)
                    break
        else:
            MethodToRun(reservationDetails["id"], service.Alias, 'Service', command_name, processed_command_inputs, print_output)
            entities_run.append(service.Alias)
    except:
        continue

print("Ran the command on the following entities:")
for entity in entities_run:
    print(entity + " ")