"""
dalion_api_set_colour.py

Allows modifying the colour of a lamp, group or channel.
The parameters can be passed via command line arguments or via user input.

Usage - User input
dalion_api_set_colour.py

Usage - Command line arguments
dalion_api_set_colour.py ip channel destination destination-index cid ctype cvalue

ip: The DALION IP address.
channel: The channel number, 1-4.
destination: 1 = lamp, 2 = group, 3 = channel.
destination-index: Lamp short address 0-63, group index 0-15 or channel -1.
cid: Indicates the colour to modify (d8ac, dvpl, dvsl, dvnl, dvxl, d8s0-15, d8tw, d8tc).
ctype: Indicates the type of colour
    (16 = xy-coordinate, 32 = colour temperature Tc, 64 = primary N, 128 = RGBWAF).
cvalue: Indicates the value of the colour.

Exemples:
Set light colour temperature to 2500 Kelvin for the channel 1.
dalion_api_set_colour.py 192.168.0.210 1 3 -1 d8ac 32 2500

Set light colour temperature to 4000 Kelvin for the group 2 on the channel 1.
dalion_api_set_colour.py 192.168.0.210 1 2 2 d8ac 32 4000
"""

import sys
import urllib.request
import urllib.parse
import json


DEF_CID = [
    {"id": "d8ac",  "name": "Actual Level"},
    {"id": "d8tp",  "name": "Power On Level"},
    {"id": "d8tf",  "name": "System Failure Level"},
    {"id": "d8s0",  "name": "Scene 0"},
    {"id": "d8s1",  "name": "Scene 1"},
    {"id": "d8s2",  "name": "Scene 2"},
    {"id": "d8s3",  "name": "Scene 3"},
    {"id": "d8s4",  "name": "Scene 4"},
    {"id": "d8s5",  "name": "Scene 5"},
    {"id": "d8s6",  "name": "Scene 6"},
    {"id": "d8s7",  "name": "Scene 7"},
    {"id": "d8s8",  "name": "Scene 8"},
    {"id": "d8s9",  "name": "Scene 9"},
    {"id": "d8s10", "name": "Scene 10"},
    {"id": "d8s11", "name": "Scene 11"},
    {"id": "d8s12", "name": "Scene 12"},
    {"id": "d8s13", "name": "Scene 13"},
    {"id": "d8s14", "name": "Scene 14"},
    {"id": "d8s15", "name": "Scene 15"},
    {"id": "d8tw",  "name": "Warmest Tc"},
    {"id": "d8tc",  "name": "Coolest Tc"}
]

"""
"" List of cid.
"""

DEF_CTYPE = [
    {"id": 16,   "name": "xy-coordinate"},
    {"id": 32,   "name": "colour temperature Tc"},
    {"id": 64,   "name": "primary N"},
    {"id": 128,  "name": "RGBWAF"}
]

"""
"" List of ctype.
"""

DEF_DEFAULT_CVALUE = {
	"type": 0x10,
	"value": {
		"ll": 65535,
		"xx": 65535,
		"xy": 65535,
		"tc": 65535,
		"p0": 65535,
		"p1": 65535,
		"p2": 65535,
		"p3": 65535,
		"p4": 65535,
		"p5": 65535,
		"rr": 255,
		"rg": 255,
		"rb": 255,
		"rw": 255,
		"ra": 255,
		"rf": 255,
		"ll_isMask": True,
		"xx_isMask": True,
		"xy_isMask": True,
		"tc_isMask": True,
		"p0_isMask": True,
		"p1_isMask": True,
		"p2_isMask": True,
		"p3_isMask": True,
		"p4_isMask": True,
		"p5_isMask": True,
		"rr_isMask": True,
		"rg_isMask": True,
		"rb_isMask": True,
		"rw_isMask": True,
		"ra_isMask": True,
		"rf_isMask": True
	}
}

"""
"" Default cvalue.
"""



def valid_arguments(valip, valch, valc, valii):
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

    return bvalid


