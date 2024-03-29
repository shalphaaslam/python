
# this is working - just to quickly test keycloak connectivity
import requests

url = 'http://192.168.160.1:8080/auth/realms/master/protocol/openid-connect/token'
data = {
    'client_id': 'account',
    'grant_type': 'password',
    'client_secret': 'z0oj3sxJtm3WGeqkxa9d5DwSJWxIUlt2',
    'scope': 'openid',
    'username': 'admin',
    'password': 'password'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad status codes (4xx or 5xx)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
