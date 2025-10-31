# Eureka Forbes LVAC Voice Pro - Complete Setup Guide

This guide will walk you through the entire process of setting up local control for your Eureka Forbes LVAC Voice Pro vacuum cleaner.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Getting Device Credentials](#getting-device-credentials)
4. [Configuration](#configuration)
5. [First Connection](#first-connection)
6. [Running Scripts](#running-scripts)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements
- Eureka Forbes LVAC Voice Pro vacuum cleaner
- Computer on the same WiFi network as the vacuum
- WiFi router with 2.4GHz support (Tuya devices require 2.4GHz)

### Software Requirements
- Python 3.7 or higher
- pip (Python package manager)
- Network access to vacuum's IP address

### Knowledge Requirements
- Basic command line usage
- Basic Python knowledge (helpful but not required)

## Installation

### Step 1: Install Python

**Check if Python is installed:**
```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Clone or Download Project

```bash
cd ~/Documents
# If you have the project already:
cd banthi-decoder
```

### Step 3: Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install tinytuya matplotlib numpy
```

### Step 4: Verify Installation

```bash
python3 -c "import tinytuya; print('TinyTuya version:', tinytuya.__version__)"
```

## Getting Device Credentials

You need three pieces of information to connect to your vacuum:

1. **Device ID** - Unique identifier for your vacuum
2. **Local Key** - Encryption key for local communication
3. **IP Address** - Network address of your vacuum

### Method 1: Using Tuya IoT Platform (Recommended)

**Step 1: Create Tuya Developer Account**

1. Go to [iot.tuya.com](https://iot.tuya.com/)
2. Sign up for a free developer account
3. Verify your email

**Step 2: Create Cloud Project**

1. Go to "Cloud" → "Development"
2. Create a new project
3. Note your **API Key** and **API Secret**
4. Select your data center region (e.g., "India" for `.in`)

**Step 3: Link Smart Life App**

1. Go to "Cloud" → "API Group"
2. Subscribe to "Authorization" service
3. Go to "Devices" → "Link Tuya App Account"
4. Scan QR code with Smart Life app
5. Your devices will appear

**Step 4: Get Device Information**

1. Go to "Cloud" → "API Explorer"
2. Use endpoint: `GET /v1.0/devices/{device_id}`
3. Or run the discovery script:

```bash
python3 discovery/tuya_get_local.py
```

Edit the script with your API credentials first:
```python
API_REGION = "in"  # Your region
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
```

### Method 2: Network Scanning (Quick)

**Step 1: Find Vacuum IP Address**

Check your router's connected devices, or use network scanner:

```bash
# Install nmap if needed
sudo apt install nmap  # Linux
brew install nmap      # macOS

# Scan your network
nmap -p 6668 192.168.1.0/24
```

Look for open port 6668 (Tuya default port)

**Step 2: Scan for Tuya Devices**

```bash
python3 discovery/tuyatest.py
```

This will show all Tuya devices on your network.

**Step 3: Listen for Broadcasts**

```bash
python3 discovery/vaccumpy.py
```

Press a button on the vacuum or start cleaning - it will broadcast packets.

### Method 3: Extracting from Smart Life App (Advanced)

This requires packet capture tools like Wireshark. See network captures in `data/` folder for examples.

## Configuration

### Option 1: Edit Configuration File

Edit `data/tinytuya.json`:

```json
{
    "apiKey": "your_api_key_here",
    "apiSecret": "your_api_secret_here",
    "apiRegion": "in",
    "apiDeviceID": "your_device_id_here"
}
```

### Option 2: Hardcode in Script

Edit `control/vacuum_controller.py` (lines 7-11):

```python
self.vacuum = tinytuya.Device(
    dev_id="your_device_id_here",
    address="192.168.x.x",  # Your vacuum's IP
    local_key="your_local_key_here",
    version=3.3
)
```

**How to find each value:**

- **dev_id**: From Tuya IoT platform or app extraction
- **address**: From router or network scan
- **local_key**: From Tuya IoT platform (in device details)
- **version**: Usually 3.3 for newer devices

## First Connection

### Test Connection

**Step 1: Ensure vacuum is powered on and connected to WiFi**

Check the vacuum's WiFi indicator is solid (not blinking).

**Step 2: Test basic connectivity**

```bash
python3 -c "
import tinytuya

vacuum = tinytuya.Device(
    dev_id='your_device_id',
    address='192.168.x.x',
    local_key='your_local_key',
    version=3.3
)

print(vacuum.status())
"
```

Expected output:
```json
{
  "dps": {
    "1": false,
    "5": "standby",
    "26": 100,
    ...
  }
}
```

### Launch Main Controller

```bash
python3 control/vacuum_controller.py
```

You should see:
```
==================================================
EUREKA FORBES VOICE PRO CONTROLLER
==================================================
1.  Show Status
2.  Start Cleaning
3.  Stop/Pause
4.  Return to Dock
...
```

### First Test Commands

1. **Check status** (Option 1)
   - Should display current battery, mode, etc.

2. **Find robot** (Option 7)
   - Vacuum should beep

3. **Return to dock** (Option 4)
   - Vacuum should navigate to charging station

If these work, you're all set up!

## Running Scripts

### Basic Control

```bash
# Main controller (interactive menu)
python3 control/vacuum_controller.py

# Legacy version
python3 control/vacuum_controller_v1.py
```

### Map Extraction

```bash
# Request and decode map
python3 mapping/banthi_get_map.py

# Visualize existing map data
python3 mapping/map_visualizer_v2.py

# Live map monitoring
python3 mapping/live_map.py

# Decode raw map data
python3 mapping/decode_map.py

# Various visualization options
python3 mapping/visualize_map.py
```

### Discovery and Testing

```bash
# Scan for devices
python3 discovery/tuyatest.py

# Test cloud API
python3 discovery/tuya_get_local.py

# Listen for broadcasts
python3 discovery/vaccumpy.py

# Test DPS values
python3 utils/banthi_dps_mapping.py
```

## Script Execution Order

For first-time setup and exploration:

### 1. Discovery Phase

```bash
# Find your vacuum
python3 discovery/tuyatest.py
```

### 2. Connection Test

```bash
# Edit with your credentials first
python3 control/vacuum_controller.py
# Choose option 1 to view status
```

### 3. Basic Control

```bash
# Still in vacuum_controller.py menu
# Try option 7 (Find Robot) - safe test
# Try option 4 (Return to Dock)
# Try option 2 (Start Cleaning)
```

### 4. Map Extraction

```bash
# Start vacuum cleaning first
python3 mapping/banthi_get_map.py
# Choose option 1 or 2
```

### 5. Visualization

```bash
python3 mapping/map_visualizer_v2.py
# Check output PNG file
```

### 6. Advanced Testing

```bash
# Discover new DPS values
python3 utils/banthi_dps_mapping.py

# Live monitoring
python3 mapping/live_map.py
```

## Troubleshooting

### Issue: "Connection refused" or timeout

**Solutions:**
1. Check vacuum is on WiFi (not in setup mode)
2. Verify IP address is correct
3. Check firewall isn't blocking port 6668
4. Ensure you're on same network as vacuum
5. Try restarting the vacuum

```bash
# Test connectivity
ping 192.168.x.x
nc -zv 192.168.x.x 6668
```

### Issue: "Decrypt failed" or "Invalid key"

**Solutions:**
1. Verify local key is correct
2. Check device ID matches
3. Ensure protocol version is 3.3
4. Try re-linking device in Tuya IoT platform

### Issue: "No response" or empty status

**Solutions:**
1. Increase timeout in script:
```python
vacuum.set_socketTimeout(10)  # 10 seconds
```

2. Enable persistent connection:
```python
vacuum.set_socketPersistent(True)
```

3. Check device is not sleeping

### Issue: Map data not appearing

**Solutions:**
1. Start cleaning first (map generates during cleaning)
2. Try different DPS values (121, 122, 123)
3. Use monitor mode to catch updates
4. Check DPS 15 after requesting map

```bash
python3 mapping/banthi_get_map.py
# Choose option 2 (Monitor mode)
# Open Smart Life app and view map
```

### Issue: Commands not working

**Solutions:**
1. Check current status first
2. Verify vacuum is not in error state
3. Ensure battery is charged (>20%)
4. Try each command individually
5. Check DPS mapping is correct

```bash
# Test individual DPS
python3 utils/banthi_dps_mapping.py
```

### Issue: IP address keeps changing

**Solutions:**
1. Set static IP in router (DHCP reservation)
2. Use MAC address to track device
3. Implement auto-discovery in script

```python
# Add to script:
devices = tinytuya.deviceScan()
vacuum_ip = devices['your_device_id']['ip']
```

### Issue: Import errors

**Solutions:**
```bash
# Reinstall dependencies
pip3 install --upgrade tinytuya matplotlib numpy

# Check installation
pip3 list | grep -E "tinytuya|matplotlib|numpy"
```

## Advanced Configuration

### Persistent Socket Connection

For faster response and continuous monitoring:

```python
vacuum.set_socketPersistent(True)
vacuum.set_socketNODELAY(True)
vacuum.set_socketRetryLimit(3)
```

### Logging and Debugging

```python
import tinytuya
tinytuya.set_debug(True)  # Enable debug output
```

### Environment Variables

Instead of hardcoding credentials:

```bash
export TUYA_DEVICE_ID="your_device_id"
export TUYA_IP="192.168.x.x"
export TUYA_LOCAL_KEY="your_key"
```

```python
import os
vacuum = tinytuya.Device(
    dev_id=os.getenv('TUYA_DEVICE_ID'),
    address=os.getenv('TUYA_IP'),
    local_key=os.getenv('TUYA_LOCAL_KEY'),
    version=3.3
)
```

## Security Best Practices

1. **Never commit credentials to git:**
```bash
# Add to .gitignore
data/tinytuya.json
*.key
credentials.txt
```

2. **Use environment variables** for sensitive data

3. **Limit network access** - firewall rules for port 6668

4. **Regular key rotation** via Tuya IoT platform

5. **Local network only** - don't expose to internet

## Next Steps

Once setup is complete:

1. **Explore all control features** - Try every menu option
2. **Extract and visualize maps** - Understand your floor plan
3. **Monitor live status** - Watch vacuum in real-time
4. **Discover new DPS values** - Find hidden features
5. **Read protocol docs** - Understand how it works

See [PROTOCOL.md](PROTOCOL.md) for technical details.

## Getting Help

If you're stuck:

1. Check error messages carefully
2. Enable debug logging
3. Review network captures in `data/`
4. Compare with working examples
5. Test each component individually

## Success Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (tinytuya, matplotlib, numpy)
- [ ] Device credentials obtained
- [ ] IP address verified
- [ ] Basic connection test passed
- [ ] Status command works
- [ ] Control commands work (find robot, return to dock)
- [ ] Map extraction works
- [ ] Visualization generates images

Congratulations! You now have full local control of your vacuum cleaner.
