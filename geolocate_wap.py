from winreg import *
import requests
import json
import argparse
import sys

# Convert a mac string into ":" separated octets
def convert_to_mac(mac):
    return ":".join([mac[i:(i + 2)] for i in range(0, len(mac), 2)])


# Gets a list of networks this device has conencted to from the Windows registry (optional for Windows devices)
def get_networks():
    net = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    # Counter is used to iterate through list of subkeys
    counter = 0
    # Dictionary of Network names and MAC addresses
    dict = {}
    while True:
        try:
            guid = EnumKey(key, counter)
            counter += 1
            net_key = OpenKey(key, guid)
            mac_address, mac_type = QueryValueEx(net_key, "DefaultGatewayMac")
            mac_address = convert_to_mac(mac_address.hex())
            net_name, net_type = QueryValueEx(net_key, "Description")
            dict[net_name] = mac_address       
        except:
            return dict


# Requires an API key which can be obtained from: https://wigle.net/
def locate_mac(mac_address):
    mac = mac_address.replace(":", "%3A")
    url = f"https://api.wigle.net/api/v2/network/detail?netid={mac}"
    headers = {
        "Authorization" : "Basic <INSERT API KEY HERE>",
        "Accept" : "application/json"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    results = data["results"][0]
    latitude = results["trilat"]
    longitude = results["trilong"]
    ssid = results["ssid"]
    encryption = results["encryption"]
    country = results["country"]
    region = results["region"]
    city = results["city"]
    road = results["road"]
    postalcode = results["postalcode"]

    print(f"[+] Details on {mac_address}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"SSID: {ssid}")
    print(f"Encryption: {encryption}")
    print(f"Road Name: {road}")
    print(f"City: {city}")
    print(f"Postal Code: {postalcode}")
    print(f"Region: {region}")
    print(f"Country: {country}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mac", dest="mac", help="Specify the MAC address of your target.")

    if len(sys.argv) != 3:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    mac = args.mac
    locate_mac(mac)


if __name__ == "__main__":
    main()


