from dataclasses import dataclass
from appwashpy.common.enums import LOCATION_TYPE


@dataclass
class Location:
    """Representation of a AppWash location.

    Attributes:
        id: ID of the Location
        location_type: Which type of location it is.
        services: List of dicsts of available services at the location. Dicts contains "service" and "costs_cent" keys. 
        name: Name of the location.
        reservable: Wether you can reserve services at the location
        reservable_days_in_advance: How much days in advance you can reserve if allowed.

    """
    id: str
    location_type: LOCATION_TYPE
    location_status: str
    services: list
    name: str
    reservable: bool
    reservable_days_in_advance: int

    @staticmethod
    def _from_result(result: dict) -> "Location":
        services = []
        for service in result["services"]:
            # Get price of service
            price = list(
                filter(lambda p: p["serviceType"] == service["type"], result["pricing"]))[0]

            services.append({
                "service": service["type"],
                "costs_cent": price
            })

        return Location(
            id=result["externalId"],
            location_type=result["locationTypeV2"],
            location_status=result["locationStatus"],
            services=services,
            name=result["name"],
            reservable=False if result["reservedType"] == "NOT_RESERVABLE" else True,
            reservable_days_in_advance=result["maxDaysInAdvance"],
        )