def prepare_url(valip, valch, valc, valii,
        valcid, valctype,
        valcvalue_xx, valcvalue_xy,
        valcvalue_tc,
        valcvalue_p0, valcvalue_p1, valcvalue_p2, valcvalue_p3, valcvalue_p4, valcvalue_p5,
        valcvalue_rr, valcvalue_rg, valcvalue_rb, valcvalue_rw, valcvalue_ra, valcvalue_rf):
    """
    Prepare the URL
    """

    ## Parameter - IP
    url = "http://" + valip

    ## Parameter - URL - action
    url += "/api/v100/dali_devices.ssi?action=set_colour"

    ## Parameter - Channel
    url += "&ch=" + valch

    ## Parameter - Lamp index, group index or channel
    if valc == 1:
        # Lamp index
        valii = json.dumps([valii])
        valii = urllib.parse.quote_plus(valii)
        url += "&sa=" + valii
    elif valc == 2:
        # Group index
        valii = json.dumps([valii])
        valii = urllib.parse.quote_plus(valii)
        url += "&gi=" + valii
    else:
        # Channel
        valii = json.dumps([-1])
        valii = urllib.parse.quote_plus(valii)
        url += "&gi=" + valii

    ## Parameter - cid
    url += "&cid=" + valcid

    ## Parameter - ctype
    url += "&ctype=" + str(valctype)

    ## Parameter - cvalue
    valcvalue = DEF_DEFAULT_CVALUE
    valcvalue['type'] = valctype
    if valctype == 16:
        ## xy-coordinate
        valcvalue['value']['xx'] = valcvalue_xx
        valcvalue['value']['xy'] = valcvalue_xy

        valcvalue['value']['xx_isMask'] = False
        valcvalue['value']['xy_isMask'] = False
    elif valctype == 32:
        ## colour temperature Tc
        valcvalue['value']['tc'] = valcvalue_tc

        valcvalue['value']['tc_isMask'] = False
    elif valctype == 64:
        ## primary N
        valcvalue['value']['p0'] = valcvalue_p0
        valcvalue['value']['p1'] = valcvalue_p1
        valcvalue['value']['p2'] = valcvalue_p2
        valcvalue['value']['p3'] = valcvalue_p3
        valcvalue['value']['p4'] = valcvalue_p4
        valcvalue['value']['p5'] = valcvalue_p5

        valcvalue['value']['p0_isMask'] = False
        valcvalue['value']['p1_isMask'] = False
        valcvalue['value']['p2_isMask'] = False
        valcvalue['value']['p3_isMask'] = False
        valcvalue['value']['p4_isMask'] = False
        valcvalue['value']['p5_isMask'] = False
    elif valctype == 128:
        ## RGBWAF
        valcvalue['value']['rr'] = valcvalue_rr
        valcvalue['value']['rg'] = valcvalue_rg
        valcvalue['value']['rb'] = valcvalue_rb
        valcvalue['value']['rw'] = valcvalue_rw
        valcvalue['value']['ra'] = valcvalue_ra
        valcvalue['value']['rf'] = valcvalue_rf

        valcvalue['value']['rr_isMask'] = False
        valcvalue['value']['rg_isMask'] = False
        valcvalue['value']['rb_isMask'] = False
        valcvalue['value']['rw_isMask'] = False
        valcvalue['value']['ra_isMask'] = False
        valcvalue['value']['rf_isMask'] = False

    valcvalue = json.dumps(valcvalue)
    valcvalue = urllib.parse.quote_plus(valcvalue)
    url += "&cvalue=" + valcvalue

    return url


def send_request(url):
    """
    Send the HTTP GET request
    """

    response = urllib.request.urlopen(url).read()

    return response


