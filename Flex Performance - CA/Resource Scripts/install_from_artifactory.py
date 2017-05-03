import urllib
import json
import paramiko
import os
from time import sleep
from os import environ as parameter
from cloudshell.api.cloudshell_api import CloudShellAPISession

connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservation = json.loads(parameter["RESERVATIONCONTEXT"])
resource = json.loads(parameter["RESOURCECONTEXT"])

artifactory_server = parameter["artifactory_server_address"]
repo_name = parameter["repository_name"]
playbook_name = parameter["ansible_playbook"]

api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], 'Global')
reservation_details = api.GetReservationDetails(reservation["id"]).ReservationDescription
build_name = reservation_details.Name.split('_')[-1]

api.WriteMessageToReservationOutput(reservation["id"], "Running Ansible playbook  \"{1}\" on \"{0}\"\n\n".format(resource['deployedAppData']["name"], playbook_name))
sleep(3)
api.WriteMessageToReservationOutput(reservation["id"], "TASK: [Retrieve package from repository] ***************************************\n")
file_name = "index.html"
target_url = "http://{0}:8081/artifactory/{1}/{2}/{3}".format(artifactory_server, repo_name, build_name, file_name)
save_target = r"C:\Temp\{0}".format(file_name)
sleep(3)
api.WriteMessageToReservationOutput(reservation["id"], "ok: {0}\n\n".format(resource['deployedAppData']["name"]))
api.WriteMessageToReservationOutput(reservation["id"], "TASK: [Copy package content to Web Server] *************************************\n")
try:
    os.remove(save_target)
except:
    pass
testfile = urllib.URLopener()
testfile.retrieve(target_url, save_target)
original_file = open(save_target, 'r').read()
open(save_target, 'w').write(original_file.format(build_name))

resource_username = "ubuntu"
resource_password = "Quali1234QS1234"
#for attribute in resource['deployedAppData']['attributes']:
#    if attribute['name'] == 'User':
#        resource_username = attribute['value']
#    if attribute['name'] == 'Password':
#        resource_password = api.DecryptPassword(attribute['value']).Value

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=resource['deployedAppData']['address'], username=resource_username, password=resource_password, timeout=300)
sftp = ssh.open_sftp()
sftp.put(save_target, "/var/www/index.html")
sftp.close()
ssh.close()
sleep(3)
api.WriteMessageToReservationOutput(reservation["id"], "ok: {0}\n\n".format(resource['deployedAppData']["name"]))
api.WriteMessageToReservationOutput(reservation["id"], "PLAY RECAP *********************************************************************\n")
api.WriteMessageToReservationOutput(reservation["id"], "{0}\t\t: ok=2\tchanged=0\tunreachable=0\tfailed=0\n\n".format(resource['deployedAppData']["name"]))

