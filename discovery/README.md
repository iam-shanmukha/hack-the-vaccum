# Discovery Scripts

Tools for discovering and connecting to Tuya devices on your network.

## Scripts

### tuyatest.py

**Network scanner for Tuya devices.**

Scans your local network for all Tuya-compatible devices.

**Usage:**
```bash
python3 tuyatest.py
```

**Output:**
```
Found devices:
IP: 192.168.1.100
  Version: 3.3
  Product ID: d7921b8722a14bbf3da8di
```

### tuya_get_local.py

**Cloud API connection script.**

Connects to Tuya Cloud to retrieve device information.

**Configuration Required:**
Edit lines 5-8:
```python
API_REGION = "in"  # Your region
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
DEVICE_ID = "your_device_id"
```

**Usage:**
```bash
python3 tuya_get_local.py
```

**Gets:**
- Device details
- All registered devices
- Device status from cloud

### vaccumpy.py

**UDP broadcast listener.**

Listens for Tuya device broadcasts on port 6667.

**Usage:**
```bash
python3 vaccumpy.py
```

**When to use:**
- Device discovery without cloud
- Protocol analysis
- Network debugging
- Packet structure examination

**Output:**
```
[12:34:56] Packet from 192.168.1.100:6667
Length: 256 bytes
✓ Magic header found: 0x55aa
  Packet type: 0x0001 (1)
  Payload length: 240

Hex dump:
  0000: 00 00 55 aa 00 00 00 01 ...
```

## Discovery Process

### Step 1: Find IP Address

**Method A - Router:**
Check your router's DHCP client list for "Tuya" or "Smart Life" devices.

**Method B - Network scan:**
```bash
python3 tuyatest.py
```

**Method C - nmap:**
```bash
nmap -p 6668 192.168.1.0/24
```

### Step 2: Get Credentials

**Via Cloud (Recommended):**
1. Create account at [iot.tuya.com](https://iot.tuya.com)
2. Link Smart Life app
3. Get API key and secret
4. Run `tuya_get_local.py`

**Via Packet Capture:**
1. Run `vaccumpy.py`
2. Press button on vacuum
3. Analyze broadcast packet
4. Extract device ID

### Step 3: Test Connection

```bash
python3 -c "
import tinytuya
d = tinytuya.Device('device_id', '192.168.x.x', 'local_key', version=3.3)
print(d.status())
"
```

## Troubleshooting

**No devices found:**
- Ensure vacuum is connected to WiFi (not AP mode)
- Check you're on same network
- Verify 2.4GHz WiFi (Tuya requires 2.4GHz)

**Cloud API errors:**
- Verify API credentials
- Check region setting
- Ensure device is linked in app

**UDP listener silent:**
- Check firewall allows UDP 6667
- Try triggering activity (press vacuum button)
- Verify network interface

## Security Notes

Keep credentials secure:
- API keys provide access to all your devices
- Local key allows full device control
- Never commit credentials to git
- Use environment variables when possible

## See Also

- [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) - Getting credentials
- [../docs/PROTOCOL.md](../docs/PROTOCOL.md) - Protocol details
