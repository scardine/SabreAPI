import time
import requests
import base64
import types
import re
import warnings

class Sabre(object):
    token = None
    APIS = {
        'v1.shop.flights.fares' : ('GET', '/v1/shop/flights/fares', 'Lead Price Calendar API'),
        'v1.historical.shop.flights.fares' : ('GET', '/v1/historical/shop/flights/fares', 'Low Fare History API'),
        'v1.lists.supported.shop.flights.origins.destinations' : ('GET', '/v1/lists/supported/shop/flights/origins-destinations', 'City Pairs Lookup API'),
        'v1.shop.calendar.flights' : ('POST', '/v1.8.1/shop/calendar/flights', 'Advanced Calendar Search API'),
        'v1.lists.supported.pointofsalecountries' : ('GET', '/v1/lists/supported/pointofsalecountries', 'Point of Sale Country Code Lookup API'),
        'v1.lists.supported.shop.themes.theme' : ('GET', '/v1/lists/supported/shop/themes/{theme}', 'Theme Airport Lookup API'),
        'v1.auth.token' : ('POST', '/v1/auth/token', 'Authentication Request'),
        'v1.lists.utilities.airlines.alliances' : ('GET', '/v1/lists/utilities/airlines/alliances/', 'Airline Alliance Lookup API'),
        'v1.historical.flights.fares' : ('GET', '/v1/historical/flights/fares', 'Fare Range API'),
        'v1.forecast.flights.fares' : ('GET', '/v1/forecast/flights/fares', 'Low Fare Forecast API'),
        'v1.lists.supported.cities' : ('GET', '/v1/lists/supported/cities', 'Multi-Airport City Lookup API'),
        'v1.lists.top.destinations' : ('GET', '/v1/lists/top/destinations', 'Top Destinations API'),
        'v1.lists.supported.countries' : ('GET', '/v1/lists/supported/countries', 'Countries Lookup API'),
        'v1.lists.supported.cities.airports' : ('GET', '/v1/lists/supported/cities/{city}/airports/', 'Airports at Cities Lookup API'),
        'v1.shop.altdates.flights' : ('POST', '/v1.8.6/shop/altdates/flights', 'Alternate Date API'),
        'v1.lists.supported.shop.themes' : ('GET', '/v1/lists/supported/shop/themes/', 'Travel Theme Lookup API'),
        'v1.lists.supported.historical.seasonality.airports' : ('GET', '/v1/lists/supported/historical/seasonality/airports', 'Travel Seasonality Airports Lookup API'),
        'v2.shop.cars' : ('POST', '/v2.4.0/shop/cars', 'Car Availability (beta) API'),
        'v3.book.flights.seatmaps' : ('POST', '/v3.0.0/book/flights/seatmaps?mode=seatmaps', 'Seat Map (beta) API'),
        'v1.historical.flights.destination.seasonality' : ('GET', '/v1/historical/flights/{destination}/seasonality', 'Travel Seasonality API'),
        'v1.lists.utilities.airlines.' : ('GET', '/v1/lists/utilities/airlines/', 'Airline Lookup API'),
        'v1.lists.utilities.aircraft.equipment' : ('GET', '/v1/lists/utilities/aircraft/equipment/', 'Aircraft Equipment Lookup API'),
        'v1.shop.flights' : ('GET', '/v1/shop/flights', 'InstaFlights Search API'),
    }
    
    def __init__(self, client_id, client_secret, server='https://api.test.sabre.com'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.server = server
        self.credentials = self.encode_credentials()  
        
        class Container(object):
            def __call__(self, *args, **kwargs):
                return self._call(self.endpoint, *args, **kwargs)
            
        self.api = Container()
        
        for api_name, (method, endpoint, description) in self.APIS.items():
            parts = api_name.split('.')
            obj = self.api
            for part in parts:
                if getattr(obj, part, None) is None:
                    setattr(obj, part, Container())
                obj = getattr(obj, part)
                    
            def fn(s, endpoint, *args, **kwargs):
                e = endpoint
                if '{' in endpoint:
                    e = endpoint.format(**kwargs)
                    for arg in re.findall(r'{(\w+)}', endpoint):
                        del kwargs[arg]
                
                if method == 'GET':
                    kwargs = {"params": kwargs}
                else:
                    kwargs = {"data": kwargs}
                    
                result = self.call_method(method.lower(), self.server + e, *args, **kwargs)
                assert result.status_code is 200, u"Got a {} (expecting 200): {}".format(result.status_code, result.json())
                return result.json()
            
            obj.endpoint = endpoint
            obj._call = types.MethodType(fn, obj, Container)
        
    def is_valid(self):
        self.last_check = time.time()
        if self.token and self.token['expires'] < self.last_check:
            return True
        return False
        
    def get_token(self):
        if self.is_valid():
            return self.token
        headers = {'Authorization': 'Basic ' + self.credentials}
        params = {'grant_type': 'client_credentials'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = requests.post(self.server + '/v1/auth/token', headers=headers, data=params)
        assert r.status_code is 200, 'Expecting 200 answer, got {} instead'.format(r.status_code)
        self.token = r.json()
        self.token['expires'] = self.last_check + self.token['expires_in']
        return self.token
        
    def encode_credentials(self):
        return base64.b64encode("{client_id}:{client_secret}".format(
                   client_id=base64.b64encode(self.client_id),
                   client_secret=base64.b64encode(self.client_secret)))
    
    def call_method(self, method, *args, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update(Authorization='Bearer ' + self.get_token()[u'access_token'])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return getattr(requests, method)(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        return self.call_method('get', *args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.call_method('post', *args, **kwargs)
    
    def api_list(self):
        for api_name, (method, endpoint, description) in self.APIS.items():
            print(u"{}: {} (endpoint: {} {})".format(api_name, description, method, endpoint))
