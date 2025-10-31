import tinytuya
import time 
import json
vacuum = tinytuya.Device(
    dev_id="YOUR_DEVICE_ID_HERE",
    address="YOUR_VACUUM_IP_HERE",
    local_key="YOUR_LOCAL_KEY_HERE",
    version=3.3
)

# Map the function names to DPS numbers
# Based on common Tuya vacuum patterns:

print("Testing map-related DPS...")

# Request map (try all possible DPS)
test_dps = {
    'request_map': [106, 121, 122, 123, 124, 125],
    'path_data': [107, 110, 111, 112, 113, 114],
    'command_trans': [108, 115, 116, 117],
}

for func_name, dps_list in test_dps.items():
    print(f"\nTesting {func_name}:")
    for dps in dps_list:
        try:
            # First try to read
            value = vacuum.status()
            if 'dps' in value and str(dps) in value['dps']:
                print(f"  DPS {dps}: {value['dps'][str(dps)]}")
        except:
            pass

# Now request the map
print("\n\nRequesting map data...")
for dps in [106, 121, 122, 123]:
    try:
        result = vacuum.set_value(dps, 'get_both')
        print(f"Request via DPS {dps}: {result}")
    except Exception as e:
        print(f"DPS {dps} failed: {e}")

# Wait and check for updates
time.sleep(3)
print("\nChecking status after request...")
status = vacuum.status()
print(json.dumps(status, indent=2))
