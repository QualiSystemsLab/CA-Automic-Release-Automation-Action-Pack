#################################################################
# Script Name: 	VMPowerOn
# Inputs:		None
# Outputs:		None
# Use:			Resets all attribtues
# Assumptions:	None
# Author:		Chris Grabosky <chris.g@qualisystems.com>
# Version:		1.0.2
#################################################################

import os
import time
import datetime
import json
import random
import math
import qualipy.api.cloudshell_api

# get matricies for inputs
reservation = json.loads(os.environ["RESERVATIONCONTEXT"])
resource = json.loads(os.environ["RESOURCECONTEXT"])
connectivity = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])
attr = resource["attributes"]

# log into the API
csapi = qualipy.api.cloudshell_api.CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], reservation["domain"])

attName = "Power State"

csapi.SetAttributeValue(resource["name"], attName, "On")

# logoff the API
csapi.Logoff()