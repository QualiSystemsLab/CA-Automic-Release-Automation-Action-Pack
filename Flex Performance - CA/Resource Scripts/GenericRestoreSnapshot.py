#################################################################
# Script Name: 	GenericRestoreSnapshot
# Inputs:		None
# Outputs:		None
# Use:			Mock the generic restoration process of a resource
# Assumptions:	SetResourceStatus script attached to resource
# Author:		Leeor Vardi <leeor.v@quali.com>
# Version:		1.0
#################################################################

import os
import time
import datetime
import json
import random
from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.api.cloudshell_api import InputNameValue as CmdInput

# get matrices for inputs
reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])

# log into the API
csapi = CloudShellAPISession(connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=reservation["domain"])

csapi.WriteMessageToReservationOutput(reservation["id"], "Beginning to restore " + resource["name"] + "...")

# save the old status
live_status = csapi.GetResourceLiveStatus(resource["name"])

# update to backing up 0%
csapi.ExecuteCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [CmdInput("Status", "Progress 0"), CmdInput("Description", "Restoring...")])
time.sleep(random.randint(3,5))

# update to backing up 40%
csapi.ExecuteCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [CmdInput("Status", "Progress 40"), CmdInput("Description", "Restoring...")])
time.sleep(random.randint(2,5))

# update to backing up 60%
csapi.ExecuteCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [CmdInput("Status", "Progress 60"), CmdInput("Description", "Restoring...")])
time.sleep(random.randint(3,6))

# update to backing up 80%
csapi.ExecuteCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [CmdInput("Status", "Progress 80"), CmdInput("Description", "Restoring...")])
time.sleep(random.randint(4,9))

newDescription = ""

if len(live_status.liveStatusDescription) > 0:
	newDescription = live_status.liveStatusDescription

csapi.ExecuteCommand(reservation["id"], resource["name"], "Resource", "GenericSetResourceStatus", [CmdInput("Status", live_status.liveStatusName), CmdInput("Description", newDescription)])

csapi.WriteMessageToReservationOutput(reservation["id"], resource["name"] + " has been successfully restored.")

# logoff the API
csapi.Logoff()