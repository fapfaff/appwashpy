import pytest
from appwashpy import (
    AppWash,
    Location,
    Service,
    LOCATION_TYPE,
    SERVICE_TYPE,
    check_credentials,
)
from appwashpy.common.enums import STATE
from appwashpy.common.errors import AppWashApiError, WrongCredentialsError

EMAIL = "example@mail.org"
PASSWORD = "abcdefgh"
LOCATION_ID = "11111"
TOKEN = "1111111:11111111111:1111"
SERVERTIME = 1657791333
SERVICE_ID = "12345"


@pytest.fixture
def appwash(mocker, authentication_successful_result) -> AppWash:
    def mock_perform_request(self):
        self._response = authentication_successful_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash = AppWash(EMAIL, PASSWORD)
    appwash._authenticate()
    return appwash


@pytest.fixture
def service(mocker, services_result, appwash) -> Service:
    def mock_perform_request(self):
        self._response = services_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    services = appwash.services(LOCATION_ID)
    return services[0]


@pytest.fixture
def authentication_successful_result():
    """Sample result for Authentication Request"""
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": SERVERTIME,
        "activeSessions": [],
        "login": {
            "email": EMAIL,
            "username": EMAIL,
            "externalId": "123456789",
            "language": "EN",
            "token": TOKEN,
            "offlineAllowed": True,
            "manageOthers": True,
            "administrator": True,
            "viewInvoice": True,
            "viewTransactionHistory": False,
            "viewProducts": False,
            "apiMessagePermission": True,
            "correctionAllowed": False,
            "installer": False,
            "startMultiple": True,
            "startForOthers": False,
            "timeForReview": False,
        },
    }


@pytest.fixture
def authentication_wrong_credentials_result():
    """Sample result for Authentication Request with wrong credentials"""
    return {
        "errorCode": 61,
        "errorDescription": "Login failed. Please check your username and password. (code 61)",
        "token_expire_ts": 0,
        "serverTime": SERVERTIME,
    }


@pytest.fixture
def location_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": SERVERTIME,
        "data": {
            "name": "Box 220402",
            "externalId": LOCATION_ID,
            "gps": {},
            "locationTypeV2": "OTHER",
            "locationTypeObject": {"type": "OTHER", "name": "Andere"},
            "locationStatus": "PRODUCTION_PHASE",
            "durationRequired": False,
            "knownCommunicationIssues": False,
            "services": [
                {"type": "DRYER", "name": "Trockner"},
                {"type": "WASHING_MACHINE", "name": "Waschmaschine"},
            ],
            "pricing": [
                {
                    "serviceType": "WASHING_MACHINE",
                    "componentPriceObjects": [
                        {
                            "type": "UNIT_PRICE",
                            "fullPriceString": "Pro Waschgang: EUR 2.75",
                            "priceString": "EUR 2.75",
                            "costCents": 275,
                        }
                    ],
                },
                {
                    "serviceType": "DRYER",
                    "componentPriceObjects": [
                        {
                            "type": "UNIT_PRICE",
                            "fullPriceString": "Pro Trockengang: EUR 2.25",
                            "priceString": "EUR 2.25",
                            "costCents": 225,
                        }
                    ],
                },
            ],
            "products": [],
            "childLocations": [],
            "maxDaysInAdvance": 7,
            "reservedType": "NOT_RESERVABLE",
            "serviceTypes": [],
        },
    }


@pytest.fixture
def location_invalid_result():
    return {
        "errorCode": 33,
        "errorDescription": "We couldn't find this location. Please try again later. (code 33)",
        "token_expire_ts": 1658354400,
        "serverTime": SERVERTIME,
    }


