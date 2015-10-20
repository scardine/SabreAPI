# SabreAPI

Python bindings to the Sabre REST API (https://developer.sabre.com/docs/read/REST_APIs)

This is a quick hack for a Hackathon sponsored by Sabre (the event was sponsored, not this project). Lots of room for improvement, feel free to send a PR.

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
    
Unfortunately, looks like their API is not reflexive. The method list is:

    sabre.api_list()
    
 * v1.shop.flights.fares: Lead Price Calendar API (endpoint: GET /v1/shop/flights/fares)
 * v1.historical.shop.flights.fares: Low Fare History API (endpoint: GET /v1/historical/shop/flights/fares)
 * v1.lists.supported.shop.flights.origins.destinations: City Pairs Lookup API (endpoint: GET /v1/lists/supported/shop/flights/origins-destinations)
 * v1.lists.supported.countries: Countries Lookup API (endpoint: GET /v1/lists/supported/countries)
 * v1.lists.supported.pointofsalecountries: Point of Sale Country Code Lookup API (endpoint: GET /v1/lists/supported/pointofsalecountries)
 * v1.lists.supported.shop.themes.theme: Theme Airport Lookup API (endpoint: GET /v1/lists/supported/shop/themes/{theme})
 * v1.auth.token: Authentication Request (endpoint: POST /v1/auth/token)
 * v1.lists.utilities.airlines.alliances: Airline Alliance Lookup API (endpoint: GET /v1/lists/utilities/airlines/alliances/)
 * v1.historical.flights.fares: Fare Range API (endpoint: GET /v1/historical/flights/fares)
 * v1.forecast.flights.fares: Low Fare Forecast API (endpoint: GET /v1/forecast/flights/fares)
 * v1.lists.supported.cities: Multi-Airport City Lookup API (endpoint: GET /v1/lists/supported/cities)
 * v1.lists.supported.cities.airports: Airports at Cities Lookup API (endpoint: GET /v1/lists/supported/cities/{city}/airports/)
 * v1.shop.calendar.flights: Advanced Calendar Search API (endpoint: POST /v1.8.1/shop/calendar/flights)
 * v1.lists.top.destinations: Top Destinations API (endpoint: GET /v1/lists/top/destinations)
 * v1.shop.altdates.flights: Alternate Date API (endpoint: POST /v1.8.6/shop/altdates/flights)
 * v1.lists.supported.shop.themes: Travel Theme Lookup API (endpoint: GET /v1/lists/supported/shop/themes/)
 * v1.lists.supported.historical.seasonality.airports: Travel Seasonality Airports Lookup API (endpoint: GET /v1/lists/supported/historical/seasonality/airports)
 * v2.shop.cars: Car Availability (beta) API (endpoint: POST /v2.4.0/shop/cars)
 * v3.book.flights.seatmaps: Seat Map (beta) API (endpoint: POST /v3.0.0/book/flights/seatmaps?mode=seatmaps)
 * v1.historical.flights.destination.seasonality: Travel Seasonality API (endpoint: GET /v1/historical/flights/{destination}/seasonality)
 * v1.lists.utilities.airlines.: Airline Lookup API (endpoint: GET /v1/lists/utilities/airlines/)
 * v1.lists.utilities.aircraft.equipment: Aircraft Equipment Lookup API (endpoint: GET /v1/lists/utilities/aircraft/equipment/)
 * v1.shop.flights: InstaFlights Search API (endpoint: GET /v1/shop/flights)    

