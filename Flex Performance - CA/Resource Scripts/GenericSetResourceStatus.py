#################################################################
# Script Name: 	SetResourceStatus
# Inputs:		str(Status) = status to use as in ServerUniversalSettings.xml
#				str(Description) = additionalInfo hover text
# Outputs:		None
# Use:			Will change change live status based on input
# Assumptions:	None
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.1.2
#################################################################

import os
import time
import datetime
import json
from cloudshell.api.cloudshell_api import CloudShellAPISession

# parse inputs
reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])

# login to api, change status, log off
csapi = CloudShellAPISession(connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=reservation["domain"])
try:
	csapi.SetResourceLiveStatus(resource["name"], os.environ["STATUS"], os.environ["DESCRIPTION"])
except:
	try:
		csapi.SetServiceLiveStatus(reservation["id"], resource["name"], os.environ["STATUS"], os.environ["DESCRIPTION"])
	except:
		pass
	
csapi.Logoff()
