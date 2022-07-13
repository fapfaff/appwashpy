from dataclasses import dataclass, field
from appwash.common.enums import SERVICE_TYPE, STATE
from typing import TYPE_CHECKING

# Fix cyclical import because of type annotation
if TYPE_CHECKING:
    from appwash import AppWash


@dataclass
class Service:
    _client: "AppWash" = field(repr=False)
    service_id: str
    location_id: str
    type: SERVICE_TYPE
    name: str
    cost_cents: int
    reservable: bool
    state: STATE
    session_start: int

    @staticmethod
    def _from_result(client: "AppWash", result: dict) -> "Service":
        return Service(
            _client=client,
            service_id=result["externalId"],
            location_id=result["locationId"],
            type=result["serviceType"],
            name=result["serviceName"],
            cost_cents=result["pricing"][0]["componentPriceObjects"][0]["costCents"],
            reservable=False if result["reservable"] == "NOT_RESERVABLE" else True,
            session_start=result["lastSessionStart"] if "lastSessionStart" in result else None,
            state=result["state"]
        )

    def buy(self):
        self._client.buy_service(self.service_id)
