import tinytuya
import json
import time

# Your vacuum credentials
# TODO: Replace with your actual credentials
# Get these from: https://iot.tuya.com or see docs/SETUP_GUIDE.md
DEVICE_ID = "YOUR_DEVICE_ID_HERE"        # e.g., "d7921b8722a14bbf3da8di"
IP_ADDRESS = "YOUR_VACUUM_IP_HERE"       # e.g., "192.168.1.100"
LOCAL_KEY = "YOUR_LOCAL_KEY_HERE"        # e.g., "Vwel'|(#;Nkbc{^o"

# Connect to vacuum
vacuum = tinytuya.Device(
    dev_id=DEVICE_ID,
    address=IP_ADDRESS,
    local_key=LOCAL_KEY,
    version=3.3
)

vacuum.set_socketPersistent(True)

print("=" * 50)
print("Eureka Forbes LVAC Voice Pro Controller")
print("=" * 50)

# Get current status
print("\n1. Getting current status...")
try:
    data = vacuum.status()
    print("Status Response:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Detect available data points (DPS)
print("\n2. Detecting available controls (DPS)...")
try:
    dps = vacuum.detect_available_dps()
    print("Available Data Points:")
    print(json.dumps(dps, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Get detailed device info
print("\n3. Getting device details...")
try:
    info = vacuum.generate_payload(tinytuya.UPDATEDPS)
    print(json.dumps(info, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Interactive Control Menu")
print("=" * 50)
print("Commands you can try:")
print("  vacuum.set_value(1, True)   # Start cleaning")
print("  vacuum.set_value(1, False)  # Stop/Pause")
print("  vacuum.set_value(3, 'gentle')  # Set fan speed")
print("  vacuum.set_value(101, 50)   # Set suction power")