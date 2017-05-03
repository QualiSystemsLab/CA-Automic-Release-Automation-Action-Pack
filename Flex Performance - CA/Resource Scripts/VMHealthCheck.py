#################################################################
# Script Name: 	HealthCheck
# Inputs:		None
# Outputs:		None
# Use:			Will change change live to green to pass HealthCheck
# Assumptions:	GenericSetResourceStatus script attached to resource
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.0.1
#################################################################
import os
import time
import datetime
import json
import random
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])
attr = resource["attributes"]

api = CloudShellAPISession(host=connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=reservation["domain"])

resource_state = api.GetResourceLiveStatus(resource["fullname"])
time.sleep(random.randint(4, 9))

if "Online" in resource_state.liveStatusName and attr["Power State"] == "On":
	status, description = InputNameValue("Status", resource_state.liveStatusName), InputNameValue("Description", "Healthcheck last ran at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
elif attr["Power State"] == "On":
	status, description = InputNameValue("Status", "Online"), InputNameValue("Description", "Healthcheck last ran at: "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
else:
	status, description = InputNameValue("Status", "Error"), InputNameValue("Description", "Healthcheck last failed at: "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

api.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [status, description])

api.Logoff()
