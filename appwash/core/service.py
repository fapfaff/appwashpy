from dataclasses import dataclass
from appwash.common.enums import SERVICE_TYPE, STATE


@dataclass
class Service:
    service_id: str
    location_id: str
    type: SERVICE_TYPE
    name: str
    cost_cents: int
    reservable: bool
    state: STATE
    session_start: int

    @staticmethod
    def _from_result(result: dict) -> "Service":
        return Service(
            service_id=result["externalId"],
            location_id=result["locationId"],
            type=result["serviceType"],
            name=result["serviceName"],
            cost_cents=result["pricing"][0]["componentPriceObjects"][0]["costCents"],
            reservable=False if result["reservable"] == "NOT_RESERVABLE" else True,
            session_start=result["lastSessionStart"] if "lastSessionStart" in result else None,
            state=result["state"]
        )