@pytest.fixture
def services_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": 1657800054,
        "data": [
            {
                "externalId": "38031",
                "locationId": LOCATION_ID,
                "location": "Waschküche - Haus 2",
                "locationTopLevelName": "Ulm - Hochsträß 2",
                "serviceType": "DRYER",
                "serviceName": "Trockner",
                "unit": "Transaktion",
                "state": "AVAILABLE",
                "stateDescription": "frei",
                "requiredFields": [],
                "freeFormQuestionInt": [],
                "pricing": [
                    {
                        "serviceType": "DRYER",
                        "componentPriceObjects": [
                            {
                                "type": "UNIT_PRICE",
                                "fullPriceString": "Pro Trockengang: EUR 2.25",
                                "priceString": "EUR 2.25",
                                "costCents": 225,
                            }
                        ],
                    }
                ],
                "tariffSetName": "default",
                "gps": {},
                "reservable": "NOT_RESERVABLE",
                "reservations": [],
                "blockTimeSeconds": 900,
                "timeOfArrivalSeconds": 0,
                "checkoutTimeSeconds": 0,
                "startWithPredeterminedUsage": False,
                "optionalName": "",
            },
            {
                "externalId": "38032",
                "locationId": LOCATION_ID,
                "location": "Waschküche - Haus 2",
                "locationTopLevelName": "Ulm - Hochsträß 2",
                "serviceType": "WASHING_MACHINE",
                "serviceName": "Waschmaschine",
                "unit": "Transaktion",
                "state": "AVAILABLE",
                "stateDescription": "frei",
                "requiredFields": [],
                "freeFormQuestionInt": [],
                "pricing": [
                    {
                        "serviceType": "WASHING_MACHINE",
                        "componentPriceObjects": [
                            {
                                "type": "UNIT_PRICE",
                                "fullPriceString": "Pro Waschgang: EUR 2.75",
                                "priceString": "EUR 2.75",
                                "costCents": 275,
                            }
                        ],
                    }
                ],
                "tariffSetName": "default",
                "gps": {},
                "reservable": "NOT_RESERVABLE",
                "reservations": [],
                "blockTimeSeconds": 900,
                "timeOfArrivalSeconds": 0,
                "checkoutTimeSeconds": 0,
                "startWithPredeterminedUsage": False,
                "optionalName": "",
            },
        ],
    }


@pytest.fixture
def service_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": 1657832158,
        "data": {
            "externalId": SERVICE_ID,
            "locationId": LOCATION_ID,
            "location": "Sample Name",
            "locationTopLevelName": "SampleTopLevelName",
            "serviceType": "WASHING_MACHINE",
            "serviceName": "Waschmaschine",
            "unit": "Transaktion",
            "state": "AVAILABLE",
            "stateDescription": "frei",
            "requiredFields": [],
            "freeFormQuestionInt": [],
            "pricing": [
                {
                    "serviceType": "WASHING_MACHINE",
                    "componentPriceObjects": [
                        {
                            "type": "UNIT_PRICE",
                            "fullPriceString": "Pro Waschgang: EUR 2.50",
                            "priceString": "EUR 2.50",
                            "costCents": 250,
                        }
                    ],
                }
            ],
            "tariffSetName": "default",
            "gps": {},
            "reservable": "NOT_RESERVABLE",
            "reservations": [],
            "blockTimeSeconds": 900,
            "timeOfArrivalSeconds": 0,
            "checkoutTimeSeconds": 0,
            "startWithPredeterminedUsage": False,
            "optionalName": "",
        },
    }


@pytest.fixture
def service_buy_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658268000,
        "serverTime": SERVERTIME,
        "data": {
            "sessionId": "4114114",
            "externalId": "12345",
            "locationExternalId": LOCATION_ID,
            "locationName": "Location",
            "serviceType": "WASHING_MACHINE",
            "startDateTime": 1657714551,
            "endDateTime": 0,
            "state": "SESSION_WAIT_ON",
            "stateTranslation": {"type": "SESSION_WAIT_ON", "name": "wird gestartet"},
            "stateDescription": "wird gestartet",
            "pinCodes": [],
        },
    }


def test_create_appwash(mocker, authentication_successful_result):
    """Test if the AppWash Object gets created successfully."""

    def mock_perform_request(self):
        self._response = authentication_successful_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash = AppWash(EMAIL, PASSWORD, LOCATION_ID)
    appwash._authenticate()

    assert appwash.email == EMAIL
    assert appwash.password == PASSWORD
    assert appwash.location_id == LOCATION_ID

    assert appwash.token == TOKEN


def test_create_appwash_without_location(mocker, authentication_successful_result):
    """Test if the AppWash Object gets created successfully if no location_id is passed."""

    def mock_perform_request(self):
        self._response = authentication_successful_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash = AppWash(EMAIL, PASSWORD)

    assert appwash.location_id == None


def test_create_appwash_wrong_credentials(
    mocker, authentication_wrong_credentials_result
):
    """Test if the AppWash raises an Error if the credentials are wrong."""

    def mock_perform_request(self):
        self._response = authentication_wrong_credentials_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    with pytest.raises(WrongCredentialsError):
        AppWash(EMAIL, "")._authenticate()


def test_default_location(mocker, location_result, appwash):
    """Test if loading the default location works."""

    def mock_perform_request(self):
        self._response = location_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash.location_id = LOCATION_ID

    location = appwash.location()

    assert isinstance(location, Location)

    assert location.id == LOCATION_ID
    assert LOCATION_TYPE.has(location.location_type)
    assert location.name == "Box 220402"


