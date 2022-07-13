from dataclasses import dataclass
from appwash.common.enums import LOCATION_TYPE


@dataclass
class Location:
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
                "costsCent": price
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
