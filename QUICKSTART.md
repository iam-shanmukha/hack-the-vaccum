# Quick Start Guide - 5 Minutes to Controlling Your Vacuum

Get your Eureka Forbes LVAC Voice Pro under local control in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.7+ installed
- [ ] Vacuum connected to WiFi
- [ ] Computer on same network as vacuum
- [ ] Device credentials available (or ready to get them)

## Step 1: Install (30 seconds)

```bash
cd banthi-decoder
pip3 install -r requirements.txt
```

**Verify:**
```bash
python3 -c "import tinytuya; print('OK')"
```

## Step 2: Get Credentials (2-3 minutes)

### Quick Method - Network Scan

```bash
python3 discovery/tuyatest.py
```

This shows your vacuum's IP address. Note it down.

### Get Full Credentials

You need:
1. **Device ID** - From Tuya IoT platform
2. **Local Key** - From Tuya IoT platform
3. **IP Address** - From above scan

**Don't have them?** See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed instructions.

## Step 3: Configure (1 minute)

Edit `control/vacuum_controller.py` lines 7-11:

```python
self.vacuum = tinytuya.Device(
    dev_id="d7921b8722a14bbf3da8di",    # Your device ID
    address="192.168.84.145",           # Your vacuum's IP
    local_key="Vwel'|(#;Nkbc{^o",      # Your local key
    version=3.3                         # Keep as 3.3
)
```

**Save the file.**

## Step 4: Test Connection (30 seconds)

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
...
```

Choose **option 1** to view status.

**Expected output:**
```
==================================================
VACUUM STATUS
==================================================
Power:          False
Status:         standby
Battery:        100%
...
```

**Success!** You're connected.

## Step 5: Try Basic Commands (1 minute)

Still in the menu:

1. **Option 7: Find Robot**
   - Vacuum should beep
   - Safe test of communication

2. **Option 4: Return to Dock**
   - Vacuum should move to charger
   - Tests movement commands

3. **Option 2: Start Cleaning**
   - Vacuum should start cleaning
   - Full functionality test

**All working?** You have full control!

## Common Issues

### "Connection refused"

**Fix:**
```bash
# Check vacuum is reachable
ping 192.168.x.x

# Check port is open
nc -zv 192.168.x.x 6668
```

### "Decrypt failed"

**Fix:**
- Verify local key is correct
- Check device ID matches
- Ensure version is 3.3

### "No response"

**Fix:**
- Ensure vacuum is powered on
- Check WiFi indicator is solid (not blinking)
- Try restarting vacuum

## Next Steps

### Extract Map Data

```bash
# Start vacuum cleaning first
python3 control/vacuum_controller.py  # Option 2

# Then in another terminal
python3 mapping/banthi_get_map.py  # Option 1

# Visualize
python3 mapping/map_visualizer_v2.py
```

Check output file: `room_map_proper.png`

### Explore All Features

In the controller menu:
- [5] Set suction mode (gentle/normal/max)
- [6] Set water level (low/medium/high)
- [8] Toggle Do Not Disturb mode
- [9] Toggle auto carpet boost
- [10] Check maintenance status

### Monitor Live

```bash
python3 mapping/live_map.py  # Option 3
```

## Script Execution Order

For complete exploration:

```bash
# 1. Discovery
python3 discovery/tuyatest.py

# 2. Basic control
python3 control/vacuum_controller.py

# 3. Map extraction
python3 mapping/banthi_get_map.py

# 4. Visualization
python3 mapping/map_visualizer_v2.py

# 5. Advanced testing
python3 utils/banthi_dps_mapping.py
```

## Quick Command Reference

### Start Cleaning
```bash
python3 control/vacuum_controller.py
# Choose option 2
```

### Stop Cleaning
```bash
python3 control/vacuum_controller.py
# Choose option 3
```

### Return to Dock
```bash
python3 control/vacuum_controller.py
# Choose option 4
```

### Get Status
```bash
python3 control/vacuum_controller.py
# Choose option 1
```

### Extract Map
```bash
python3 mapping/banthi_get_map.py
# Choose option 1 or 2
```

## Python API Quick Reference

### Direct Control (Without Menu)

```python
import tinytuya

# Connect
vacuum = tinytuya.Device(
    dev_id="your_id",
    address="192.168.x.x",
    local_key="your_key",
    version=3.3
)

# Start cleaning
vacuum.set_value('1', True)

# Return to dock
vacuum.set_value('4', 'chargego')

# Get status
status = vacuum.status()
battery = status['dps']['26']
print(f"Battery: {battery}%")
```

## Directory Quick Reference

```
control/      - Vacuum control scripts (START HERE)
discovery/    - Find devices and credentials
mapping/      - Map extraction and visualization
utils/        - Testing and exploration tools
data/         - Sample data and configurations
docs/         - Detailed documentation
```

## Help Resources

### Documentation
- [README.md](README.md) - Full project overview
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed setup
- [docs/PROTOCOL.md](docs/PROTOCOL.md) - Technical details

### Per-Directory Help
- [control/README.md](control/README.md)
- [discovery/README.md](discovery/README.md)
- [mapping/README.md](mapping/README.md)
- [utils/README.md](utils/README.md)

### Common Tasks
- Getting credentials → [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md#getting-device-credentials)
- Connection issues → [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md#troubleshooting)
- Map extraction → [mapping/README.md](mapping/README.md)
- DPS discovery → [utils/README.md](utils/README.md)

## Success Checklist

- [ ] Dependencies installed
- [ ] Device credentials obtained
- [ ] Configuration updated
- [ ] Connection test passed
- [ ] Basic commands work
- [ ] Map extraction works (optional)

**All checked?** You're ready to fully control your vacuum!

## Safety Notes

All commands are safe. The vacuum has built-in protections:
- Won't start if lifted
- Auto-stops on errors
- Returns to dock on low battery
- Collision detection active

Feel free to experiment!

## What's Next?

1. **Read the docs** - [docs/PROTOCOL.md](docs/PROTOCOL.md) for technical details
2. **Explore features** - Try all menu options
3. **Extract maps** - Understand your floor plan
4. **Customize** - Modify scripts for your needs
5. **Discover** - Find new DPS values and features

**Have fun controlling your robot!**
