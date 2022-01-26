# DALION API Python

## Overview

Any programming language capable of sending HTTP GET requests can interact with DALI lamps through the DALION.

The data are transferred in the JSON format and with URL parameters.

For example, the HTTP GET requests can be sent via a command line script with the cURL command.

```bash
curl -X "GET" "http://192.168.0.210/api/v100/dali_devices.ssi?action=set_level&ch=1&sa=3&da=1000"
```

## Python

This is a collection of sample Python scripts that use the DALION API.
