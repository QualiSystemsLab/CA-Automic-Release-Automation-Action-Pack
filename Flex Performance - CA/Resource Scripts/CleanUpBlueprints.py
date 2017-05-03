from cloudshell.api.cloudshell_api import CloudShellAPISession
from os import environ as parameter
import json

connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservationDetails = json.loads(parameter["RESERVATIONCONTEXT"])
resourceDetails = json.loads(parameter["RESOURCECONTEXT"])

approved_blueprints_file = open(parameter["input_file"],'r')
domains_to_scan = parameter["domains"].split(',')
dry_run = 'false' not in parameter["dry_run"].lower()

api = CloudShellAPISession(host=connectivity["serverAddress"], token_id=connectivity["adminAuthToken"], domain=reservationDetails["domain"])
approved_blueprints = [(line.split('\t')[0].strip(), line.split('\t')[1].strip()) for line in approved_blueprints_file.readlines()]
for domain in domains_to_scan:
    domain_details = api.GetDomainDetails(domain)
    blueprints_in_domain = domain_details.Topologies
    blueprints_to_delete = [blueprint.Name for blueprint in blueprints_in_domain if (domain, blueprint.Name) not in approved_blueprints]
    for blueprint in blueprints_to_delete:
        if not dry_run:
            api.DeleteTopology(domain_details.TopologiesFolder + '\\' + blueprint)
        print("Deleted Blueprint {}".format(domain_details.TopologiesFolder + '\\' + blueprint))
