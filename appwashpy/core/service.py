from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from appwashpy.common.enums import SERVICE_TYPE, STATE

# Fix cyclical import because of type annotation
if TYPE_CHECKING:
    from appwashpy import AppWash


@dataclass
class Service:
    """Representation of an AppWash Service.

    Attributes:
        service_id: ID of the service.
        location_id: ID of the location this service belongs to.
        type: Type of the Service. Known Types: WASHING_MACHINE, DRYER, ELECTRICITY.
        name: Name of the service.
        cost_cents: Price of the service in cents.
        reservable: Wether the service is reservable.
        state: Current state of the service. Known States: AVAILABLE, OCCUPIED, FAULTED, SESSION_WAIT_ON
        session_start: Timestamp of when the service was started, if it is currently activate.

    """

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
            session_start=result["lastSessionStart"]
            if "lastSessionStart" in result
            else None,
            state=result["state"],
        )

    def buy(self, safe: bool = True) -> None:
        """Buys the service.

        Be careful, calling this function multiple times cancels the previous service and bill you again.
        No warranty for freedom from errors and no compensation for damages incurred.
        """
        self._client.buy_service(self.service_id, safe)

    def stop(self) -> None:
        """Buys the service."""
        self._client.stop_service(self.service_id)
