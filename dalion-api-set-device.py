import sys
import urllib.request
import urllib.parse
import json

import device_variables

#
# dalion-api-set-device.py
#
# Allows modifying a lamp, group or channel.
# The parameters can be passed via command line arguments or via user input.
#
# Usage - User input
# dalion-api-set-device.py
#
# Usage - Command line arguments
# dalion-api-set-device.py ip channel destination destination-index id value
#
# ip: The DALION IP address.
# channel: The channel number, 1-4. 
# destination: 1 = lamp, 2 = group, 3 = channel.
# destination-index: Lamp index 0-63, group index 0-15 or channel -1.
# id: The variable id.
# value: The value.
#
# Exemple: 
# Set light intensity to 10% for the channel 1.
# dalion-api-set-device.py 192.168.0.210 1 3 -1 dval 100
#
# Set light intensity to 90% for the group 2 on the channel 1.
# dalion-api-set-device.py 192.168.0.210 1 2 2 dval 900
#
# Set light intensity to 0% for the lamp 0 on the channel 1.
# dalion-api-set-device.py 192.168.0.210 1 1 0 dval 0
#
# Set the lamp 1 to the group 0, 1 and 2 on the channel 1.
# dalion-api-set-device.py 192.168.0.210 1 1 1 dvgr 7
#
# Set the fade time to 1 second on the channel 1.
# dalion-api-set-device.py 192.168.0.210 1 3 -1 dvft 2
#

# Valid the arguments
def valid_arguments(valip, valch, valc, valii, valid, valv, variable):
    bvalid = True

    # Type converssion
    valch = int(valch)
    valii = int(valii)

    # Valid the parameters
    # Valid - Channel
    if ((valch < 1) | (valch > 4)):
        print("Channel number is invalid.")
        bvalid = False
    # Valid - Index
    if valc == 1:
        # Lamp index
        if ((valii < 0) | (valii > 63)):
            print("Lamp index is invalid.")
            bvalid = False
    elif valc == 2:
        # Group index
        if ((valii < 0) | (valii > 15)):
            print("Group index is invalid.")
            bvalid = False
    else:
        # Channel
        if (valii != -1):
            print("Channel index is invalid.")
            bvalid = False
    
    if ((variable['ty'] == 'nb') | (variable['ty'] == 'nb10')):
        if (variable['ty'] == 'nb10'):
            valv = float(valv) * 10
        else:
            valv = int(valv)
        if ((valv < int(variable['mi'])) | (valv > int(variable['ma']))):
            print("Variable value is out of range.")
            bvalid = False

    return bvalid


# Prepare the URL
def prepare_url(valip, valch, valc, valii, valid, valv, variable):
    # Prepare the URL

    ## Parameter - IP
    url = "http://" + valip

    ## Parameter - URL - action
    url += "/api/v100/dali_devices.ssi?action=set_device"

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

    ## Parameter - Device
    if (variable['ty'] == 'nb10'):
        va = str(float(valv) * 10)
    else:
        va = valv

    device = json.dumps([{'id': variable['id'], 'va': va}])
    device = urllib.parse.quote_plus(device)
    url += "&device=" + device

    return url


# Send the HTTP GET request
def send_request(url):
    response = urllib.request.urlopen(url).read()

    return response


# Parse the command arguments
if len(sys.argv) != 7:
    # User Input

    # Input - IP
    valip = input("Enter DALION IP address: ")

    # Input - Destination (channel number)
    valch = input("Enter channel number (1-4): ")

    # Input - Destination (lamp, group or channel)
    a = """Select destination: 
    1) Lamp
    2) Group
    3) Channel
    """
    valc = input(a)
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
        if (variable['ty'] != 'lt'):
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

    # Input - Value
    valv = input("Enter the value for " + variable['tx'] + ": ")
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
    # value
    valv = sys.argv[6]

    valc = int(valc)

    # Find the variable for valid
    index = 0
    for variable in device_variables.device_variables:
        if (variable['id'] == valid):
            valvi = index
            break
        index = index + 1
    variable = device_variables.device_variables[valvi]


# Valid arguments
bvalid = valid_arguments(valip, valch, valc, valii, valid, valv, variable)
if bvalid == False:
    sys.exit()

# Prepare the URL
url = prepare_url(valip, valch, valc, valii, valid, valv, variable)

# Print the URL
print("")
print("Request: ")
print(url)
print("")

# Send the request
response = send_request(url)

# Print the response
print("Response: ")
print(response)
print("")
