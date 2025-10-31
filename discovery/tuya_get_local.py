import tinytuya
import json

# Your credentials
API_REGION = "in"
API_KEY = "YOUR_API_KEY_HERE"
API_SECRET = "YOUR_API_SECRET_HERE"
DEVICE_ID = "YOUR_DEVICE_ID_HERE"

print("Connecting to Tuya Cloud...")
cloud = tinytuya.Cloud(
    apiRegion=API_REGION,
    apiKey=API_KEY,
    apiSecret=API_SECRET
)

# Try to get token first
print("\nGetting access token...")
token = cloud.token
if token:
    print(f"✓ Token obtained: {token[:20]}...")
else:
    print("✗ Failed to get token - check API credentials")

# Try different methods to get device info
print("\n1. Trying getdevice()...")
try:
    device_info = cloud.getdevice(DEVICE_ID)
    print(json.dumps(device_info, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n2. Trying getdevices()...")
try:
    devices = cloud.getdevices()
    print(json.dumps(devices, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n3. Trying getstatus()...")
try:
    status = cloud.getstatus(DEVICE_ID)
    print(json.dumps(status, indent=2))
except Exception as e:
    print(f"Error: {e}")