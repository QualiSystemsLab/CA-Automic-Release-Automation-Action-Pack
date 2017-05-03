#################################################################
# Script Name: 	GenericDelayPrint
# Inputs:		str(MSG) = Message to print out async
#				str(DELAY) = How long to wait after
# Outputs:		None
# Use:			Cause a fake msg to be written
# Assumptions:	None
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.0.0
#################################################################

import os
import time
import datetime
import json
import qualipy.api.cloudshell_api

# parse inputs
reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])

# login to api, change status, log off
csapi = qualipy.api.cloudshell_api.CloudShellAPISession(connectivity["serverAddress"], reservation["ownerUser"], reservation["ownerPass"], reservation["domain"])
csapi.WriteMessageToReservationOutput(reservation["id"], os.environ["MSG"])

time.sleep(int(os.environ["DELAY"]))

csapi.Logoff()