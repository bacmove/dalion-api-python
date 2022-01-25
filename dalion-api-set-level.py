import sys
import urllib.request
import urllib.parse
import json

#
# dalion-api-set-level.py
#
# Allows modifying the light intensity of a lamp, group or channel.
# The parameters can be passed via command line arguments or via user input.
#
# Usage - User input
# dalion-api-set-level.py
#
# Usage - Command line arguments
# dalion-api-set-level.py IP channel destination destination-index value
#
# IP: The DALION IP address.
# channel: The channel number, 1-4. 
# destination: 1 = lamp, 2 = group, 3 = channel.
# destination-index: lamp index 0-63, group index 0-15 or channel -1.
# value: the light intensity value in percent.
#
# Exemple: 
# Set light intensity to 10% for the channel 1.
# dalion-api-set-level.py 192.168.0.210 1 3 -1 100
#
# Set light intensity to 90% for the group 2 on the channel 1.
# dalion-api-set-level.py 192.168.0.210 1 2 2 900
#
# Set light intensity to 0% for the lamp 0 on the channel 1.
# dalion-api-set-level.py 192.168.0.210 1 1 0 0
#

if len(sys.argv) != 6:
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
    if valc == 1:
        # Input - Lamp index
        valii = input("Enter lamp index: ")
    elif valc == 2:
        # Input - Group index
        valii = input("Enter group index: ")    

    # Input - Value in percent
    valv = input("Enter light intensity in percent %: ")
else:
    # Command line argument

    valip = sys.argv[1]
    valch = sys.argv[2]
    valc  = sys.argv[3]
    valii = sys.argv[4]
    valv  = sys.argv[5]

    valc = int(valc)

# Prepare the URL

## Parameter - IP
url = "http://" + valip

## Parameter - URL
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
device = json.dumps([{'id': 'dval', 'va': str(float(valv) * 10)}])
device = urllib.parse.quote_plus(device)
url += "&device=" + device

print(url)

# Send the HTTP GET request
response = urllib.request.urlopen(url).read()
print(response)
