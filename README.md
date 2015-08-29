# SabreAPI

Python bindings to the Sabre REST API (https://developer.sabre.com/docs/read/REST_APIs)

This is a quick hack for a Hackathon sponsored by Sabre. Feel free to send a PR.

## Usage

Get your client id and secret at https://developer.sabre.com/apps/mykeys

    sabre = Sabre(client_id, client_secret)
    country_list = sabre.api.v1.lists.supported.countries()
    
The method list is:

    sabre.APIS.keys()

