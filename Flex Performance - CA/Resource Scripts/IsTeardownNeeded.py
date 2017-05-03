"""
Is Teardown Needed
Version 1.0
Required variables:
Returns true if current reservation should perform teardown or false otherwise.
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
should_run_teardown = True


# Create an API Session on TestShell Python API
api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], 'Global')
shared_resources = []

for resource in api.GetReservationDetails(reservationDetails["id"]).ReservationDescription.Resources:
        if resource.Shared:
            shared_resources.append(resource)

for reservation in api.GetCurrentReservations().Reservations:
    if reservation.Id == reservationDetails["id"]:
        continue
    for reserved_resource in api.GetReservationDetails(reservation.Id).ReservationDescription.Resources:
        if should_run_teardown:
            for shared_resource in shared_resources:
                if shared_resource.Name.split('/')[0] == reserved_resource.Name.split('/')[0]:
                    should_run_teardown = False
                    break


print(str(should_run_teardown))
