"""
dalion_api_get_control_device.py

Allows retrieving a DALI-2 control device; sensor, button.
The parameters can be passed via command line arguments or via user input.

Usage - User input
dalion_api_get_control_device.py

Usage - Command line arguments
dalion_api_get_control_device.py ip channel control-device-index id

ip: The DALION IP address.
channel: The channel number, 1-4.
control-device-index: Control device index 0-63.
id: The variable id.

Exemples:
Get the light intensity of the control device 0 on the channel 1.
dalion_api_get_control_device.py 192.168.0.210 1 0 ls

Get the occupancy of the control device 0 on the channel 1.
dalion_api_get_control_device.py 192.168.0.210 1 0 os
"""

import sys
import urllib.request
import urllib.parse
import json


DEF_ID = [
    {"id": "os",   "name": "Occupancy state"},
    {"id": "ls",   "name": "Light"}
]

"""
"" List of id.
"""


def valid_arguments(valip, valch, valii, valid):
    """
    Valid the arguments
    """

    bvalid = True

    # Type converssion
    valch = int(valch)
    valii = int(valii)

    # Valid the parameters

    # Valid - IP
    if valip == "":
        print("IP is invalid.")
        bvalid = False
    # Valid - Channel
    if (valch < 1) | (valch > 4):
        print("Channel number is invalid.")
        bvalid = False
    # Valid - Index
    # Control device index
    if (valii < 0) | (valii > 63):
        print("Control device index is invalid.")
        bvalid = False
    # Valid - id
    if valid == "":
        print("id is invalid.")
        bvalid = False

    return bvalid


def prepare_url(valip, valch):
    """
    Prepare the URL
    """

    ## Parameter - IP
    url = "http://" + valip

    ## Parameter - URL - action
    url += "/api/v100/dali_devices.ssi?action=get"

    ## Parameter - Channel
    url += "&ch=" + valch

    return url


def send_request(url):
    """
    Send the HTTP GET request.
    """

    response = urllib.request.urlopen(url).read()

    return response


def parse_response(response, valii, valid):
    """
    Parse the response
    """

    response = json.loads(response)
	
    for device in response['data']['control_devices']['devices']:
        if device['ii'] == valii:
            if valid == 'os':
                return device['os']
            if valid == 'ls':
                return device['ls']
    return ""


def main():
    """
    main
    """

    # Parse the command arguments
    if len(sys.argv) != 5:
        # User Input

        # Input - IP
        valip = input("Enter DALION IP address: ")

        # Input - Destination (channel number)
        valch = input("Enter channel number (1-4): ")

        ## Input - Control device index
        valii = -1
        # Input - Lamp index
        valii = input("Enter control device index (0-63): ")

        # Input - Value choice
        print("Select type: ")
        index = 0
        for vid in DEF_ID:
            index = index + 1

            vstr =  "    "
            vstr += str(index)
            vstr += ") "
            vstr += (" " if index < 10 else "")
            vstr += vid['name']
            print(vstr)
        valvi = input("    ")
        valvi = int(valvi) - 1
        vid = DEF_ID[valvi]
        valid = vid['id']
    else:
        # Command line arguments

        # ip
        valip = sys.argv[1]
        # channel
        valch = sys.argv[2]
        # control device index
        valii = sys.argv[3]
        # variable id
        valid = sys.argv[4]

        # Find the variable for valid
        index = 0
        for vid in DEF_ID:
            if vid['id'] == valid:
                valvi = index
                break
            index = index + 1
        vid = DEF_ID[valvi]


    # Valid arguments
    bvalid = valid_arguments(valip, valch, valii, valid)
    if bvalid is False:
        sys.exit()

    # Prepare the URL
    url = prepare_url(valip, valch)

    # Print the URL
    print("")
    print("Request: ")
    print(url)
    print("")

    # Send the request
    response = send_request(url)

    # Parse the response
    response = parse_response(response, valii, valid)

    # Print the response
    print("Response: ")
    print(response)
    print("")


if __name__ == '__main__':
    main()