def test_specific_location(mocker, location_result, appwash):
    """Test if loading a specific location works."""

    def mock_perform_request(self):
        self._response = location_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash.location_id = "999999"
    location = appwash.location(LOCATION_ID)

    assert location.id == LOCATION_ID


def test_missing_location(appwash):
    """Test if error gets thrown if neither a default nor a specific location is given."""

    with pytest.raises(ValueError):
        appwash.location()


def test_invalid_location(mocker, location_invalid_result, appwash):
    """Test if error gets thrown if the location doesn't exist"""

    def mock_perform_request(self):
        self._response = location_invalid_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    with pytest.raises(AppWashApiError):
        appwash.location("abc")


def test_services_default_location(mocker, services_result, appwash):
    """Test loading services for the default location."""

    def mock_perform_request(self):
        self._response = services_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash.location_id = LOCATION_ID

    services = appwash.services()

    assert isinstance(services, list)
    assert len(services) > 0
    for s in services:
        assert isinstance(s, Service)

    s = services[0]

    assert s.location_id == LOCATION_ID
    assert SERVICE_TYPE.has(s.type)


def test_services_missing_location(appwash):
    """Test if error gets thrown if neither a default nor a specific location is given."""

    with pytest.raises(ValueError):
        appwash.services()


def test_services_invalid_location(mocker, location_invalid_result, appwash):
    """Test if error gets thrown if the location doesn't exist"""

    def mock_perform_request(self):
        self._response = location_invalid_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    with pytest.raises(AppWashApiError):
        appwash.services("abc")


def test_get_service(mocker, service_result, appwash):
    """Test retrieving a single service."""

    def mock_perform_request(self):
        self._response = service_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    service = appwash.service("12345")

    assert isinstance(service, Service)
    assert service.location_id == LOCATION_ID
    assert SERVICE_TYPE.has(service.type)
    assert service.service_id == SERVICE_ID


def test_buy_service_by_id(mocker, service_buy_result, appwash, service):
    """Test buying a service by id."""

    def mock_service(self, service_id):
        return service

    mocker.patch("appwashpy.client.appwash.AppWash.service", mock_service)

    def mock_perform_request(self):
        self._response = service_buy_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    appwash.buy_service("12345")


def test_service_buy(mocker, service_buy_result, service):
    """Tests if service.buy() works."""

    def mock_service(self, service_id):
        return service

    mocker.patch("appwashpy.client.appwash.AppWash.service", mock_service)

    def mock_perform_request(self):
        self._response = service_buy_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    service.buy()


def test_service_wont_safe_buy_if_stoppable(mocker, service: Service):
    """Test if service will be bought if it's state is STOPPABLE or SESSION_WAIT_ON."""

    def mock_service(self, service_id):
        service.state = STATE.STOPPABLE
        return service

    mocker.patch("appwashpy.client.appwash.AppWash.service", mock_service)

    def mock_perform_request(self):
        self._response = service_buy_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    res = service.buy()

    assert res == False


def test_service_wont_safe_buy_if_session_wait_on(mocker, service: Service):
    """Test if service will be bought if it's state is STOPPABLE or SESSION_WAIT_ON."""

    def mock_service(self, service_id):
        service.state = STATE.SESSION_WAIT_ON
        return service

    mocker.patch("appwashpy.client.appwash.AppWash.service", mock_service)

    def mock_perform_request(self):
        self._response = service_buy_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    res = service.buy()

    assert res == False


def test_check_credentials_valid(mocker, authentication_successful_result):
    """Tests if check_credentials returns True with valid credentials."""

    def mock_perform_request(self):
        self._response = authentication_successful_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    assert check_credentials(EMAIL, PASSWORD)


def test_check_credentials_invalid(mocker, authentication_wrong_credentials_result):
    """Tests if check_credentials returns False with invalid credentials."""

    def mock_perform_request(self):
        self._response = authentication_wrong_credentials_result

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    assert check_credentials(EMAIL, PASSWORD) == False


def test_check_credentials_connection_error(mocker):
    """Tests if check_credentials raises an Exception when the connection fails."""

    def mock_perform_request(self):
        raise Exception()

    mocker.patch(
        "appwashpy.client.requests.ApiRequest._perform_request", mock_perform_request
    )

    with pytest.raises(Exception):
        check_credentials(EMAIL, PASSWORD)
