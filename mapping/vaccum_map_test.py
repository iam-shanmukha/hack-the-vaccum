import tinytuya
import json
import time

vacuum = tinytuya.Device(
    dev_id="YOUR_DEVICE_ID_HERE",
    address="YOUR_VACUUM_IP_HERE",
    local_key="YOUR_LOCAL_KEY_HERE",
    version=3.3
)

# Try to get map data through various DPS points
print("Attempting to retrieve map data...")

# Check for map-related DPS (common ones: 110-125, 350-365)
map_dps = [110, 111, 112, 113, 114, 115, 120, 121, 122, 
           350, 351, 360, 361, 362, 363, 364, 365,
           199, 200, 201, 202, 203]

for dps in map_dps:
    try:
        result = vacuum.get_value(dps)
        if result:
            print(f"\nDPS {dps}: {result}")
    except Exception as e:
        pass

# Try cloud API for map
print("\n\nTrying cloud API for map data...")
from tinytuya import Cloud

# TODO: Replace with your Tuya Cloud API credentials
DEVICE_ID_FOR_CLOUD = "YOUR_DEVICE_ID_HERE"

cloud = Cloud(
    apiRegion="in",
    apiKey="YOUR_API_KEY_HERE",
    apiSecret="YOUR_API_SECRET_HERE"
)

# Try to get map through cloud
try:
    # Device properties
    props = cloud.cloudrequest(f'/v1.0/devices/{DEVICE_ID_FOR_CLOUD}/properties')
    print("Device Properties:")
    print(json.dumps(props, indent=2))
except Exception as e:
    print(f"Properties error: {e}")

try:
    # Device functions
    functions = cloud.cloudrequest(f'/v1.0/devices/{DEVICE_ID_FOR_CLOUD}/functions')
    print("\nDevice Functions:")
    print(json.dumps(functions, indent=2))
except Exception as e:
    print(f"Functions error: {e}")

try:
    # Try getting map specifically
    map_data = cloud.cloudrequest(f'/v2.0/cloud/thing/{DEVICE_ID_FOR_CLOUD}/map')
    print("\nMap Data:")
    print(json.dumps(map_data, indent=2))
except Exception as e:
    print(f"Map error: {e}")