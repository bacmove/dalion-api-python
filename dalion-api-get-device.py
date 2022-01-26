"""
dalion-api-get-device.py

Allows retrieving a lamp, group or channel.
The parameters can be passed via command line arguments or via user input.

Usage - User input
dalion-api-get-device.py

Usage - Command line arguments
dalion-api-get-device.py ip channel destination destination-index id

ip: The DALION IP address.
channel: The channel number, 1-4.
destination: 1 = lamp, 2 = group, 3 = channel.
destination-index: Lamp index 0-63, group index 0-15 or channel -1.
id: The variable id.

Exemples:
Get the light intensity of the channel 1.
dalion-api-get-device.py 192.168.0.210 1 3 -1 dval

Get the light intensity of the group 2 on the channel 1.
dalion-api-get-device.py 192.168.0.210 1 2 2 dval

Get the light intensity of the lamp 0 on the channel 1.
dalion-api-get-device.py 192.168.0.210 1 1 0 dval

Get the groups of the lamp 1 on the channel 1.
dalion-api-get-device.py 192.168.0.210 1 1 1 dvgr

Get the fade time of the lamp 0 on the channel 1.
dalion-api-get-device.py 192.168.0.210 1 1 0 dvft
#
"""

import sys
import urllib.request
import urllib.parse
import json

import device_variables


def valid_arguments(valip, valch, valc, valii, valid):
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
    if valc == 1:
        # Lamp index
        if (valii < 0) | (valii > 63):
            print("Lamp index is invalid.")
            bvalid = False
    elif valc == 2:
        # Group index
        if (valii < 0) | (valii > 15):
            print("Group index is invalid.")
            bvalid = False
    else:
        # Channel
        if valii != -1:
            print("Channel index is invalid.")
            bvalid = False
    # Valid - id
    if valid == "":
        print("id is invalid.")
        bvalid = False

    return bvalid


def prepare_url(valip, valch, valc, valii):
    """
    Prepare the URL
    """

    ## Parameter - IP
    url = "http://" + valip

    ## Parameter - URL - action
    url += "/api/v100/dali_devices.ssi?action=get_device"

    ## Parameter - Channel
    url += "&ch=" + valch

    ## Parameter - Lamp index, group index or channel
    if valc == 1:
        # Lamp index
        url += "&di=" + valii
    elif valc == 2:
        # Group index
        url += "&gi=" + valii
    else:
        # Channel
        url += "&gi=-1"

    return url


def send_request(url):
    """
    Send the HTTP GET request.
    """

    response = urllib.request.urlopen(url).read()

    return response


def parse_response(response, valid):
    """
    Parse the response
    """

    response = json.loads(response)

    for variable in response['data']['device']['variables']:
        if variable['id'] == valid:
            if variable['ty'] == 'nb10':
                return float(variable['va']) / 10
            else:
                return variable['va']
    return ""


def main():
    """
    main
    """

    # Parse the command arguments
    if len(sys.argv) != 6:
        # User Input

        # Input - IP
        valip = input("Enter DALION IP address: ")

        # Input - Destination (channel number)
        valch = input("Enter channel number (1-4): ")

        # Input - Destination (lamp, group or channel)
        strd = """Select destination:
        1) Lamp
        2) Group
        3) Channel
        """
        valc = input(strd)
        valc = int(valc)

        ## Input - Lamp or group index
        valii = -1
        if valc == 1:
            # Input - Lamp index
            valii = input("Enter lamp index (0-63): ")
        elif valc == 2:
            # Input - Group index
            valii = input("Enter group index (0-15): ")

        # Input - Value choice
        print("Select type: ")
        index = 0
        for variable in device_variables.device_variables:
            index = index + 1
            if variable['ty'] != 'lt':
                vstr =  "    "
                vstr += str(index)
                vstr += ") "
                vstr += (" " if index < 10 else "")
                vstr += variable['tx']
                print(vstr)
        valvi = input("    ")
        valvi = int(valvi) - 1
        variable = device_variables.device_variables[valvi]
        valid = variable['id']
    else:
        # Command line arguments

        # ip
        valip = sys.argv[1]
        # channel
        valch = sys.argv[2]
        # destination (lamp, group, channel)
        valc = sys.argv[3]
        # lamp index, group index, -1 channel
        valii = sys.argv[4]
        # variable id
        valid = sys.argv[5]

        valc = int(valc)

        # Find the variable for valid
        index = 0
        for variable in device_variables.device_variables:
            if variable['id'] == valid:
                valvi = index
                break
            index = index + 1
        variable = device_variables.device_variables[valvi]


    # Valid arguments
    bvalid = valid_arguments(valip, valch, valc, valii, valid)
    if bvalid is False:
        sys.exit()

    # Prepare the URL
    url = prepare_url(valip, valch, valc, valii)

    # Print the URL
    print("")
    print("Request: ")
    print(url)
    print("")

    # Send the request
    response = send_request(url)

    # Parse the response
    response = parse_response(response, valid)

    # Print the response
    print("Response: ")
    print(response)
    print("")


if __name__ == '__main__':
    main()
