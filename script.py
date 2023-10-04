import requests
import urllib.parse
import datetime
import json
from creds import credentials


# Getting the LWA access token using the Seller Central App credentials. The token will be valid for 1 hour until it expires.
token_response = requests.post(
    "https://api.amazon.com/auth/o2/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": credentials["refresh_token"],
        "client_id": credentials["lwa_app_id"],
        "client_secret": credentials["lwa_client_secret"],
    },
)
access_token = token_response.json()["access_token"]

# North America SP API endpoint (from https://developer-docs.amazon.com/sp-api/docs/sp-api-endpoints)
endpoint = "https://sellingpartnerapi-na.amazon.com"

# US Amazon Marketplace ID (from https://developer-docs.amazon.com/sp-api/docs/marketplace-ids)
marketplace_id = "ATVPDKIKX0DER"

# Downloading orders (from https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders)
# the getOrders operation is a HTTP GET request with query parameters
request_params = {
    "MarketplaceIds": marketplace_id,  # required parameter
    "CreatedAfter": (
        datetime.datetime.now() - datetime.timedelta(days=30)
    ).isoformat(),  # orders created since 30 days ago, the date needs to be in the ISO format
}

orders = requests.get(
    endpoint
    + "/orders/v0/orders"  # getOrders operation path (from https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders)
    + "?"
    + urllib.parse.urlencode(request_params),  # encode query parameters to the URL
    headers={
        "x-amz-access-token": access_token,  # access token from LWA, every SP API request needs to have this header
    },
)

# pretty print the JSON response
print(json.dumps(orders.json(), indent=2))