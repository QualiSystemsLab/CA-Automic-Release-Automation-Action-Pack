#################################################################
# Script Name: 	HealthCheck
# Inputs:		None
# Outputs:		None
# Use:			Will change change live to green to pass HealthCheck
# Assumptions:	GenericSetResourceStatus script attached to resource
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.0.4
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

csapi = CloudShellAPISession(connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=reservation["domain"])

time.sleep(random.randint(4, 9))

status = InputNameValue("Status", "Online")
Description = InputNameValue("Description", "Healthcheck last ran at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

csapi.EnqueueCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [status, Description])
csapi.Logoff()
