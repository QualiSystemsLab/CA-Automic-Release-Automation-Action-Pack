#################################################################
# Script Name: 	Snapshot
# Inputs:		None
# Outputs:		None
# Use:			Will change change live status progress bar on
#				a resource then set it back to its old icon.
# Assumptions:	SetResourceStatus script attached to resource
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.0.4
#################################################################

import os
import time
import datetime
import json
import random
import qualipy.api.cloudshell_api

# get matricies for inputs
reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])

# log into the API
csapi = qualipy.api.cloudshell_api.CloudShellAPISession(connectivity["serverAddress"], reservation["ownerUser"], reservation["ownerPass"], reservation["domain"])

csapi.WriteMessageToReservationOutput(reservation["id"], "Beginning to backup " + resource["name"] + "...")

# save the old status
rls = csapi.GetResourceLiveStatus(resource["name"])

# update to backing up 0%
sInput = qualipy.api.cloudshell_api.InputNameValue("Status", "Progress 0")
dInput = qualipy.api.cloudshell_api.InputNameValue("Description", "Backing up...")
csapi.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [sInput, dInput])
time.sleep(random.randint(3,5))

# update to backing up 40%
sInput = qualipy.api.cloudshell_api.InputNameValue("Status", "Progress 40")
dInput = qualipy.api.cloudshell_api.InputNameValue("Description", "Backing up...")
csapi.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [sInput, dInput])
time.sleep(random.randint(2,5))

# update to backing up 60%
sInput = qualipy.api.cloudshell_api.InputNameValue("Status", "Progress 60")
dInput = qualipy.api.cloudshell_api.InputNameValue("Description", "Backing up...")
csapi.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [sInput, dInput])
time.sleep(random.randint(3,6))

# update to backing up 80%
sInput = qualipy.api.cloudshell_api.InputNameValue("Status", "Progress 80")
dInput = qualipy.api.cloudshell_api.InputNameValue("Description", "Backing up...")
csapi.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [sInput, dInput])
time.sleep(random.randint(4,9))

#revert status and append that it was backed up
# if there was no description on the status, change it to backup time
# if there was, append backup time to the old descritiption
newDescription = ""

if len(rls.liveStatusDescription) > 0:
	newDescription = rls.liveStatusDescription + " and backed up at: "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
else:
	newDescription = "Backed up at: "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

sInput = qualipy.api.cloudshell_api.InputNameValue("Status", rls.liveStatusName)
dInput = qualipy.api.cloudshell_api.InputNameValue("Description", newDescription)
csapi.ExecuteCommand(reservation["id"], resource["name"], 0, "GenericSetResourceStatus", [sInput, dInput])

# logoff the API
csapi.Logoff()

print resource["name"] + " has been successfully backed up."  