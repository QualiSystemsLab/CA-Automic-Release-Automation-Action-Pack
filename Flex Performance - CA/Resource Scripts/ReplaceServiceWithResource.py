"""
Replace a service with an existing/new resource.
Version 1.0
Required variables: service_alias, resource_name, resource_family, resource_model, create_resource(True / False), share_resource (True / False)
"""
from qualipy.api.cloudshell_api import CloudShellAPISession, InputNameValue, SetConnectorRequest
import json
from os import environ as parameter

# Get CloudShell information passed as variables
connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservationDetails = json.loads(parameter["RESERVATIONCONTEXT"])
resourceDetails = json.loads(parameter["RESOURCECONTEXT"])
service_alias = parameter["service_alias"]
resource_name = parameter["resource_name"]
resource_family = parameter["resource_family"]
resource_model = parameter["resource_model"]
create_resource = parameter["create_resource"].lower() == "true"
share_resource = parameter["share_resource"].lower() == "true"
connectors = []

# Create an API Session on TestShell Python API
api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], reservationDetails["domain"])
reservation_details_from_api = api.GetReservationDetails(reservationDetails["id"])

if create_resource:
    api.CreateResource(resource_family, resource_model, resource_name, "NA", "Generated Resources")

reservation_connectors = reservation_details_from_api.ReservationDescription.Connectors
for connector in reservation_connectors:
    if connector.Source == service_alias:
        connectors.append(SetConnectorRequest(resource_name, connector.Target, connector.Direction, connector.Alias))
    elif connector.Target == service_alias:
        connectors.append(SetConnectorRequest(connector.Source, resource_name, connector.Direction, connector.Alias))


services_details = reservation_details_from_api.ReservationDescription.Services
for service in services_details:
    if service.Alias == service_alias:
        requested_service = service
        break

services_positions = api.GetReservationServicesPositions(reservationDetails["id"])
for service_diagram_layout in services_positions.ResourceDiagramLayouts:
    if service_diagram_layout.ResourceName == service_alias:
        service_position = service_diagram_layout
        break

api.RemoveServicesFromReservation(reservationDetails["id"], [service_alias])
api.AddResourcesToReservation(reservationDetails["id"], [resource_name], share_resource)
api.SetReservationResourcePosition(reservationDetails["id"], resource_name, service_position.X, service_position.Y)
api.SetConnectorsInReservation(reservationDetails["id"], connectors)