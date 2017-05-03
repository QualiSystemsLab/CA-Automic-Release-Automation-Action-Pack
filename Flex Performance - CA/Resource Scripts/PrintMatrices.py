import os
import json
print("Quali Connectivity:\n{}".format(json.dumps(json.loads(os.environ["QUALICONNECTIVITYCONTEXT"]), indent=4)))
print("Resservation:\n{}".format(json.dumps(json.loads(os.environ["RESERVATIONCONTEXT"]), indent=4)))
print("Resource:\n{}".format(json.dumps(json.loads(os.environ["RESOURCECONTEXT"]), indent=4)))