def main():
    """
    main
    """

    # User inputs
    # User inputs - IP
    valip = "192.168.0.210"
    # User inputs - channel
    valch = "0"
    # User inputs - lamp or groups index
    valii = -1
    # User inputs - cid
    valcid = "d8ac"
    # User inputs - ctype
    valctype = 32
    # User inputs - cvalue
    # User inputs - cvalue - xy-coordinate
    valcvalue_xx = 65535
    valcvalue_xy = 65535
    # User inputs - cvalue - colour temperature Tc
    valcvalue_tc = 65535
    # User inputs - cvalue - primary N
    valcvalue_p0 = 65535
    valcvalue_p1 = 65535
    valcvalue_p2 = 65535
    valcvalue_p3 = 65535
    valcvalue_p4 = 65535
    valcvalue_p5 = 65535
    # User inputs - cvalue - RGBWAF
    valcvalue_rr = 255
    valcvalue_rg = 255
    valcvalue_rb = 255
    valcvalue_rw = 255
    valcvalue_ra = 255
    valcvalue_rf = 255

    # Parse the command arguments
    if len(sys.argv) < 7:
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
            valii = input("Enter lamp short address (0-63): ")
        elif valc == 2:
            # Input - Group index
            valii = input("Enter group index (0-15): ")

        # Input - cid
        print("Select cid: ")
        index = 0
        for cid in DEF_CID:
            index = index + 1

            vstr =  "    "
            vstr += str(index)
            vstr += ") "
            vstr += (" " if index < 10 else "")
            vstr += cid['name']
            print(vstr)

        valcid = input("    ")
        valcid = int(valcid) - 1
        cid = DEF_CID[valcid]
        valcid = cid['id']

        # Input - ctype
        print("Select ctype: ")
        index = 0
        for ctype in DEF_CTYPE:
            index = index + 1

            vstr =  "    "
            vstr += str(index)
            vstr += ") "
            vstr += (" " if index < 10 else "")
            vstr += ctype['name']
            print(vstr)

        valctype = input("    ")
        valctype = int(valctype) - 1
        ctype = DEF_CTYPE[valctype]
        valctype = ctype['id']

        # Input - cvalue
        print("Enter the value")
        if valctype == 16:
            ## xy-coordinate
            valcvalue_xx = input("x-coordinate (0-65535): ")
            valcvalue_xy = input("y-coordinate (0-65535): ")
        elif valctype == 32:
            ## colour temperature Tc
            valcvalue_tc = input("Kelvin (0-65535): ")
            ## Kelvin to Mirek
            valcvalue_tc = int(valcvalue_tc)
            valcvalue_tc = int(1000000 / valcvalue_tc)
        elif valctype == 64:
            ## primary N
            valcvalue_p0 = input("primary N 0 (0-65535): ")
            valcvalue_p1 = input("primary N 1 (0-65535): ")
            valcvalue_p2 = input("primary N 2 (0-65535): ")
            valcvalue_p3 = input("primary N 3 (0-65535): ")
            valcvalue_p4 = input("primary N 4 (0-65535): ")
            valcvalue_p5 = input("primary N 5 (0-65535): ")
        elif valctype == 128:
            ## RGBWAF
            valcvalue_rr = input("Red (0-255): ")
            valcvalue_rg = input("Green (0-255): ")
            valcvalue_rb = input("Blue (0-255): ")
            valcvalue_rw = input("White (0-255): ")
            valcvalue_ra = input("Amber (0-255): ")
            valcvalue_rf = input("Freecolour (0-255): ")

    else:
        # Command line arguments

        # ip
        valip = sys.argv[1]

        # channel
        valch = sys.argv[2]

        # destination (lamp, group, channel)
        valc = sys.argv[3]

        # lamp short address, group index, -1 channel
        valii = sys.argv[4]

        # cid
        valcid = sys.argv[5]

        # ctype
        valctype = sys.argv[6]
        # Find the variable for valid
        valctype = int(valctype)
        if valctype < len(DEF_CID):
            valctype = DEF_CID[valctype]['id']

        if valctype == 16:
            ## xy-coordinate
            valcvalue_xx = sys.argv[7]
            valcvalue_xy = sys.argv[8]
        elif valctype == 32:
            ## colour temperature Tc
            valcvalue_tc = sys.argv[7]
            ## Kelvin to Mirek
            valcvalue_tc = int(valcvalue_tc)
            valcvalue_tc = int(1000000 / valcvalue_tc)
        elif valctype == 64:
            ## primary N
            valcvalue_p0 = sys.argv[7]
            valcvalue_p1 = sys.argv[8]
            valcvalue_p2 = sys.argv[9]
            valcvalue_p3 = sys.argv[10]
            valcvalue_p4 = sys.argv[11]
            valcvalue_p5 = sys.argv[12]
        elif valctype == 128:
            ## RGBWAF
            valcvalue_rr = sys.argv[7]
            valcvalue_rg = sys.argv[8]
            valcvalue_rb = sys.argv[9]
            valcvalue_rw = sys.argv[10]
            valcvalue_ra = sys.argv[11]
            valcvalue_rf = sys.argv[12]

    # Valid arguments
    bvalid = valid_arguments(valip, valch, valc, valii)
    if bvalid is False:
        sys.exit()

    # Prepare the URL
    url = prepare_url(valip, valch, valc, valii,
        valcid, valctype,
        valcvalue_xx, valcvalue_xy,
        valcvalue_tc,
        valcvalue_p0, valcvalue_p1, valcvalue_p2, valcvalue_p3, valcvalue_p4, valcvalue_p5,
        valcvalue_rr, valcvalue_rg, valcvalue_rb, valcvalue_rw, valcvalue_ra, valcvalue_rf)

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


if __name__ == '__main__':
    main()
