from appwashpy.client.requests import ApiRequest
from appwashpy.common.enums import HTTP_METHOD, SERVICE_TYPE
from appwashpy.common.errors import AppWashApiError, WrongCredentialsError
from appwashpy.common.helper import current_timestamp
from appwashpy.core.location import Location
from appwashpy.core.service import Service


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

    def authenticate(self) -> None:
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

        error_code = request.response["errorCode"]
        if error_code == 0:
            self._token = request.response['login']['token']
            self._token_expiry = request.response['token_expire_ts']
        elif error_code == 61:
            raise WrongCredentialsError(
                error_code, request.response["errorDescription"], self.email, self.password)
        else:
            raise AppWashApiError(
                error_code, request.response["errorDescription"])

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

        # Use either location_id parameter or default location_id
        if location_id == None and self.location_id == None:
            raise ValueError(
                "Either set a default location_id or pass a location_id to the method.")
        location_id = location_id if location_id != None else self.location_id

        request = ApiRequest(
            self, endpoint=f"/locations/split/{location_id}", method=HTTP_METHOD.GET)

        if request.response["errorCode"] != 0:
            raise AppWashApiError(
                request.response["errorCode"], request.response["errorDescription"])

        return Location._from_result(request.response["data"])

    def services(self, location_id: str = None, service_type: SERVICE_TYPE = None) -> list[Service]:
        """Load the available services at your house.

        Attributes:
            location_id (optional): The location_id of your house. Can be seen in the appwash URL. Uses the location_id of the Objekt if not specified.
        """
        # Use either location_id parameter or default location_id
        if location_id == None and self.location_id == None:
            raise ValueError(
                "Either set a default location_id or pass a location_id to the method.")
        location_id = location_id if location_id != None else self.location_id

        body = {"serviceType": service_type} if service_type != None else {}

        request = ApiRequest(
            self, endpoint=f"/location/{location_id}/connectorsv2", method=HTTP_METHOD.POST, body=body)

        if request.response["errorCode"] != 0:
            raise AppWashApiError(
                request.response["errorCode"], request.response["errorDescription"])

        services = []
        for service in request.response["data"]:
            services.append(Service._from_result(self, service))

        return services

    def service(self, service_id: str) -> Service:
        """Load a specific service by ID.

        Attributes:
            serivce_id: ID of the service"""

        request = ApiRequest(
            self, endpoint=f"//connector/{service_id}", method=HTTP_METHOD.GET)

        if request.response["errorCode"] != 0:
            raise AppWashApiError(
                request.response["errorCode"], request.response["errorDescription"])

        return Service._from_result(self, request.response["data"])

    def buy_service(self, service_id: str) -> None:
        """Buy the service with the specified ID. 

            Be careful, calling this function multiple times cancels the previous service and bill you again.
            No warranty for freedom from errors and no compensation for damages incurred.

        Attributes:
            serivce_id: ID of the service
        """
        body = {"sourceChannel": "WEBSITE"}
        request = ApiRequest(
            self, endpoint=f'/connector/{service_id}/start', method=HTTP_METHOD.POST, body=body)

        if request.response["errorCode"] != 0:
            raise AppWashApiError(
                request.response["errorCode"], request.response["errorDescription"])


def check_credentials(email: str, password: str) -> bool:
    """Checks wether the credentials are valid."""
    request = ApiRequest(
        None,
        endpoint='/login',
        method=HTTP_METHOD.POST,
        body={
            "email": email,
            "password": password
        }
    )
    error_code = request.response["errorCode"]
    if error_code == 0:
        return True
    if error_code == 61:
        return False
    else:
        raise AppWashApiError(
            error_code, request.response["errorDescription"])
