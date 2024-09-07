import requests
import socket

def ip_address_tracker(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "success":
        country = data["country"]
        city = data["city"]
        isp = data["isp"]
        longitude = data["lon"]
        latitude = data["lat"]
        zip_code = data["zip"]
        region = data["regionName"]
        timezone= data["timezone"]

        return {
            'is_fetched': True,
            'ip_address': ip_address,
            'country': country,
            'city': city,
            'isp': isp,
            'longitude': longitude,
            'latitude': latitude,
            'zip_code': zip_code,
            'region': region,
            'timezone': timezone
        }
    else:
        return {'is_fetched': False}

def url_to_ip(url1):
    try:
        ip_address1 = socket.gethostbyname(url1)
        return ip_address1
    except socket.gaierror:
        return "Error: Unable to resolve host."