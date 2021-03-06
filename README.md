# AppWashPy

Inofficial API Client for appWash by Miele.

## Usage
Check the Juypter-Notebook (example.ipynb) for more code examples!

### Installation
Install the package via pip:
```shell
$ pip install appwashpy
```

### Get Started
Import and initialize the AppWash-Client with your Email and Password:  
Optionally pass the ID of your default location. See below how to obtain it. 
```Python
from appwashpy import AppWash

appwash = AppWash("example@mail.org", "superstrongpassword", location_id="12345")
```

### Information about the Location
Get the Location Object either to the location you specified in the AppWash-Object or to the given parameter.  
It contains information like the name and available services and their prices.

```Python
location = appwash.location()
# or
location = appwash.location("12345")
```
#### Obtaining the Location ID
If you login at [appwash.com](https://appwash.com/en/) you should get redirected to your default location.  
The URL then contains the Location ID. For example *12345* for h<span>ttps://</span>appwash.com/myappwash/location/?id=*12345*

### Services
#### List of Available Services
Get a list of available services/machines at your default or the specified location.  
The Service Object contains among other things the type of service (washing machine, dryer, ...) and the current status (available, occupied, ...).
```Python
services = appwash.services()
# or 
services = appwash.services("12345")
```
#### Get Specific Service by ID
Get a specific Service Object.
```Python
services = appwash.services("12345")
```

#### Buy the Service
The service can be bought directly through the .buy() method or via the AppWash-Object.  
This will bill you the corresponding price!
```Python
services[0].buy()
# or
appwash.buy("12345")
```

Be careful, calling this function multiple times cancels the previous service and bills you again.  
No warranty for freedom from errors and no compensation for damages incurred.

## Donations
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/fapfaff)
