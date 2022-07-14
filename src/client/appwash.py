from src.client.requests import ApiRequest
from src.common.enums import HTTP_METHOD, SERVICE_TYPE
from src.common.helper import current_timestamp
from src.core.location import Location
from src.core.service import Service


class AppWash:
    """Entry point for the AppWashPy SDK.

    Entry point containing methods to load locations and services.
    Needs your AppWash Login credentials to handle the authentication.

    Attributes:
        email: Email Adress of your AppWash Account.
        password: Password of your AppWash Account.
        location_id (optional): The location_id of your house. Can be obtained via the website (URL-Parameter id, e.g. 11111 for https://appwash.com/myappwash/location/?id=11111)

    """
    email: str
    password: str
    location_id: str = None

    _token_expiry: int = None

    def __init__(self, email: str, password: str, location_id: str = None):
        self.email = email
        self.password = password

        if location_id != None:
            self.location_id = location_id

        self._authenticate()

    def _authenticate(self) -> None:
        """Loads a new authentication token for your Account."""
        request = ApiRequest(
            self,
            endpoint='/login',
            method=HTTP_METHOD.POST,
            body={
                "email": self.email,
                "password": self.password
            }
        )

        self._token = request.response['login']['token']
        self._token_expiry = request.response['token_expire_ts']

    @property
    def token(self) -> None:
        """Getter for the token. Automatically renews the token if the old one is expired."""
        if(self._token_expiry > current_timestamp()):
            return self._token
        else:
            self._authenticate()
            return self._token

    def location(self, location_id: str = None) -> Location:
        """Load your default or a specific location.

        Attributes:
            location_id (optional): The location_id of your house. Can be seen in the appwash URL. Uses the location_id of the Objekt if not specified.  
            """
        location_id = location_id if location_id != None else self.location_id

        req = ApiRequest(
            self, endpoint=f"/locations/split/{location_id}", method=HTTP_METHOD.GET)

        return Location._from_result(req.response["data"])

    def services(self, location_id: str = None, service_type: SERVICE_TYPE = None) -> Service:
        """Load the available services at your house.

        Attributes:
            location_id (optional): The location_id of your house. Can be seen in the appwash URL. Uses the location_id of the Objekt if not specified.
        """
        location_id = location_id if location_id != None else self.location_id
        body = {"serviceType": service_type} if service_type != None else {}

        req = ApiRequest(
            self, endpoint=f"/location/{location_id}/connectorsv2", method=HTTP_METHOD.POST, body=body)

        services = []
        for service in req.response["data"]:
            services.append(Service._from_result(self, service))

        return services

    def buy_service(self, service_id: str) -> None:
        """Buy the service with the specified ID. 

        Be careful, calling this function multiple times cancels the previous service and bill you again.
        No warranty for freedom from errors and no compensation for damages incurred.
        """
        body = {"sourceChannel": "WEBSITE"}
        req = ApiRequest(
            self, endpoint=f'/connector/{service_id}/start', method=HTTP_METHOD.POST, body=body)
