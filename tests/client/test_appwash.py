import pytest
from src import AppWash
from src.common.enums import LOCATION_TYPE, SERVICE_TYPE
from src.common.errors import AppWashApiError, WrongCredentialsError
from src.core.location import Location
from src.core.service import Service

email = "example@mail.org"
password = "abcdefgh"
location_id = "11111"
token = "1111111:11111111111:1111"
servertime = 1657791333


@pytest.fixture
def appwash(mocker, authentication_successful_result) -> AppWash:
    def mock_perform_request(self):
        self._response = authentication_successful_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash = AppWash(email, password)
    return appwash


@pytest.fixture
def service(mocker, services_result, appwash) -> Service:

    def mock_perform_request(self):
        self._response = services_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    services = appwash.services(location_id)
    return services[0]


@pytest.fixture
def authentication_successful_result():
    """Sample result for Authentication Request"""
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": servertime,
        "activeSessions": [],
        "login": {
            "email": email,
            "username": email,
            "externalId": "123456789",
            "language": "EN",
            "token": token,
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
            "timeForReview": False
        }
    }


@pytest.fixture
def authentication_wrong_credentials_result():
    """Sample result for Authentication Request with wrong credentials"""
    return {
        "errorCode": 61,
        "errorDescription": "Login failed. Please check your username and password. (code 61)",
        "token_expire_ts": 0,
        "serverTime": servertime
    }


@pytest.fixture
def location_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658354400,
        "serverTime": servertime,
        "data": {
            "name": "Box 220402",
            "externalId": location_id,
            "gps": {},
            "locationTypeV2": "OTHER",
            "locationTypeObject": {
                "type": "OTHER",
                "name": "Andere"
            },
            "locationStatus": "PRODUCTION_PHASE",
            "durationRequired": False,
            "knownCommunicationIssues": False,
            "services": [
                {
                    "type": "DRYER",
                    "name": "Trockner"
                },
                {
                    "type": "WASHING_MACHINE",
                    "name": "Waschmaschine"
                }
            ],
            "pricing": [
                {
                    "serviceType": "WASHING_MACHINE",
                    "componentPriceObjects": [
                        {
                            "type": "UNIT_PRICE",
                            "fullPriceString": "Pro Waschgang: EUR 2.75",
                            "priceString": "EUR 2.75",
                            "costCents": 275
                        }
                    ]
                },
                {
                    "serviceType": "DRYER",
                    "componentPriceObjects": [
                        {
                            "type": "UNIT_PRICE",
                            "fullPriceString": "Pro Trockengang: EUR 2.25",
                            "priceString": "EUR 2.25",
                            "costCents": 225
                        }
                    ]
                }
            ],
            "products": [],
            "childLocations": [],
            "maxDaysInAdvance": 7,
            "reservedType": "NOT_RESERVABLE",
            "serviceTypes": []
        }
    }


@pytest.fixture
def location_invalid_result():
    return {
        "errorCode": 33,
        "errorDescription": "We couldn't find this location. Please try again later. (code 33)",
        "token_expire_ts": 1658354400,
        "serverTime": servertime
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
                "locationId": location_id,
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
                "locationId": location_id,
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
def service_buy_result():
    return {
        "errorCode": 0,
        "errorDescription": "",
        "token_expire_ts": 1658268000,
        "serverTime": servertime,
        "data": {
            "sessionId": "4114114",
            "externalId": "12345",
            "locationExternalId": location_id,
            "locationName": "Location",
            "serviceType": "WASHING_MACHINE",
            "startDateTime": 1657714551,
            "endDateTime": 0,
            "state": "SESSION_WAIT_ON",
            "stateTranslation": {
                "type": "SESSION_WAIT_ON",
                "name": "wird gestartet"
            },
            "stateDescription": "wird gestartet",
            "pinCodes": []
        }
    }


def test_create_appwash(mocker, authentication_successful_result):
    """Test if the AppWash Object gets created successfully."""

    def mock_perform_request(self):
        self._response = authentication_successful_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash = AppWash(email, password, location_id)

    assert appwash.email == email
    assert appwash.password == password
    assert appwash.location_id == location_id

    assert appwash.token == token


def test_create_appwash_without_location(mocker, authentication_successful_result):
    """Test if the AppWash Object gets created successfully if no location_id is passed."""

    def mock_perform_request(self):
        self._response = authentication_successful_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash = AppWash(email, password)

    assert appwash.location_id == None


def test_create_appwash_wrong_credentials(mocker, authentication_wrong_credentials_result):
    """Test if the AppWash raises an Error if the credentials are wrong."""

    def mock_perform_request(self):
        self._response = authentication_wrong_credentials_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    with pytest.raises(WrongCredentialsError):
        AppWash(email, "")


def test_default_location(mocker, location_result, appwash):
    """Test if loading the default location works."""

    def mock_perform_request(self):
        self._response = location_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash.location_id = location_id

    location = appwash.location()

    assert isinstance(location, Location)

    assert location.id == location_id
    assert LOCATION_TYPE.has(location.location_type)
    assert location.name == "Box 220402"


def test_specific_location(mocker, location_result, appwash):
    """Test if loading a specific location works."""

    def mock_perform_request(self):
        self._response = location_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash.location_id = "999999"
    location = appwash.location(location_id)

    assert location.id == location_id


def test_missing_location(appwash):
    """Test if error gets thrown if neither a default nor a specific location is given."""

    with pytest.raises(ValueError):
        appwash.location()


def test_invalid_location(mocker, location_invalid_result, appwash):
    """Test if error gets thrown if the location doesn't exist"""

    def mock_perform_request(self):
        self._response = location_invalid_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    with pytest.raises(AppWashApiError):
        appwash.location("abc")


def test_services_default_location(mocker, services_result, appwash):
    """Test loading services for the default location."""

    def mock_perform_request(self):
        self._response = services_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash.location_id = location_id

    services = appwash.services()

    assert isinstance(services, list)
    assert len(services) > 0
    for s in services:
        assert isinstance(s, Service)

    s = services[0]

    assert s.location_id == location_id
    assert SERVICE_TYPE.has(s.type)


def test_services_missing_location(appwash):
    """Test if error gets thrown if neither a default nor a specific location is given."""

    with pytest.raises(ValueError):
        appwash.services()


def test_services_invalid_location(mocker, location_invalid_result, appwash):
    """Test if error gets thrown if the location doesn't exist"""

    def mock_perform_request(self):
        self._response = location_invalid_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    with pytest.raises(AppWashApiError):
        appwash.services("abc")


def test_buy_service_no_id(mocker, service_buy_result, appwash):
    """Test if error gets thrown if the location doesn't exist"""

    def mock_perform_request(self):
        self._response = service_buy_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    appwash.buy_service("12345")


def test_service_buy(mocker, service_buy_result, service):
    def mock_perform_request(self):
        self._response = service_buy_result
    mocker.patch("src.client.requests.ApiRequest._perform_request",
                 mock_perform_request)

    service.buy()
