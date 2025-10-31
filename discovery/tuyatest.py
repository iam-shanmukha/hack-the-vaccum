# Install tinytuya
# pip3 install tinytuya

import tinytuya
import socket

# First, let's scan for Tuya devices
print("Scanning for Tuya devices...")
devices = tinytuya.deviceScan(verbose=False)

print("\nFound devices:")
for ip, info in devices.items():
    print(f"IP: {ip}")
    print(f"  Version: {info['version']}")
    print(f"  Product ID: {info.get('gwId', 'Unknown')}")
    print()

# Try to connect to your vacuum
# You'll need: Device ID, Local Key, and IP
# device_id = "YOUR_DEVICE_ID"      # Get from Tuya Cloud
# local_key = "YOUR_LOCAL_KEY"      # Get from Tuya Cloud
# device_ip = "192.168.84.145"

# Uncomment when you have credentials:
# vacuum = tinytuya.Device(device_id, device_ip, local_key)
# vacuum.set_version(3.3)  # Tuya protocol version
# 
# print("Getting vacuum status...")
# status = vacuum.status()
# print(status)