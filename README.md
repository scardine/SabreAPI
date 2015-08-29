# SabreAPI

Python bindings to the Sabre REST API (https://developer.sabre.com/docs/read/REST_APIs)

This is a quick hack for a Hackathon sponsored by Sabre. Feel free to send a PR.

## Usage

Get your client id and secret at https://developer.sabre.com/apps/mykeys

    sabre = Sabre(client_id, client_secret)
    country_list = sabre.api.v1.lists.supported.countries()
    
    fares = sabre.api.v1.historical.flights.fares(
        origin='LAX', 
        destination='JFK', 
        earliestdeparturedate='2015-08-30', 
        latestdeparturedate='2015-08-30', 
        lengthofstay=1,
    )
    
When the endpoint path is in the form `/v1/foo/{bar}/` you must supply an extra parameter with the same name of the path component, like `sabre.api.v1.foo(bar='spam')` (parameter order is not important). Example:

    # /v1/lists/supported/cities/{city}/airports/
    sabre.api.v1.lists.supported.cities.airports(city='RIO')
    
The method list is:

    sabre.APIS.keys()

